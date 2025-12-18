from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail
from .models import User, EmailVerificationToken, PasswordResetToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, PasswordResetConfirmSerializer


class RegisterView(APIView):
    """User registration endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create email verification token and send email
            try:
                token_obj = EmailVerificationToken.create_for_user(user)
                verify_link = f"{settings.EMAIL_VERIFICATION_BASE_URL}?token={token_obj.token}"
                send_mail(
                    subject='Verify your email - Smart Placement Portal',
                    message=f'Welcome! Please verify your email by clicking this link: {verify_link}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            except Exception:
                pass
            return Response({
                'message': 'User registered successfully. Please verify your email and await admin approval.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Check if user is approved
            if not user.is_approved:
                return Response({
                    'error': 'Account not approved yet. Please wait for admin approval.'
                }, status=status.HTTP_403_FORBIDDEN)
            # Check if email is verified
            if not user.email_verified:
                return Response({
                    'error': 'Please verify your email before logging in.'
                }, status=status.HTTP_403_FORBIDDEN)
            
            # Authenticate user
            user = authenticate(username=user.username, password=password)
            if user is None:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login successful',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logout successful'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """Verify email using token"""
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token_obj = EmailVerificationToken.objects.get(token=token)
        except EmailVerificationToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        if not token_obj.is_valid():
            return Response({'error': 'Token expired or already used'}, status=status.HTTP_400_BAD_REQUEST)
        token_obj.used = True
        token_obj.save()
        user = token_obj.user
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)


class ResendVerificationView(APIView):
    """Resend email verification link"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'If the email exists, a verification link has been sent.'}, status=status.HTTP_200_OK)
        if user.email_verified:
            return Response({'message': 'Email already verified.'}, status=status.HTTP_200_OK)
        token_obj = EmailVerificationToken.create_for_user(user)
        verify_link = f"{settings.EMAIL_VERIFICATION_BASE_URL}?token={token_obj.token}"
        try:
            send_mail(
                subject='Verify your email - Smart Placement Portal',
                message=f'Please verify your email by clicking this link: {verify_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass
        return Response({'message': 'Verification link sent if the email exists.'}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """Request password reset"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'If the email exists, a reset link has been sent.'}, status=status.HTTP_200_OK)
        token_obj = PasswordResetToken.create_for_user(user)
        reset_link = f"{settings.PASSWORD_RESET_BASE_URL}?token={token_obj.token}"
        try:
            send_mail(
                subject='Reset your password - Smart Placement Portal',
                message=f'Reset your password using this link: {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )
        except Exception:
            pass
        return Response({'message': 'Password reset link sent if the email exists.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """Confirm password reset with token"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        try:
            token_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)
        if not token_obj.is_valid():
            return Response({'error': 'Token expired or already used'}, status=status.HTTP_400_BAD_REQUEST)
        user = token_obj.user
        user.set_password(new_password)
        user.save(update_fields=['password'])
        token_obj.used = True
        token_obj.save()
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
