"""
ClayWorks Personalization Engine Module
=======================================

Advanced personalization capabilities for creating hyper-relevant messages
that reflect each prospect's specific situation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import re


@dataclass
class PersonalizationField:
    """Definition of a personalization field."""
    name: str
    description: str
    data_source: str
    transform: Optional[Callable[[Any], str]] = None
    fallback: str = ""
    priority: int = 1  # Higher = more important


@dataclass
class PersonalizationContext:
    """Context for personalizing a message."""
    prospect_id: str
    company_data: Dict[str, Any]
    contact_data: Dict[str, Any]
    signal_data: Dict[str, Any]
    custom_data: Dict[str, Any] = field(default_factory=dict)

    @property
    def all_data(self) -> Dict[str, Any]:
        """Get all data merged."""
        return {
            **self.company_data,
            **self.contact_data,
            **self.signal_data,
            **self.custom_data,
        }


class PersonalizationEngine:
    """
    Engine for creating deeply personalized messages.

    Personalization Levels:
    1. Basic: Name, company, title
    2. Contextual: Industry, size, stage, location
    3. Signal-based: Recent events, hiring, funding, tech changes
    4. Insight-based: Peer comparisons, benchmarks, specific findings
    """

    def __init__(self):
        self.fields: Dict[str, PersonalizationField] = {}
        self._transformers: Dict[str, Callable] = {}
        self._load_default_fields()

    def _load_default_fields(self) -> None:
        """Load default personalization fields."""
        defaults = [
            # Basic personalization
            PersonalizationField(
                name="first_name",
                description="Contact's first name",
                data_source="contact",
                priority=1,
            ),
            PersonalizationField(
                name="company_name",
                description="Company name",
                data_source="company",
                priority=1,
            ),
            PersonalizationField(
                name="title",
                description="Contact's job title",
                data_source="contact",
                priority=1,
            ),

            # Contextual personalization
            PersonalizationField(
                name="industry",
                description="Company industry",
                data_source="company",
                priority=2,
            ),
            PersonalizationField(
                name="employee_count",
                description="Number of employees",
                data_source="company",
                transform=lambda x: f"{x:,}" if isinstance(x, int) else str(x),
                priority=2,
            ),
            PersonalizationField(
                name="funding_stage",
                description="Current funding stage",
                data_source="company",
                priority=2,
            ),

            # Signal-based personalization
            PersonalizationField(
                name="recent_job_posting",
                description="Most relevant recent job posting",
                data_source="signals",
                priority=3,
            ),
            PersonalizationField(
                name="funding_amount",
                description="Recent funding amount",
                data_source="signals",
                transform=lambda x: f"${x/1_000_000:.1f}M" if x >= 1_000_000 else f"${x:,}",
                priority=3,
            ),
            PersonalizationField(
                name="tech_stack_item",
                description="Notable technology in stack",
                data_source="signals",
                priority=3,
            ),

            # Insight-based personalization
            PersonalizationField(
                name="peer_company_example",
                description="Similar company as example",
                data_source="insights",
                priority=4,
            ),
            PersonalizationField(
                name="benchmark_stat",
                description="Relevant benchmark statistic",
                data_source="insights",
                priority=4,
            ),
            PersonalizationField(
                name="specific_finding",
                description="Specific data finding about them",
                data_source="insights",
                priority=4,
            ),
        ]

        for field in defaults:
            self.fields[field.name] = field

    def add_field(self, field: PersonalizationField) -> None:
        """Add a custom personalization field."""
        self.fields[field.name] = field

    def register_transformer(
        self, name: str, transformer: Callable[[Any], str]
    ) -> None:
        """Register a custom data transformer."""
        self._transformers[name] = transformer

    def get_personalization_level(
        self, context: PersonalizationContext
    ) -> Dict[str, Any]:
        """
        Analyze the personalization level possible with given data.

        Returns level (1-4) and available fields by priority.
        """
        all_data = context.all_data
        available_by_priority: Dict[int, List[str]] = {1: [], 2: [], 3: [], 4: []}

        for field_name, field in self.fields.items():
            if field_name in all_data and all_data[field_name]:
                available_by_priority[field.priority].append(field_name)

        # Determine level based on highest priority with data
        level = 1
        for priority in [4, 3, 2, 1]:
            if available_by_priority[priority]:
                level = priority
                break

        level_names = {
            1: "basic",
            2: "contextual",
            3: "signal_based",
            4: "insight_based",
        }

        return {
            "level": level,
            "level_name": level_names[level],
            "available_fields": available_by_priority,
            "total_fields": sum(len(v) for v in available_by_priority.values()),
        }

    def personalize(
        self,
        template: str,
        context: PersonalizationContext,
    ) -> str:
        """
        Personalize a template string with context data.

        Supports ${field_name} syntax for field substitution.
        """
        all_data = context.all_data
        result = template

        # Find all ${field_name} patterns
        pattern = r"\$\{(\w+)\}"
        matches = re.findall(pattern, template)

        for field_name in matches:
            value = all_data.get(field_name)
            field_def = self.fields.get(field_name)

            if value is not None:
                # Apply transform if defined
                if field_def and field_def.transform:
                    try:
                        value = field_def.transform(value)
                    except Exception:
                        value = str(value)
                else:
                    value = str(value)
            elif field_def:
                value = field_def.fallback
            else:
                value = f"[{field_name}]"

            result = result.replace(f"${{{field_name}}}", value)

        return result

    def build_context(
        self,
        prospect_id: str,
        company: Dict[str, Any],
        contact: Dict[str, Any],
        signals: Dict[str, Any],
        custom: Optional[Dict[str, Any]] = None,
    ) -> PersonalizationContext:
        """Build a personalization context from data sources."""
        return PersonalizationContext(
            prospect_id=prospect_id,
            company_data=company,
            contact_data=contact,
            signal_data=signals,
            custom_data=custom or {},
        )

    def generate_mirror_statement(
        self, context: PersonalizationContext
    ) -> str:
        """
        Generate a mirror statement for PQS messages.

        The "Mirror Effect": Reflect their exact situation back to them
        with such accuracy they feel seen.
        """
        data = context.all_data

        # Build mirror statement from available signals
        observations = []

        if data.get("recent_job_posting"):
            observations.append(f"your recent {data['recent_job_posting']} posting")

        if data.get("funding_amount"):
            field = self.fields.get("funding_amount")
            formatted = field.transform(data["funding_amount"]) if field and field.transform else str(data["funding_amount"])
            observations.append(f"your recent {formatted} raise")

        if data.get("employee_growth_rate"):
            rate = data["employee_growth_rate"]
            observations.append(f"your {rate:.0%} team growth this year")

        if data.get("tech_stack_item"):
            observations.append(f"your use of {data['tech_stack_item']}")

        if len(observations) >= 2:
            return f"Your {observations[0]} combined with {observations[1]}"
        elif observations:
            return f"Your {observations[0]}"
        else:
            return "Based on our analysis"

    def generate_peer_insight(
        self,
        context: PersonalizationContext,
        insight_data: Dict[str, Any],
    ) -> str:
        """
        Generate a peer insight statement for PQS messages.

        This provides the non-obvious pattern from peer companies.
        """
        data = context.all_data

        peer_type = data.get("industry", "similar companies")
        common_approach = insight_data.get("common_approach", "the traditional approach")
        better_approach = insight_data.get("better_approach", "a different strategy")
        outcome = insight_data.get("outcome", "better results")

        return (
            f"Most {peer_type} in this position initially try {common_approach}—"
            f"but the ones who succeeded discovered that {better_approach} "
            f"led to {outcome}."
        )

    def generate_value_hook(
        self,
        context: PersonalizationContext,
        finding: Dict[str, Any],
    ) -> str:
        """
        Generate a data hook statement for PVP messages.

        Leads with specific, quantified finding about their situation.
        """
        data = context.all_data
        company = data.get("company_name", "your company")

        finding_type = finding.get("type", "analysis")
        metric = finding.get("metric", "data")
        value = finding.get("value", "insights")
        specifics = finding.get("specifics", "")

        hook = f"Analysis of {company}'s {finding_type} shows {metric}: {value}"
        if specifics:
            hook += f"—{specifics}"

        return hook

    def calculate_personalization_score(
        self, context: PersonalizationContext
    ) -> float:
        """
        Calculate a 0-1 personalization score based on data richness.

        Higher scores indicate more personalized messages are possible.
        """
        all_data = context.all_data
        total_weight = 0
        achieved_weight = 0

        for field_name, field in self.fields.items():
            weight = field.priority
            total_weight += weight

            if field_name in all_data and all_data[field_name]:
                achieved_weight += weight

        return achieved_weight / total_weight if total_weight > 0 else 0

    def get_missing_high_value_fields(
        self, context: PersonalizationContext
    ) -> List[PersonalizationField]:
        """
        Get high-value fields that are missing from the context.

        These are fields that would significantly improve personalization.
        """
        all_data = context.all_data
        missing = []

        for field_name, field in self.fields.items():
            if field.priority >= 3 and field_name not in all_data:
                missing.append(field)

        # Sort by priority descending
        missing.sort(key=lambda f: f.priority, reverse=True)
        return missing
