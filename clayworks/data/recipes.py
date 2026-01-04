"""
ClayWorks Data Recipes Module
=============================

A Data Recipe is a specific combination of data sources that identifies
prospects at the exact moment they experience a verifiable pain point.

Recipe Construction Formula:
1. TARGET OUTCOME: What situation are we identifying?
2. DATA INGREDIENTS: Which sources provide which signals?
3. COMBINATION LOGIC: IF/AND/THEN rules for matching
4. SCORING MODEL: Point values for each signal
5. VALIDATION METHOD: Manual verification steps
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime
from enum import Enum
import json
import yaml


class ConditionOperator(Enum):
    """Operators for recipe conditions."""
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_OR_EQUAL = "greater_or_equal"
    LESS_OR_EQUAL = "less_or_equal"
    IN_LIST = "in_list"
    NOT_IN_LIST = "not_in_list"
    EXISTS = "exists"
    NOT_EXISTS = "not_exists"
    MATCHES_REGEX = "matches_regex"
    WITHIN_DAYS = "within_days"


@dataclass
class RecipeCondition:
    """A single condition in a recipe."""
    field: str
    operator: ConditionOperator
    value: Any
    source: Optional[str] = None  # Which data source provides this field

    def evaluate(self, data: Dict[str, Any]) -> bool:
        """Evaluate this condition against data."""
        field_value = data.get(self.field)

        if self.operator == ConditionOperator.EXISTS:
            return field_value is not None

        if self.operator == ConditionOperator.NOT_EXISTS:
            return field_value is None

        if field_value is None:
            return False

        if self.operator == ConditionOperator.EQUALS:
            return field_value == self.value

        if self.operator == ConditionOperator.NOT_EQUALS:
            return field_value != self.value

        if self.operator == ConditionOperator.CONTAINS:
            return self.value in str(field_value)

        if self.operator == ConditionOperator.NOT_CONTAINS:
            return self.value not in str(field_value)

        if self.operator == ConditionOperator.GREATER_THAN:
            return field_value > self.value

        if self.operator == ConditionOperator.LESS_THAN:
            return field_value < self.value

        if self.operator == ConditionOperator.GREATER_OR_EQUAL:
            return field_value >= self.value

        if self.operator == ConditionOperator.LESS_OR_EQUAL:
            return field_value <= self.value

        if self.operator == ConditionOperator.IN_LIST:
            return field_value in self.value

        if self.operator == ConditionOperator.NOT_IN_LIST:
            return field_value not in self.value

        if self.operator == ConditionOperator.WITHIN_DAYS:
            if isinstance(field_value, datetime):
                days_ago = (datetime.now() - field_value).days
                return days_ago <= self.value

        return False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "field": self.field,
            "operator": self.operator.value,
            "value": self.value,
            "source": self.source,
        }


@dataclass
class DataIngredient:
    """A data ingredient in a recipe."""
    source: str
    data_point: str
    signal_description: str
    required: bool = True
    fallback_sources: List[str] = field(default_factory=list)


@dataclass
class ScoringComponent:
    """A scoring component in a recipe."""
    name: str
    description: str
    points: int
    weight_percentage: float
    condition: RecipeCondition


@dataclass
class ValidationStep:
    """A manual validation step."""
    description: str
    verification_method: str
    required: bool = True


@dataclass
class DataRecipe:
    """
    A complete Data Recipe definition.

    A recipe identifies prospects at the exact moment they experience
    a verifiable pain point by combining multiple data signals.
    """
    name: str
    description: str
    target_outcome: str
    target_persona: str
    target_company_type: str
    timeframe: str

    # Data ingredients from various sources
    ingredients: List[DataIngredient]

    # Combination logic (all conditions that must be met)
    required_conditions: List[RecipeCondition]
    optional_conditions: List[RecipeCondition] = field(default_factory=list)

    # Scoring model
    scoring_components: List[ScoringComponent] = field(default_factory=list)
    score_threshold: int = 70

    # Validation steps before outreach
    validation_steps: List[ValidationStep] = field(default_factory=list)

    # Output configuration
    output_segment: str = ""
    output_sequence: str = ""

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    author: str = ""

    def evaluate(self, prospect_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a prospect against this recipe.

        Returns:
            Dictionary with match status, score, and details
        """
        # Check required conditions
        required_met = all(
            cond.evaluate(prospect_data) for cond in self.required_conditions
        )

        if not required_met:
            return {
                "matches": False,
                "reason": "Required conditions not met",
                "score": 0,
                "threshold": self.score_threshold,
            }

        # Check optional conditions and calculate score
        optional_met = [
            cond for cond in self.optional_conditions
            if cond.evaluate(prospect_data)
        ]

        # Calculate total score
        total_score = 0
        scoring_details = []

        for component in self.scoring_components:
            if component.condition.evaluate(prospect_data):
                total_score += component.points
                scoring_details.append({
                    "component": component.name,
                    "points": component.points,
                })

        qualifies = total_score >= self.score_threshold

        return {
            "matches": qualifies,
            "score": total_score,
            "threshold": self.score_threshold,
            "required_conditions_met": True,
            "optional_conditions_met": len(optional_met),
            "scoring_details": scoring_details,
            "output_segment": self.output_segment if qualifies else None,
        }

    def get_required_sources(self) -> List[str]:
        """Get list of data sources required for this recipe."""
        sources = set()
        for ingredient in self.ingredients:
            if ingredient.required:
                sources.add(ingredient.source)
        for condition in self.required_conditions:
            if condition.source:
                sources.add(condition.source)
        return list(sources)

    def to_dict(self) -> Dict[str, Any]:
        """Convert recipe to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "target_outcome": self.target_outcome,
            "target_persona": self.target_persona,
            "target_company_type": self.target_company_type,
            "timeframe": self.timeframe,
            "ingredients": [
                {
                    "source": i.source,
                    "data_point": i.data_point,
                    "signal_description": i.signal_description,
                    "required": i.required,
                }
                for i in self.ingredients
            ],
            "required_conditions": [c.to_dict() for c in self.required_conditions],
            "optional_conditions": [c.to_dict() for c in self.optional_conditions],
            "scoring_components": [
                {
                    "name": s.name,
                    "description": s.description,
                    "points": s.points,
                    "weight_percentage": s.weight_percentage,
                    "condition": s.condition.to_dict(),
                }
                for s in self.scoring_components
            ],
            "score_threshold": self.score_threshold,
            "validation_steps": [
                {"description": v.description, "verification_method": v.verification_method}
                for v in self.validation_steps
            ],
            "output_segment": self.output_segment,
            "version": self.version,
        }

    def to_yaml(self) -> str:
        """Export recipe as YAML."""
        return yaml.dump(self.to_dict(), default_flow_style=False)


class DataRecipeBuilder:
    """
    Builder for creating and managing Data Recipes.

    Usage:
        builder = DataRecipeBuilder()
        recipe = (builder
            .name("Compliance Deadline Collision")
            .target_outcome("Companies facing compliance deadline with gaps")
            .add_ingredient("sam_gov", "contract_deadline", "Government contract deadline")
            .add_condition("days_to_deadline", ConditionOperator.LESS_THAN, 90)
            .add_scoring("deadline_urgency", 30, "Deadline within 90 days")
            .build())
    """

    def __init__(self):
        self._reset()

    def _reset(self) -> None:
        """Reset builder state."""
        self._name: str = ""
        self._description: str = ""
        self._target_outcome: str = ""
        self._target_persona: str = ""
        self._target_company_type: str = ""
        self._timeframe: str = ""
        self._ingredients: List[DataIngredient] = []
        self._required_conditions: List[RecipeCondition] = []
        self._optional_conditions: List[RecipeCondition] = []
        self._scoring_components: List[ScoringComponent] = []
        self._score_threshold: int = 70
        self._validation_steps: List[ValidationStep] = []
        self._output_segment: str = ""
        self._output_sequence: str = ""

    def name(self, name: str) -> "DataRecipeBuilder":
        """Set recipe name."""
        self._name = name
        return self

    def description(self, description: str) -> "DataRecipeBuilder":
        """Set recipe description."""
        self._description = description
        return self

    def target_outcome(self, outcome: str) -> "DataRecipeBuilder":
        """Set target outcome."""
        self._target_outcome = outcome
        return self

    def target_persona(self, persona: str) -> "DataRecipeBuilder":
        """Set target persona."""
        self._target_persona = persona
        return self

    def target_company_type(self, company_type: str) -> "DataRecipeBuilder":
        """Set target company type."""
        self._target_company_type = company_type
        return self

    def timeframe(self, timeframe: str) -> "DataRecipeBuilder":
        """Set timeframe."""
        self._timeframe = timeframe
        return self

    def add_ingredient(
        self,
        source: str,
        data_point: str,
        signal_description: str,
        required: bool = True,
    ) -> "DataRecipeBuilder":
        """Add a data ingredient."""
        self._ingredients.append(DataIngredient(
            source=source,
            data_point=data_point,
            signal_description=signal_description,
            required=required,
        ))
        return self

    def add_condition(
        self,
        field: str,
        operator: ConditionOperator,
        value: Any,
        source: Optional[str] = None,
        required: bool = True,
    ) -> "DataRecipeBuilder":
        """Add a condition."""
        condition = RecipeCondition(
            field=field,
            operator=operator,
            value=value,
            source=source,
        )
        if required:
            self._required_conditions.append(condition)
        else:
            self._optional_conditions.append(condition)
        return self

    def add_scoring(
        self,
        name: str,
        points: int,
        description: str,
        field: str,
        operator: ConditionOperator,
        value: Any,
        weight_percentage: float = 0,
    ) -> "DataRecipeBuilder":
        """Add a scoring component."""
        condition = RecipeCondition(field=field, operator=operator, value=value)
        self._scoring_components.append(ScoringComponent(
            name=name,
            description=description,
            points=points,
            weight_percentage=weight_percentage,
            condition=condition,
        ))
        return self

    def score_threshold(self, threshold: int) -> "DataRecipeBuilder":
        """Set score threshold."""
        self._score_threshold = threshold
        return self

    def add_validation_step(
        self, description: str, verification_method: str, required: bool = True
    ) -> "DataRecipeBuilder":
        """Add a validation step."""
        self._validation_steps.append(ValidationStep(
            description=description,
            verification_method=verification_method,
            required=required,
        ))
        return self

    def output(self, segment: str, sequence: str = "") -> "DataRecipeBuilder":
        """Set output segment and sequence."""
        self._output_segment = segment
        self._output_sequence = sequence
        return self

    def build(self) -> DataRecipe:
        """Build the recipe."""
        recipe = DataRecipe(
            name=self._name,
            description=self._description,
            target_outcome=self._target_outcome,
            target_persona=self._target_persona,
            target_company_type=self._target_company_type,
            timeframe=self._timeframe,
            ingredients=self._ingredients,
            required_conditions=self._required_conditions,
            optional_conditions=self._optional_conditions,
            scoring_components=self._scoring_components,
            score_threshold=self._score_threshold,
            validation_steps=self._validation_steps,
            output_segment=self._output_segment,
            output_sequence=self._output_sequence,
        )
        self._reset()
        return recipe


# Example recipe templates
def create_deadline_collision_recipe() -> DataRecipe:
    """Create a Deadline Collision recipe template."""
    builder = DataRecipeBuilder()
    return (builder
        .name("Deadline Collision")
        .description("Companies facing deadline pressure with resource/capability gaps")
        .target_outcome("Identify companies with upcoming compliance or contract deadlines that show hiring or technology gaps")
        .target_persona("VP of Ops, CISO, Compliance Lead")
        .target_company_type("Mid-market companies with government contracts or compliance requirements")
        .timeframe("Deadline within 90 days")
        .add_ingredient("sam_gov", "contract_deadline", "Government contract with upcoming deadline")
        .add_ingredient("linkedin_jobs", "compliance_roles", "Posted compliance-related job in last 30 days")
        .add_ingredient("builtwith", "tech_stack", "Current technology stack")
        .add_condition("days_to_deadline", ConditionOperator.LESS_THAN, 90, "sam_gov")
        .add_condition("has_relevant_posting", ConditionOperator.EQUALS, True, "linkedin_jobs")
        .add_condition("employee_count", ConditionOperator.GREATER_THAN, 50)
        .add_scoring("deadline_urgency", 30, "Deadline urgency", "days_to_deadline", ConditionOperator.LESS_THAN, 60)
        .add_scoring("hiring_signal", 25, "Recent hiring signal", "posting_age_days", ConditionOperator.LESS_THAN, 14)
        .add_scoring("tech_gap", 25, "Technology gap identified", "has_tech_gap", ConditionOperator.EQUALS, True)
        .add_scoring("company_fit", 20, "Company size fit", "employee_count", ConditionOperator.GREATER_THAN, 100)
        .score_threshold(70)
        .add_validation_step("Verify deadline date in SAM.gov", "Manual check of contract record")
        .add_validation_step("Confirm job posting is still active", "Visit LinkedIn job page")
        .output("deadline_pressure_segment", "urgent_deadline_sequence")
        .build())


def create_growth_pressure_recipe() -> DataRecipe:
    """Create a Growth Pressure recipe template."""
    builder = DataRecipeBuilder()
    return (builder
        .name("Growth Pressure")
        .description("Companies with recent funding experiencing rapid growth strain")
        .target_outcome("Identify recently funded companies with hiring surge and infrastructure gaps")
        .target_persona("VP of Engineering, CTO, Head of Operations")
        .target_company_type("Series A-C startups in growth phase")
        .timeframe("Funding within last 6 months")
        .add_ingredient("crunchbase", "funding_round", "Recent funding event")
        .add_ingredient("linkedin_company", "employee_growth", "Employee count growth")
        .add_ingredient("linkedin_jobs", "open_roles", "Current open positions")
        .add_condition("months_since_funding", ConditionOperator.LESS_THAN, 6, "crunchbase")
        .add_condition("employee_growth_rate", ConditionOperator.GREATER_THAN, 0.2, "linkedin_company")
        .add_condition("open_positions", ConditionOperator.GREATER_THAN, 5, "linkedin_jobs")
        .add_scoring("funding_recency", 30, "Recent funding", "months_since_funding", ConditionOperator.LESS_THAN, 3)
        .add_scoring("growth_rate", 25, "High growth rate", "employee_growth_rate", ConditionOperator.GREATER_THAN, 0.3)
        .add_scoring("hiring_volume", 25, "Aggressive hiring", "open_positions", ConditionOperator.GREATER_THAN, 10)
        .add_scoring("funding_size", 20, "Significant funding", "funding_amount", ConditionOperator.GREATER_THAN, 10000000)
        .score_threshold(70)
        .add_validation_step("Verify funding announcement", "Check Crunchbase or press release")
        .add_validation_step("Confirm employee count trend", "Review LinkedIn company page")
        .output("growth_pressure_segment", "growth_support_sequence")
        .build())
