"""
ClayWorks Scoring Module
========================

Prospect scoring engine for evaluating and prioritizing prospects
based on pain signals, data recipes, and fit criteria.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum


class ScoreCategory(Enum):
    """Categories of scoring criteria."""
    OBLIGATION_URGENCY = "obligation_urgency"
    HIRING_SIGNAL = "hiring_signal"
    TECHNOLOGY_GAP = "technology_gap"
    COMPANY_FIT = "company_fit"
    TIMING = "timing"
    ENGAGEMENT = "engagement"


@dataclass
class ScoringRule:
    """A single scoring rule definition."""
    name: str
    category: ScoreCategory
    description: str
    max_points: int
    condition: Callable[[Dict[str, Any]], bool]
    score_function: Callable[[Dict[str, Any]], int]
    weight: float = 1.0

    def evaluate(self, prospect_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate this rule against prospect data."""
        if self.condition(prospect_data):
            raw_score = self.score_function(prospect_data)
            weighted_score = int(raw_score * self.weight)
            return {
                "applies": True,
                "raw_score": raw_score,
                "weighted_score": min(weighted_score, self.max_points),
                "rule_name": self.name,
                "category": self.category.value,
            }
        return {
            "applies": False,
            "raw_score": 0,
            "weighted_score": 0,
            "rule_name": self.name,
            "category": self.category.value,
        }


@dataclass
class ProspectScore:
    """Complete scoring result for a prospect."""
    prospect_id: str
    total_score: int
    max_possible: int
    category_scores: Dict[str, int]
    rule_results: List[Dict[str, Any]]
    qualifies: bool
    scored_at: datetime
    threshold_used: int
    confidence: float

    @property
    def score_percentage(self) -> float:
        """Score as a percentage of maximum possible."""
        return (self.total_score / self.max_possible * 100) if self.max_possible > 0 else 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "prospect_id": self.prospect_id,
            "total_score": self.total_score,
            "max_possible": self.max_possible,
            "score_percentage": self.score_percentage,
            "category_scores": self.category_scores,
            "qualifies": self.qualifies,
            "scored_at": self.scored_at.isoformat(),
            "threshold_used": self.threshold_used,
            "confidence": self.confidence,
            "rule_results": self.rule_results,
        }


class ProspectScorer:
    """
    Prospect Scoring Engine.

    Evaluates prospects based on configurable rules and weights
    to prioritize outreach efforts.

    Default Scoring Model (from Blueprint):
    - Obligation urgency: 30 points
    - Recent hiring signal: 25 points
    - Technology gap: 25 points
    - Company fit: 20 points
    - TOTAL THRESHOLD: 70+ points
    """

    def __init__(
        self,
        threshold: int = 70,
        weights: Optional[Dict[ScoreCategory, float]] = None
    ):
        self.threshold = threshold
        self.rules: List[ScoringRule] = []
        self.weights = weights or {
            ScoreCategory.OBLIGATION_URGENCY: 1.0,
            ScoreCategory.HIRING_SIGNAL: 1.0,
            ScoreCategory.TECHNOLOGY_GAP: 1.0,
            ScoreCategory.COMPANY_FIT: 1.0,
            ScoreCategory.TIMING: 1.0,
            ScoreCategory.ENGAGEMENT: 1.0,
        }

    def add_rule(self, rule: ScoringRule) -> None:
        """Add a scoring rule."""
        self.rules.append(rule)

    def create_rule(
        self,
        name: str,
        category: ScoreCategory,
        description: str,
        max_points: int,
        condition: Callable[[Dict[str, Any]], bool],
        score_function: Callable[[Dict[str, Any]], int],
    ) -> ScoringRule:
        """Create and add a new scoring rule."""
        weight = self.weights.get(category, 1.0)
        rule = ScoringRule(
            name=name,
            category=category,
            description=description,
            max_points=max_points,
            condition=condition,
            score_function=score_function,
            weight=weight,
        )
        self.add_rule(rule)
        return rule

    def score_prospect(
        self, prospect_id: str, prospect_data: Dict[str, Any]
    ) -> ProspectScore:
        """
        Score a single prospect against all rules.

        Args:
            prospect_id: Unique identifier for the prospect
            prospect_data: Dictionary containing all prospect data fields

        Returns:
            ProspectScore with complete scoring breakdown
        """
        rule_results = []
        category_scores: Dict[str, int] = {}
        total_score = 0
        max_possible = 0

        for rule in self.rules:
            result = rule.evaluate(prospect_data)
            rule_results.append(result)

            # Track max possible
            max_possible += rule.max_points

            if result["applies"]:
                score = result["weighted_score"]
                total_score += score

                # Aggregate by category
                category = result["category"]
                category_scores[category] = category_scores.get(category, 0) + score

        # Calculate confidence based on data completeness
        data_completeness = self._calculate_data_completeness(prospect_data)
        confidence = data_completeness * (total_score / max_possible if max_possible > 0 else 0)

        return ProspectScore(
            prospect_id=prospect_id,
            total_score=total_score,
            max_possible=max_possible,
            category_scores=category_scores,
            rule_results=rule_results,
            qualifies=total_score >= self.threshold,
            scored_at=datetime.now(),
            threshold_used=self.threshold,
            confidence=confidence,
        )

    def score_batch(
        self, prospects: List[Dict[str, Any]], id_field: str = "id"
    ) -> List[ProspectScore]:
        """
        Score multiple prospects.

        Args:
            prospects: List of prospect data dictionaries
            id_field: Name of the field containing the prospect ID

        Returns:
            List of ProspectScore objects, sorted by score descending
        """
        scores = []
        for prospect in prospects:
            prospect_id = prospect.get(id_field, str(len(scores)))
            score = self.score_prospect(prospect_id, prospect)
            scores.append(score)

        # Sort by total score descending
        scores.sort(key=lambda x: x.total_score, reverse=True)
        return scores

    def get_qualified_prospects(
        self, prospects: List[Dict[str, Any]], id_field: str = "id"
    ) -> List[ProspectScore]:
        """Get only prospects that meet the threshold."""
        scores = self.score_batch(prospects, id_field)
        return [s for s in scores if s.qualifies]

    def _calculate_data_completeness(self, prospect_data: Dict[str, Any]) -> float:
        """Calculate how complete the prospect data is."""
        # Key fields that should be present for accurate scoring
        key_fields = [
            "company_name",
            "employee_count",
            "industry",
            "tech_stack",
            "recent_job_postings",
            "funding_stage",
            "compliance_requirements",
        ]

        present = sum(1 for field in key_fields if prospect_data.get(field))
        return present / len(key_fields)

    def explain_score(self, score: ProspectScore) -> str:
        """Generate a human-readable explanation of a score."""
        lines = [
            f"Score: {score.total_score}/{score.max_possible} ({score.score_percentage:.1f}%)",
            f"Qualifies: {'Yes' if score.qualifies else 'No'} (threshold: {score.threshold_used})",
            f"Confidence: {score.confidence:.2%}",
            "",
            "Category Breakdown:",
        ]

        for category, points in sorted(score.category_scores.items()):
            lines.append(f"  - {category}: {points} points")

        lines.extend(["", "Applied Rules:"])
        for result in score.rule_results:
            if result["applies"]:
                lines.append(f"  + {result['rule_name']}: +{result['weighted_score']} pts")

        return "\n".join(lines)


def create_default_scorer() -> ProspectScorer:
    """
    Create a scorer with default Blueprint GTM rules.

    Default Scoring Model:
    - Obligation urgency: 30 points
    - Recent hiring signal: 25 points
    - Technology gap: 25 points
    - Company fit: 20 points
    """
    scorer = ProspectScorer(threshold=70)

    # Obligation Urgency Rules (30 points max)
    scorer.create_rule(
        name="has_compliance_deadline",
        category=ScoreCategory.OBLIGATION_URGENCY,
        description="Company has upcoming compliance deadline",
        max_points=15,
        condition=lambda d: bool(d.get("compliance_deadline")),
        score_function=lambda d: 15 if d.get("compliance_deadline") else 0,
    )

    scorer.create_rule(
        name="has_contract_obligation",
        category=ScoreCategory.OBLIGATION_URGENCY,
        description="Company has contract-based obligations",
        max_points=15,
        condition=lambda d: bool(d.get("contract_obligations")),
        score_function=lambda d: min(15, len(d.get("contract_obligations", [])) * 5),
    )

    # Hiring Signal Rules (25 points max)
    scorer.create_rule(
        name="recent_relevant_hiring",
        category=ScoreCategory.HIRING_SIGNAL,
        description="Posted relevant job in last 30 days",
        max_points=15,
        condition=lambda d: bool(d.get("recent_job_postings")),
        score_function=lambda d: min(15, len(d.get("recent_job_postings", [])) * 5),
    )

    scorer.create_rule(
        name="team_growth",
        category=ScoreCategory.HIRING_SIGNAL,
        description="Team growing rapidly",
        max_points=10,
        condition=lambda d: d.get("employee_growth_rate", 0) > 0.1,
        score_function=lambda d: min(10, int(d.get("employee_growth_rate", 0) * 50)),
    )

    # Technology Gap Rules (25 points max)
    scorer.create_rule(
        name="outdated_tech_stack",
        category=ScoreCategory.TECHNOLOGY_GAP,
        description="Using outdated or legacy technology",
        max_points=15,
        condition=lambda d: bool(d.get("legacy_tech_indicators")),
        score_function=lambda d: min(15, len(d.get("legacy_tech_indicators", [])) * 5),
    )

    scorer.create_rule(
        name="missing_key_tech",
        category=ScoreCategory.TECHNOLOGY_GAP,
        description="Missing key technology for their size/stage",
        max_points=10,
        condition=lambda d: bool(d.get("tech_gaps")),
        score_function=lambda d: min(10, len(d.get("tech_gaps", [])) * 3),
    )

    # Company Fit Rules (20 points max)
    scorer.create_rule(
        name="size_fit",
        category=ScoreCategory.COMPANY_FIT,
        description="Company size matches ICP",
        max_points=10,
        condition=lambda d: d.get("size_fit", False),
        score_function=lambda d: 10 if d.get("size_fit") else 0,
    )

    scorer.create_rule(
        name="industry_fit",
        category=ScoreCategory.COMPANY_FIT,
        description="Company industry matches ICP",
        max_points=10,
        condition=lambda d: d.get("industry_fit", False),
        score_function=lambda d: 10 if d.get("industry_fit") else 0,
    )

    return scorer
