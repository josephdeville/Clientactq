"""
ClayWorks Framework
===================

A comprehensive Go-To-Market (GTM) framework based on Jordan Crawford's Blueprint methodology.

Core Concepts:
- Pain-Qualified Segments (PQS): Target companies experiencing specific, verifiable pain points
- Permissionless Value Propositions (PVP): Deliver immediate, actionable insights before sales

The Fundamental Principle: "The message isn't the problem. The LIST is the message."

Attribution: Based on Jordan Crawford's Blueprint GTM methodology.
Learn more at: https://course.blueprintgtm.com
"""

__version__ = "1.0.0"
__author__ = "ClayWorks Team"
__attribution__ = "Jordan Crawford / Blueprint GTM"

from .core import ClayWorksConfig, ProspectScorer, PQSFramework, PVPFramework
from .data import DataSourceManager, DataRecipeBuilder, EnrichmentPipeline
from .messaging import MessageGenerator, PQSTemplate, PVPTemplate
from .workflows import DiscoveryPhase, RecipeDevPhase, AutomationPhase, ScalePhase
from .analytics import MetricsTracker, ReportGenerator
from .clients import ClientIntake, ProposalGenerator

__all__ = [
    # Core
    "ClayWorksConfig",
    "ProspectScorer",
    "PQSFramework",
    "PVPFramework",
    # Data
    "DataSourceManager",
    "DataRecipeBuilder",
    "EnrichmentPipeline",
    # Messaging
    "MessageGenerator",
    "PQSTemplate",
    "PVPTemplate",
    # Workflows
    "DiscoveryPhase",
    "RecipeDevPhase",
    "AutomationPhase",
    "ScalePhase",
    # Analytics
    "MetricsTracker",
    "ReportGenerator",
    # Clients
    "ClientIntake",
    "ProposalGenerator",
]
