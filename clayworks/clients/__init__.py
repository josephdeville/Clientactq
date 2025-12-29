"""
ClayWorks Clients Module
========================

Client management components for the ClayWorks GTM framework including:
- Client intake questionnaire processing
- Proposal generation
"""

from .intake import ClientIntake, IntakeResponse
from .proposals import ProposalGenerator, Proposal

__all__ = [
    "ClientIntake",
    "IntakeResponse",
    "ProposalGenerator",
    "Proposal",
]
