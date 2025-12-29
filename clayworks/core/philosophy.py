"""
ClayWorks Philosophy Module
===========================

Core philosophical frameworks for the Blueprint GTM methodology:
- PQS (Pain-Qualified Segments): Target companies with verifiable pain points
- PVP (Permissionless Value Propositions): Deliver value before sales conversations

The Fundamental Principle: "The message isn't the problem. The LIST is the message."
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class PainPointCategory(Enum):
    """Categories of verifiable pain points."""
    DEADLINE_PRESSURE = "deadline_pressure"
    COMPLIANCE_REQUIREMENT = "compliance_requirement"
    GROWTH_STRAIN = "growth_strain"
    TECHNOLOGY_GAP = "technology_gap"
    RESOURCE_CONSTRAINT = "resource_constraint"
    COMPETITIVE_THREAT = "competitive_threat"
    LEADERSHIP_CHANGE = "leadership_change"
    FUNDING_PRESSURE = "funding_pressure"


class DataSignalType(Enum):
    """Types of observable data signals."""
    GOVERNMENT_RECORD = "government_record"
    JOB_POSTING = "job_posting"
    TECH_STACK = "tech_stack"
    FUNDING_EVENT = "funding_event"
    EMPLOYEE_CHANGE = "employee_change"
    REVIEW_SENTIMENT = "review_sentiment"
    CONTRACT_AWARD = "contract_award"
    CERTIFICATION = "certification"


@dataclass
class PainSignal:
    """A verifiable signal indicating a specific pain point."""
    signal_type: DataSignalType
    source: str
    data_point: str
    observed_at: datetime
    confidence: float  # 0.0 to 1.0
    raw_data: Optional[Dict[str, Any]] = None


@dataclass
class PainQualifiedSegment:
    """
    A Pain-Qualified Segment (PQS) definition.

    PQS identifies companies experiencing specific, verifiable pain points
    through public data signals. The goal is to create messages that make
    prospects think: "How did they know we're dealing with exactly this?"
    """
    name: str
    description: str
    pain_category: PainPointCategory
    required_signals: List[DataSignalType]
    optional_signals: List[DataSignalType] = field(default_factory=list)
    minimum_confidence: float = 0.7
    scoring_weight: int = 0

    def evaluate_prospect(self, signals: List[PainSignal]) -> Dict[str, Any]:
        """
        Evaluate if a prospect matches this PQS based on their signals.

        Returns:
            Dict containing match status, confidence, and matched signals
        """
        matched_required = []
        matched_optional = []
        total_confidence = 0.0

        for signal in signals:
            if signal.signal_type in self.required_signals:
                matched_required.append(signal)
                total_confidence += signal.confidence
            elif signal.signal_type in self.optional_signals:
                matched_optional.append(signal)
                total_confidence += signal.confidence * 0.5

        # Check if all required signals are present
        required_types_matched = {s.signal_type for s in matched_required}
        all_required_matched = all(
            req in required_types_matched for req in self.required_signals
        )

        # Calculate average confidence
        num_signals = len(matched_required) + len(matched_optional)
        avg_confidence = total_confidence / num_signals if num_signals > 0 else 0

        return {
            "matches": all_required_matched and avg_confidence >= self.minimum_confidence,
            "confidence": avg_confidence,
            "required_signals_matched": matched_required,
            "optional_signals_matched": matched_optional,
            "missing_required": [
                req for req in self.required_signals
                if req not in required_types_matched
            ],
        }


class PQSFramework:
    """
    Pain-Qualified Segments Framework.

    The "Mirror Effect": Reflect their exact situation back to them
    with such accuracy they feel seen.

    Key Principles:
    1. Identify companies with specific, verifiable pain points
    2. Use public data signals as evidence
    3. Create hyper-relevant messaging based on their situation
    """

    def __init__(self):
        self.segments: List[PainQualifiedSegment] = []

    def add_segment(self, segment: PainQualifiedSegment) -> None:
        """Add a PQS to the framework."""
        self.segments.append(segment)

    def create_segment(
        self,
        name: str,
        description: str,
        pain_category: PainPointCategory,
        required_signals: List[DataSignalType],
        optional_signals: List[DataSignalType] = None,
        minimum_confidence: float = 0.7,
        scoring_weight: int = 0,
    ) -> PainQualifiedSegment:
        """Create and add a new PQS."""
        segment = PainQualifiedSegment(
            name=name,
            description=description,
            pain_category=pain_category,
            required_signals=required_signals,
            optional_signals=optional_signals or [],
            minimum_confidence=minimum_confidence,
            scoring_weight=scoring_weight,
        )
        self.add_segment(segment)
        return segment

    def evaluate_prospect(
        self, signals: List[PainSignal]
    ) -> List[Dict[str, Any]]:
        """
        Evaluate a prospect against all PQS segments.

        Returns list of matching segments with confidence scores.
        """
        matches = []
        for segment in self.segments:
            result = segment.evaluate_prospect(signals)
            if result["matches"]:
                matches.append({
                    "segment": segment,
                    "confidence": result["confidence"],
                    "signals": result["required_signals_matched"],
                })

        # Sort by confidence descending
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches

    def get_message_context(
        self, segment: PainQualifiedSegment, signals: List[PainSignal]
    ) -> Dict[str, Any]:
        """
        Build message context from segment and signals for personalization.

        This creates the data needed for the "Mirror Effect" - reflecting
        their exact situation back to them.
        """
        return {
            "pain_category": segment.pain_category.value,
            "segment_name": segment.name,
            "verifiable_facts": [
                {
                    "type": s.signal_type.value,
                    "source": s.source,
                    "data": s.data_point,
                }
                for s in signals
            ],
            "inference": f"Based on {len(signals)} observable signals indicating {segment.description}",
        }


@dataclass
class ValueProposition:
    """
    A Permissionless Value Proposition (PVP) definition.

    PVP delivers immediate, actionable insights based on public data analysis.
    Test: "Would they literally pay for this insight?"
    """
    name: str
    description: str
    insight_type: str  # analysis, benchmark, audit, assessment
    data_sources_required: List[str]
    value_statement: str
    delivery_format: str  # report, scorecard, checklist, comparison

    def generate_hook(self, company_data: Dict[str, Any]) -> str:
        """Generate the data hook for a PVP message."""
        # This would be customized based on actual data
        return f"Analysis of your {self.data_sources_required[0]} shows specific findings"

    def generate_value_extension(self) -> str:
        """Generate the value extension offer."""
        format_descriptions = {
            "report": "the complete analysis",
            "scorecard": "your full scorecard",
            "checklist": "the detailed checklist",
            "comparison": "the full competitive breakdown",
        }
        return f"Want {format_descriptions.get(self.delivery_format, 'more details')}?"


class PVPFramework:
    """
    Permissionless Value Propositions Framework.

    Provide standalone value BEFORE any sales conversation.
    Test: "Would they literally pay for this insight?"

    Key Principles:
    1. Lead with specific, quantified findings about their situation
    2. Explain why this matters NOW
    3. Offer more value (not a meeting)
    """

    def __init__(self):
        self.propositions: List[ValueProposition] = []

    def add_proposition(self, proposition: ValueProposition) -> None:
        """Add a PVP to the framework."""
        self.propositions.append(proposition)

    def create_proposition(
        self,
        name: str,
        description: str,
        insight_type: str,
        data_sources_required: List[str],
        value_statement: str,
        delivery_format: str,
    ) -> ValueProposition:
        """Create and add a new PVP."""
        prop = ValueProposition(
            name=name,
            description=description,
            insight_type=insight_type,
            data_sources_required=data_sources_required,
            value_statement=value_statement,
            delivery_format=delivery_format,
        )
        self.add_proposition(prop)
        return prop

    def build_value_package(
        self, proposition: ValueProposition, company_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build a complete value package for outreach.

        Returns the data hook, value statement, and extension offer.
        """
        return {
            "proposition": proposition.name,
            "data_hook": proposition.generate_hook(company_data),
            "value_statement": proposition.value_statement,
            "value_extension": proposition.generate_value_extension(),
            "delivery_format": proposition.delivery_format,
            "company_specific_data": company_data,
        }

    def get_applicable_propositions(
        self, available_data_sources: List[str]
    ) -> List[ValueProposition]:
        """Get PVPs that can be executed with available data sources."""
        applicable = []
        for prop in self.propositions:
            if all(
                source in available_data_sources
                for source in prop.data_sources_required
            ):
                applicable.append(prop)
        return applicable


# Pre-built common PQS templates
COMMON_PQS_TEMPLATES = {
    "compliance_deadline": PainQualifiedSegment(
        name="Compliance Deadline Pressure",
        description="Company facing upcoming compliance deadline with resource gaps",
        pain_category=PainPointCategory.DEADLINE_PRESSURE,
        required_signals=[
            DataSignalType.CERTIFICATION,
            DataSignalType.JOB_POSTING,
        ],
        optional_signals=[DataSignalType.TECH_STACK],
        scoring_weight=30,
    ),
    "growth_strain": PainQualifiedSegment(
        name="Rapid Growth Strain",
        description="Company experiencing growth with infrastructure gaps",
        pain_category=PainPointCategory.GROWTH_STRAIN,
        required_signals=[
            DataSignalType.FUNDING_EVENT,
            DataSignalType.EMPLOYEE_CHANGE,
        ],
        optional_signals=[DataSignalType.JOB_POSTING],
        scoring_weight=25,
    ),
    "technology_migration": PainQualifiedSegment(
        name="Technology Migration",
        description="Company with outdated tech stack showing modernization signals",
        pain_category=PainPointCategory.TECHNOLOGY_GAP,
        required_signals=[
            DataSignalType.TECH_STACK,
            DataSignalType.JOB_POSTING,
        ],
        optional_signals=[DataSignalType.REVIEW_SENTIMENT],
        scoring_weight=25,
    ),
}

# Pre-built common PVP templates
COMMON_PVP_TEMPLATES = {
    "tech_stack_audit": ValueProposition(
        name="Technology Stack Audit",
        description="Analysis of their public tech stack with gap identification",
        insight_type="audit",
        data_sources_required=["builtwith", "wappalyzer"],
        value_statement="Identify technology gaps affecting your operational efficiency",
        delivery_format="scorecard",
    ),
    "competitive_benchmark": ValueProposition(
        name="Competitive Benchmark",
        description="How they compare to similar companies in their space",
        insight_type="benchmark",
        data_sources_required=["linkedin_company", "crunchbase"],
        value_statement="See how your team structure compares to fast-growing peers",
        delivery_format="comparison",
    ),
    "compliance_readiness": ValueProposition(
        name="Compliance Readiness Assessment",
        description="Gap analysis against compliance requirements",
        insight_type="assessment",
        data_sources_required=["government_registry", "job_postings"],
        value_statement="Identify compliance gaps before your next audit",
        delivery_format="checklist",
    ),
}
