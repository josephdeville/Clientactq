"""
ClayWorks Message Templates Module
==================================

PQS Message Structure (Mirror-Insight-Ask):
1. MIRROR: State verifiable data point reflecting their specific situation
2. INSIGHT: Share non-obvious pattern from peer companies
3. ASK: Low-friction question inviting dialogue

PVP Message Structure (Data Hook-Value-Action):
1. DATA HOOK: Lead with specific, quantified finding about their situation
2. VALUE: Explain why this matters NOW and what peer companies did
3. ACTION: Offer more value (not a meeting)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from string import Template
import re


@dataclass
class MessageTemplate:
    """Base class for message templates."""
    name: str
    description: str
    subject_template: str
    body_template: str
    required_fields: List[str] = field(default_factory=list)
    optional_fields: List[str] = field(default_factory=list)
    max_subject_words: int = 5
    channel: str = "email"  # email, linkedin, etc.

    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate that all required fields are present."""
        missing = [f for f in self.required_fields if f not in data or not data[f]]
        return missing

    def render_subject(self, data: Dict[str, Any]) -> str:
        """Render the subject line."""
        template = Template(self.subject_template)
        try:
            return template.safe_substitute(data)
        except Exception:
            return self.subject_template

    def render_body(self, data: Dict[str, Any]) -> str:
        """Render the message body."""
        template = Template(self.body_template)
        try:
            return template.safe_substitute(data)
        except Exception:
            return self.body_template

    def render(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Render both subject and body."""
        return {
            "subject": self.render_subject(data),
            "body": self.render_body(data),
        }


@dataclass
class PQSTemplate(MessageTemplate):
    """
    Pain-Qualified Segment (PQS) Message Template.

    Structure: Mirror-Insight-Ask

    The goal is to make prospects think:
    "How did they know we're dealing with exactly this?"
    """
    mirror_template: str = ""
    insight_template: str = ""
    ask_template: str = ""

    def __post_init__(self):
        """Initialize default required fields for PQS."""
        if not self.required_fields:
            self.required_fields = [
                "observable_data_point_1",
                "observable_data_point_2",
                "logical_inference",
                "peer_companies",
                "common_approach",
                "desired_outcome",
                "specific_tactic",
                "quantified_result",
                "costly_mistake",
                "problem_symptom",
            ]

    def render_mirror(self, data: Dict[str, Any]) -> str:
        """Render the mirror sentence."""
        if self.mirror_template:
            return Template(self.mirror_template).safe_substitute(data)
        return (
            f"Your {data.get('observable_data_point_1', '[data point]')} "
            f"{data.get('combined_with', 'combined with')} "
            f"{data.get('observable_data_point_2', '[data point 2]')} "
            f"suggests you're {data.get('logical_inference', '[inference]')}."
        )

    def render_insight(self, data: Dict[str, Any]) -> str:
        """Render the insight sentences."""
        if self.insight_template:
            return Template(self.insight_template).safe_substitute(data)
        return (
            f"Most {data.get('peer_companies', '[similar companies]')} initially try "
            f"{data.get('common_approach', '[common approach]')}—but the ones who "
            f"{data.get('desired_outcome', '[achieved outcome]')} discovered that "
            f"{data.get('specific_tactic', '[specific tactic]')} "
            f"{data.get('quantified_result', '[result]')}. "
            f"They avoided {data.get('costly_mistake', '[costly mistake]')}."
        )

    def render_ask(self, data: Dict[str, Any]) -> str:
        """Render the ask question."""
        if self.ask_template:
            return Template(self.ask_template).safe_substitute(data)
        return f"Curious if you're seeing {data.get('problem_symptom', '[specific symptom]')}?"

    def render_body(self, data: Dict[str, Any]) -> str:
        """Render the complete PQS message body."""
        if self.body_template:
            return Template(self.body_template).safe_substitute(data)

        mirror = self.render_mirror(data)
        insight = self.render_insight(data)
        ask = self.render_ask(data)

        return f"{mirror}\n\n{insight}\n\n{ask}"


@dataclass
class PVPTemplate(MessageTemplate):
    """
    Permissionless Value Proposition (PVP) Message Template.

    Structure: Data Hook-Value-Action

    Test: "Would they literally pay for this insight?"
    """
    data_hook_template: str = ""
    value_template: str = ""
    action_template: str = ""

    def __post_init__(self):
        """Initialize default required fields for PVP."""
        if not self.required_fields:
            self.required_fields = [
                "public_data_source",
                "quantified_finding",
                "specific_examples",
                "external_pressure",
                "consequence",
                "peer_companies",
                "specific_outcome",
                "specific_approach",
                "analysis_type",
                "specific_scope",
            ]

    def render_data_hook(self, data: Dict[str, Any]) -> str:
        """Render the data hook paragraph."""
        if self.data_hook_template:
            return Template(self.data_hook_template).safe_substitute(data)
        return (
            f"Analysis of your {data.get('public_data_source', '[data source]')} "
            f"shows {data.get('quantified_finding', '[finding]')}—"
            f"{data.get('specific_examples', '[specific examples]')}."
        )

    def render_value(self, data: Dict[str, Any]) -> str:
        """Render the value paragraph."""
        if self.value_template:
            return Template(self.value_template).safe_substitute(data)
        return (
            f"With {data.get('external_pressure', '[external pressure]')}, "
            f"{data.get('consequence', '[consequence]')}. "
            f"{data.get('peer_companies', '[Peer companies]')} who "
            f"{data.get('addressed_proactively', 'addressed this proactively')} "
            f"{data.get('specific_outcome', '[achieved outcome]')} by "
            f"{data.get('specific_approach', '[specific approach]')}."
        )

    def render_action(self, data: Dict[str, Any]) -> str:
        """Render the action offer."""
        if self.action_template:
            return Template(self.action_template).safe_substitute(data)
        return (
            f"Want the {data.get('analysis_type', 'complete')} "
            f"{data.get('deliverable_type', 'analysis')} for your "
            f"{data.get('specific_scope', '[scope]')}?"
        )

    def render_body(self, data: Dict[str, Any]) -> str:
        """Render the complete PVP message body."""
        if self.body_template:
            return Template(self.body_template).safe_substitute(data)

        data_hook = self.render_data_hook(data)
        value = self.render_value(data)
        action = self.render_action(data)

        return f"{data_hook}\n\n{value}\n\n{action}"


# Pre-built PQS templates
PQS_TEMPLATES = {
    "compliance_deadline": PQSTemplate(
        name="Compliance Deadline PQS",
        description="For companies facing compliance deadlines with resource gaps",
        subject_template="${deadline_name} by ${deadline_date}",
        body_template="",
        mirror_template=(
            "Your ${certification_requirement} combined with your recent "
            "${job_posting_type} posting suggests you're building compliance "
            "capability under deadline pressure."
        ),
        insight_template=(
            "Most ${industry} companies in this position initially try "
            "hiring internally—but the ones who achieved ${certification} "
            "on schedule discovered that ${approach} reduced timeline by "
            "${time_saved}. They avoided ${common_mistake}."
        ),
        ask_template="Curious if you're seeing ${specific_challenge}?",
    ),
    "growth_strain": PQSTemplate(
        name="Growth Strain PQS",
        description="For rapidly growing companies with infrastructure gaps",
        subject_template="Scaling ${function} after Series ${funding_round}",
        body_template="",
        mirror_template=(
            "Your ${funding_amount} ${funding_round} combined with "
            "${employee_growth_stat} suggests you're scaling faster "
            "than your infrastructure."
        ),
        insight_template=(
            "Most post-${funding_round} startups initially try "
            "${common_first_approach}—but the ones who scaled "
            "efficiently discovered that ${specific_approach} "
            "${quantified_benefit}. They avoided ${scaling_mistake}."
        ),
        ask_template="Curious if ${infrastructure_challenge} is showing up?",
    ),
    "technology_migration": PQSTemplate(
        name="Technology Migration PQS",
        description="For companies showing technology modernization signals",
        subject_template="${legacy_tech} migration timeline",
        body_template="",
        mirror_template=(
            "Your ${current_tech_stack} combined with your "
            "${modernization_signal} suggests you're evaluating "
            "a technology transition."
        ),
        insight_template=(
            "Most ${company_type} companies initially try "
            "${common_migration_approach}—but the ones who completed "
            "migration successfully discovered that ${better_approach} "
            "${outcome}. They avoided ${migration_pitfall}."
        ),
        ask_template="Curious if ${migration_concern} is on your radar?",
    ),
}

# Pre-built PVP templates
PVP_TEMPLATES = {
    "tech_stack_audit": PVPTemplate(
        name="Tech Stack Audit PVP",
        description="Technology gap analysis based on public data",
        subject_template="Your ${company_name} tech infrastructure gaps",
        body_template="",
        data_hook_template=(
            "Analysis of your public tech stack shows ${gap_count} "
            "potential efficiency gaps—specifically in ${gap_areas}."
        ),
        value_template=(
            "With ${growth_pressure}, these gaps typically lead to "
            "${consequence}. Similar ${company_type} companies who "
            "addressed these proactively ${outcome}."
        ),
        action_template=(
            "Want the complete infrastructure assessment for ${company_name}?"
        ),
    ),
    "competitive_benchmark": PVPTemplate(
        name="Competitive Benchmark PVP",
        description="Competitive positioning analysis",
        subject_template="${company_name} vs. ${competitor_count} competitors",
        body_template="",
        data_hook_template=(
            "Competitive analysis shows ${company_name} ${competitive_position}—"
            "including ${specific_comparison_points}."
        ),
        value_template=(
            "With ${market_pressure}, ${implication}. "
            "Companies who ${action_taken} saw ${result}."
        ),
        action_template="Want the full competitive breakdown?",
    ),
    "compliance_gap": PVPTemplate(
        name="Compliance Gap PVP",
        description="Compliance readiness assessment",
        subject_template="${compliance_framework} gaps at ${company_name}",
        body_template="",
        data_hook_template=(
            "Analysis of your ${public_indicators} shows ${gap_count} "
            "potential ${compliance_framework} gaps—including ${specific_gaps}."
        ),
        value_template=(
            "With ${deadline_or_requirement}, you'll need to "
            "${required_action}. Organizations who ${proactive_action} "
            "${outcome}."
        ),
        action_template=(
            "Want the detailed ${compliance_framework} readiness checklist?"
        ),
    ),
}


def get_pqs_template(name: str) -> Optional[PQSTemplate]:
    """Get a pre-built PQS template by name."""
    return PQS_TEMPLATES.get(name)


def get_pvp_template(name: str) -> Optional[PVPTemplate]:
    """Get a pre-built PVP template by name."""
    return PVP_TEMPLATES.get(name)


def list_templates() -> Dict[str, List[str]]:
    """List all available templates."""
    return {
        "pqs": list(PQS_TEMPLATES.keys()),
        "pvp": list(PVP_TEMPLATES.keys()),
    }
