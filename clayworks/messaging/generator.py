"""
ClayWorks Message Generator Module
==================================

Generates personalized messages using templates and prospect data.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from .templates import (
    MessageTemplate,
    PQSTemplate,
    PVPTemplate,
    PQS_TEMPLATES,
    PVP_TEMPLATES,
)


@dataclass
class GeneratedMessage:
    """A generated message ready for delivery."""
    prospect_id: str
    template_name: str
    template_type: str  # pqs or pvp
    subject: str
    body: str
    channel: str
    personalization_data: Dict[str, Any]
    generated_at: datetime = field(default_factory=datetime.now)
    validation_warnings: List[str] = field(default_factory=list)
    confidence_score: float = 1.0

    @property
    def is_valid(self) -> bool:
        """Check if message passed validation."""
        return len(self.validation_warnings) == 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "prospect_id": self.prospect_id,
            "template_name": self.template_name,
            "template_type": self.template_type,
            "subject": self.subject,
            "body": self.body,
            "channel": self.channel,
            "generated_at": self.generated_at.isoformat(),
            "is_valid": self.is_valid,
            "validation_warnings": self.validation_warnings,
            "confidence_score": self.confidence_score,
        }


class MessageGenerator:
    """
    Message generation engine.

    Takes prospect data and templates to generate personalized messages
    following the PQS (Mirror-Insight-Ask) or PVP (Data Hook-Value-Action)
    frameworks.
    """

    def __init__(self):
        self.templates: Dict[str, MessageTemplate] = {}
        self._load_default_templates()

    def _load_default_templates(self) -> None:
        """Load default PQS and PVP templates."""
        for name, template in PQS_TEMPLATES.items():
            self.templates[f"pqs_{name}"] = template

        for name, template in PVP_TEMPLATES.items():
            self.templates[f"pvp_{name}"] = template

    def add_template(self, key: str, template: MessageTemplate) -> None:
        """Add a custom template."""
        self.templates[key] = template

    def get_template(self, key: str) -> Optional[MessageTemplate]:
        """Get a template by key."""
        return self.templates.get(key)

    def list_templates(self) -> Dict[str, List[str]]:
        """List all available templates by type."""
        pqs = [k.replace("pqs_", "") for k in self.templates.keys() if k.startswith("pqs_")]
        pvp = [k.replace("pvp_", "") for k in self.templates.keys() if k.startswith("pvp_")]
        custom = [k for k in self.templates.keys() if not k.startswith(("pqs_", "pvp_"))]
        return {"pqs": pqs, "pvp": pvp, "custom": custom}

    def generate(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_key: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> GeneratedMessage:
        """
        Generate a message for a prospect.

        Args:
            prospect_id: Unique identifier for the prospect
            prospect_data: Data about the prospect
            template_key: Key of the template to use
            additional_data: Additional data to merge with prospect data

        Returns:
            GeneratedMessage with rendered subject and body
        """
        template = self.get_template(template_key)
        if not template:
            raise ValueError(f"Template not found: {template_key}")

        # Merge data sources
        merged_data = {**prospect_data}
        if additional_data:
            merged_data.update(additional_data)

        # Validate required fields
        missing_fields = template.validate_data(merged_data)
        warnings = [f"Missing field: {f}" for f in missing_fields]

        # Calculate confidence based on data completeness
        total_fields = len(template.required_fields) + len(template.optional_fields)
        present_required = len(template.required_fields) - len(missing_fields)
        present_optional = sum(
            1 for f in template.optional_fields if f in merged_data
        )
        confidence = (present_required + present_optional * 0.5) / total_fields if total_fields > 0 else 1.0

        # Render the message
        rendered = template.render(merged_data)

        # Determine template type
        template_type = "pqs" if template_key.startswith("pqs_") else (
            "pvp" if template_key.startswith("pvp_") else "custom"
        )

        return GeneratedMessage(
            prospect_id=prospect_id,
            template_name=template_key,
            template_type=template_type,
            subject=rendered["subject"],
            body=rendered["body"],
            channel=template.channel,
            personalization_data=merged_data,
            validation_warnings=warnings,
            confidence_score=confidence,
        )

    def generate_pqs(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_name: str = "compliance_deadline",
    ) -> GeneratedMessage:
        """
        Generate a PQS (Pain-Qualified Segment) message.

        PQS Structure: Mirror-Insight-Ask
        """
        return self.generate(
            prospect_id=prospect_id,
            prospect_data=prospect_data,
            template_key=f"pqs_{template_name}",
        )

    def generate_pvp(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_name: str = "tech_stack_audit",
    ) -> GeneratedMessage:
        """
        Generate a PVP (Permissionless Value Proposition) message.

        PVP Structure: Data Hook-Value-Action
        """
        return self.generate(
            prospect_id=prospect_id,
            prospect_data=prospect_data,
            template_key=f"pvp_{template_name}",
        )

    def generate_batch(
        self,
        prospects: List[Dict[str, Any]],
        template_key: str,
        id_field: str = "id",
    ) -> List[GeneratedMessage]:
        """
        Generate messages for multiple prospects.

        Args:
            prospects: List of prospect data dictionaries
            template_key: Template to use for all prospects
            id_field: Field name containing prospect ID

        Returns:
            List of generated messages
        """
        messages = []
        for prospect in prospects:
            prospect_id = prospect.get(id_field, str(len(messages)))
            message = self.generate(
                prospect_id=prospect_id,
                prospect_data=prospect,
                template_key=template_key,
            )
            messages.append(message)
        return messages

    def select_best_template(
        self,
        prospect_data: Dict[str, Any],
        template_type: str = "pqs",
    ) -> str:
        """
        Select the best template for a prospect based on their data.

        Returns the template key with highest data coverage.
        """
        prefix = f"{template_type}_"
        candidate_templates = [
            k for k in self.templates.keys() if k.startswith(prefix)
        ]

        best_template = None
        best_score = -1

        for template_key in candidate_templates:
            template = self.templates[template_key]
            missing = template.validate_data(prospect_data)
            score = len(template.required_fields) - len(missing)

            if score > best_score:
                best_score = score
                best_template = template_key

        return best_template or f"{prefix}compliance_deadline"

    def create_ab_variants(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_key: str,
        variants: Dict[str, Dict[str, Any]],
    ) -> List[GeneratedMessage]:
        """
        Create A/B test variants of a message.

        Args:
            prospect_id: Prospect identifier
            prospect_data: Base prospect data
            template_key: Template to use
            variants: Dict of variant names to additional data

        Returns:
            List of message variants
        """
        messages = []
        for variant_name, variant_data in variants.items():
            merged = {**prospect_data, **variant_data, "variant": variant_name}
            message = self.generate(
                prospect_id=f"{prospect_id}__{variant_name}",
                prospect_data=merged,
                template_key=template_key,
            )
            messages.append(message)
        return messages

    def validate_message_quality(
        self, message: GeneratedMessage
    ) -> Dict[str, Any]:
        """
        Validate message quality and provide recommendations.

        Checks:
        - Subject line length
        - Body completeness
        - Personalization level
        - Data point specificity
        """
        issues = []
        recommendations = []

        # Check subject length
        subject_words = len(message.subject.split())
        if subject_words > 7:
            issues.append(f"Subject too long: {subject_words} words (aim for 3-5)")
            recommendations.append("Shorten subject to 3-5 words")

        # Check for placeholder text
        if "${" in message.body or "[" in message.body:
            issues.append("Contains unresolved placeholders")
            recommendations.append("Ensure all data fields are populated")

        # Check body length
        body_sentences = message.body.count(".") + message.body.count("?")
        if body_sentences > 6:
            issues.append(f"Body too long: {body_sentences} sentences (aim for 4-6)")
            recommendations.append("Condense message to 4-6 sentences")

        # Check personalization
        if message.confidence_score < 0.7:
            issues.append(f"Low personalization: {message.confidence_score:.0%}")
            recommendations.append("Add more specific data points")

        return {
            "is_quality": len(issues) == 0,
            "score": 1.0 - (len(issues) * 0.2),
            "issues": issues,
            "recommendations": recommendations,
        }
