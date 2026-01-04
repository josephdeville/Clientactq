"""
ClayWorks Core Module
=====================

Core components for the ClayWorks GTM framework including:
- Configuration management
- PQS (Pain-Qualified Segments) framework
- PVP (Permissionless Value Propositions) framework
- Prospect scoring engine
"""

from .config import ClayWorksConfig
from .philosophy import PQSFramework, PVPFramework
from .scoring import ProspectScorer

__all__ = [
    "ClayWorksConfig",
    "PQSFramework",
    "PVPFramework",
    "ProspectScorer",
]
