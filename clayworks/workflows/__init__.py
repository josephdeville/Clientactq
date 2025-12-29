"""
ClayWorks Workflows Module
==========================

Implementation workflow phases for the ClayWorks GTM framework:

Phase 1: Discovery - Map ICP, identify data sources, validate access
Phase 2: Recipe Development - Create data recipes, test messaging
Phase 3: Automation MVP - Build workflows, deploy to test segments
Phase 4: Scale - Multi-channel expansion, monitoring, team training
"""

from .discovery import DiscoveryPhase
from .recipe_dev import RecipeDevPhase
from .automation import AutomationPhase
from .scale import ScalePhase

__all__ = [
    "DiscoveryPhase",
    "RecipeDevPhase",
    "AutomationPhase",
    "ScalePhase",
]
