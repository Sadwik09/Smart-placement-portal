"""Recommender Module"""

# Import SkillMatcher from skill_matcher module
import sys
from pathlib import Path

# Add parent directory to path to import skill_matcher
sys.path.append(str(Path(__file__).parent.parent))

from recommender.engine import RecommendationEngine

__all__ = ['RecommendationEngine']
