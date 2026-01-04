"""
ClayWorks Recipe Development Phase Module
==========================================

Phase 2: Recipe Development

OBJECTIVES:
- Create initial PQS and PVP data recipes
- Manually execute recipes for test prospects
- Hand-craft messages and validate response rates
- Establish baseline metrics

DELIVERABLES:
- 2-3 data recipes documented with full logic
- 25 test prospects per recipe (manually researched)
- Hand-crafted messages for each prospect
- Response rate data (target: 15%+ validates concept)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class RecipeStatus(Enum):
    """Status of a data recipe."""
    DRAFT = "draft"
    TESTING = "testing"
    VALIDATED = "validated"
    FAILED = "failed"


class ProspectStatus(Enum):
    """Status of a test prospect."""
    RESEARCHED = "researched"
    MESSAGED = "messaged"
    RESPONDED = "responded"
    MEETING_BOOKED = "meeting_booked"
    NO_RESPONSE = "no_response"


@dataclass
class TestProspect:
    """A prospect being tested in recipe development."""
    prospect_id: str
    company_name: str
    contact_name: str
    contact_email: str
    recipe_name: str
    research_data: Dict[str, Any] = field(default_factory=dict)
    message_subject: str = ""
    message_body: str = ""
    status: ProspectStatus = ProspectStatus.RESEARCHED
    sent_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    responded_at: Optional[datetime] = None
    response_sentiment: str = ""  # positive, negative, neutral
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prospect_id": self.prospect_id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "recipe_name": self.recipe_name,
            "status": self.status.value,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
            "responded_at": self.responded_at.isoformat() if self.responded_at else None,
            "response_sentiment": self.response_sentiment,
        }


@dataclass
class RecipeTest:
    """A test run of a data recipe."""
    recipe_name: str
    recipe_type: str  # pqs or pvp
    recipe_logic: Dict[str, Any]
    status: RecipeStatus = RecipeStatus.DRAFT
    prospects: List[TestProspect] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def total_prospects(self) -> int:
        return len(self.prospects)

    @property
    def messaged_count(self) -> int:
        return sum(
            1 for p in self.prospects
            if p.status != ProspectStatus.RESEARCHED
        )

    @property
    def response_count(self) -> int:
        return sum(
            1 for p in self.prospects
            if p.status in [ProspectStatus.RESPONDED, ProspectStatus.MEETING_BOOKED]
        )

    @property
    def meeting_count(self) -> int:
        return sum(
            1 for p in self.prospects
            if p.status == ProspectStatus.MEETING_BOOKED
        )

    @property
    def response_rate(self) -> float:
        if self.messaged_count == 0:
            return 0.0
        return self.response_count / self.messaged_count

    @property
    def positive_response_count(self) -> int:
        return sum(
            1 for p in self.prospects
            if p.response_sentiment == "positive"
        )


class RecipeDevPhase:
    """
    Phase 2: Recipe Development

    Activities:
    Week 3:
    - Build Recipe 1: [Primary pain point segment]
    - Build Recipe 2: [Secondary pain point segment]
    - Manual research: 25 prospects per recipe
    - Draft messages using PQS/PVP templates

    Week 4:
    - Send test messages (personal email, not automation)
    - Track opens, replies, meeting conversions
    - Document message refinements based on responses
    - Identify highest-performing recipe/message combinations
    """

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # Recipe tests
        self.recipe_tests: List[RecipeTest] = []

        # Message refinements
        self.message_refinements: List[Dict[str, Any]] = []

        # Best performing combinations
        self.top_performers: List[Dict[str, Any]] = []

    def start(self) -> None:
        """Start the recipe development phase."""
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark the phase as complete."""
        self.completed_at = datetime.now()

    def create_recipe_test(
        self,
        recipe_name: str,
        recipe_type: str,
        recipe_logic: Dict[str, Any],
    ) -> RecipeTest:
        """Create a new recipe test."""
        test = RecipeTest(
            recipe_name=recipe_name,
            recipe_type=recipe_type,
            recipe_logic=recipe_logic,
        )
        self.recipe_tests.append(test)
        return test

    def add_prospect(
        self,
        recipe_name: str,
        prospect: TestProspect,
    ) -> None:
        """Add a prospect to a recipe test."""
        for test in self.recipe_tests:
            if test.recipe_name == recipe_name:
                test.prospects.append(prospect)
                break

    def update_prospect_status(
        self,
        recipe_name: str,
        prospect_id: str,
        status: ProspectStatus,
        **kwargs,
    ) -> None:
        """Update a prospect's status."""
        for test in self.recipe_tests:
            if test.recipe_name == recipe_name:
                for prospect in test.prospects:
                    if prospect.prospect_id == prospect_id:
                        prospect.status = status
                        if status == ProspectStatus.MESSAGED:
                            prospect.sent_at = kwargs.get("sent_at", datetime.now())
                        elif status in [ProspectStatus.RESPONDED, ProspectStatus.MEETING_BOOKED]:
                            prospect.responded_at = kwargs.get("responded_at", datetime.now())
                            prospect.response_sentiment = kwargs.get("sentiment", "")
                        break

    def record_message_refinement(
        self,
        recipe_name: str,
        original_message: str,
        refined_message: str,
        reason: str,
        response_improvement: Optional[float] = None,
    ) -> None:
        """Record a message refinement."""
        self.message_refinements.append({
            "recipe_name": recipe_name,
            "original": original_message,
            "refined": refined_message,
            "reason": reason,
            "response_improvement": response_improvement,
            "recorded_at": datetime.now().isoformat(),
        })

    def get_recipe_metrics(self, recipe_name: str) -> Dict[str, Any]:
        """Get metrics for a specific recipe test."""
        for test in self.recipe_tests:
            if test.recipe_name == recipe_name:
                return {
                    "recipe_name": recipe_name,
                    "recipe_type": test.recipe_type,
                    "status": test.status.value,
                    "total_prospects": test.total_prospects,
                    "messaged": test.messaged_count,
                    "responses": test.response_count,
                    "positive_responses": test.positive_response_count,
                    "meetings": test.meeting_count,
                    "response_rate": test.response_rate,
                    "meets_threshold": test.response_rate >= 0.15,  # 15% target
                }
        return {}

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get metrics for all recipe tests."""
        metrics = {}
        for test in self.recipe_tests:
            metrics[test.recipe_name] = self.get_recipe_metrics(test.recipe_name)

        # Identify top performers
        sorted_tests = sorted(
            self.recipe_tests,
            key=lambda t: t.response_rate,
            reverse=True,
        )

        return {
            "recipes": metrics,
            "total_prospects_tested": sum(t.total_prospects for t in self.recipe_tests),
            "total_messages_sent": sum(t.messaged_count for t in self.recipe_tests),
            "overall_response_rate": (
                sum(t.response_count for t in self.recipe_tests) /
                sum(t.messaged_count for t in self.recipe_tests)
                if sum(t.messaged_count for t in self.recipe_tests) > 0 else 0
            ),
            "top_recipe": sorted_tests[0].recipe_name if sorted_tests else None,
            "refinements_made": len(self.message_refinements),
        }

    def validate_recipe(self, recipe_name: str) -> Dict[str, Any]:
        """Validate if a recipe has achieved target metrics."""
        metrics = self.get_recipe_metrics(recipe_name)

        validation = {
            "recipe_name": recipe_name,
            "validated": False,
            "issues": [],
        }

        # Check minimum prospects
        if metrics.get("total_prospects", 0) < 25:
            validation["issues"].append(
                f"Need 25 prospects, have {metrics.get('total_prospects', 0)}"
            )

        # Check if all messages sent
        if metrics.get("messaged", 0) < metrics.get("total_prospects", 0):
            validation["issues"].append("Not all prospects have been messaged")

        # Check response rate threshold
        if metrics.get("response_rate", 0) < 0.15:
            validation["issues"].append(
                f"Response rate {metrics.get('response_rate', 0):.1%} below 15% target"
            )

        validation["validated"] = len(validation["issues"]) == 0
        validation["metrics"] = metrics

        # Update recipe status
        for test in self.recipe_tests:
            if test.recipe_name == recipe_name:
                if validation["validated"]:
                    test.status = RecipeStatus.VALIDATED
                    test.completed_at = datetime.now()
                elif metrics.get("messaged", 0) >= metrics.get("total_prospects", 0):
                    test.status = RecipeStatus.FAILED

        return validation

    def validate_readiness(self) -> Dict[str, Any]:
        """Validate readiness to proceed to Phase 3."""
        issues = []

        validated_recipes = [
            t for t in self.recipe_tests if t.status == RecipeStatus.VALIDATED
        ]

        if len(validated_recipes) < 1:
            issues.append("Need at least 1 validated recipe to proceed")

        total_tested = sum(t.total_prospects for t in self.recipe_tests)
        if total_tested < 50:
            issues.append(f"Need at least 50 prospects tested (have {total_tested})")

        return {
            "ready": len(issues) == 0,
            "issues": issues,
            "validated_recipes": [t.recipe_name for t in validated_recipes],
            "overall_metrics": self.get_all_metrics(),
        }
