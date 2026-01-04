"""
ClayWorks Messaging Module
==========================

Message creation components for the ClayWorks GTM framework including:
- PQS (Pain-Qualified Segments) message templates
- PVP (Permissionless Value Propositions) message templates
- Dynamic message generation
- Personalization engine
"""

from .templates import PQSTemplate, PVPTemplate, MessageTemplate
from .generator import MessageGenerator
from .personalization import PersonalizationEngine

__all__ = [
    "PQSTemplate",
    "PVPTemplate",
    "MessageTemplate",
    "MessageGenerator",
    "PersonalizationEngine",
]
