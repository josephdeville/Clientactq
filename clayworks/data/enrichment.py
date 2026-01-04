"""
ClayWorks Enrichment Pipeline Module
=====================================

Data enrichment pipeline for aggregating and enhancing prospect data
from multiple sources across all three data tiers.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Union
from datetime import datetime
from enum import Enum
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor


class EnrichmentStatus(Enum):
    """Status of an enrichment step."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class EnrichmentResult:
    """Result of a single enrichment step."""
    step_name: str
    status: EnrichmentStatus
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate duration if both timestamps are set."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


@dataclass
class EnrichmentStep:
    """
    A single step in the enrichment pipeline.

    Each step fetches data from a specific source and adds it to
    the prospect record.
    """
    name: str
    source_name: str
    fields_to_fetch: List[str]
    fetch_function: Callable[[Dict[str, Any]], Dict[str, Any]]
    required: bool = False
    depends_on: List[str] = field(default_factory=list)
    timeout_seconds: int = 30
    retry_count: int = 3
    enabled: bool = True

    def execute(self, input_data: Dict[str, Any]) -> EnrichmentResult:
        """Execute this enrichment step."""
        result = EnrichmentResult(
            step_name=self.name,
            status=EnrichmentStatus.IN_PROGRESS,
            started_at=datetime.now(),
        )

        if not self.enabled:
            result.status = EnrichmentStatus.SKIPPED
            result.completed_at = datetime.now()
            return result

        retries = 0
        last_error = None

        while retries <= self.retry_count:
            try:
                data = self.fetch_function(input_data)
                result.data = data
                result.status = EnrichmentStatus.COMPLETED
                result.completed_at = datetime.now()
                return result
            except Exception as e:
                last_error = str(e)
                retries += 1

        result.status = EnrichmentStatus.FAILED
        result.error = last_error
        result.completed_at = datetime.now()
        return result


@dataclass
class ProspectRecord:
    """A prospect record being enriched."""
    prospect_id: str
    initial_data: Dict[str, Any]
    enriched_data: Dict[str, Any] = field(default_factory=dict)
    enrichment_results: List[EnrichmentResult] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_enriched_at: Optional[datetime] = None

    def merge_enrichment(self, result: EnrichmentResult) -> None:
        """Merge enrichment result into the record."""
        self.enrichment_results.append(result)
        if result.status == EnrichmentStatus.COMPLETED and result.data:
            self.enriched_data.update(result.data)
        self.last_enriched_at = datetime.now()

    @property
    def all_data(self) -> Dict[str, Any]:
        """Get combined initial and enriched data."""
        return {**self.initial_data, **self.enriched_data}

    @property
    def enrichment_complete(self) -> bool:
        """Check if all enrichment steps completed successfully."""
        return all(
            r.status in [EnrichmentStatus.COMPLETED, EnrichmentStatus.SKIPPED]
            for r in self.enrichment_results
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "prospect_id": self.prospect_id,
            "initial_data": self.initial_data,
            "enriched_data": self.enriched_data,
            "all_data": self.all_data,
            "enrichment_complete": self.enrichment_complete,
            "enrichment_results": [
                {
                    "step": r.step_name,
                    "status": r.status.value,
                    "error": r.error,
                    "duration": r.duration_seconds,
                }
                for r in self.enrichment_results
            ],
        }


class EnrichmentPipeline:
    """
    Data Enrichment Pipeline.

    Orchestrates the enrichment of prospect data from multiple sources
    in the correct order based on dependencies.

    Usage:
        pipeline = EnrichmentPipeline()
        pipeline.add_step(EnrichmentStep(...))
        pipeline.add_step(EnrichmentStep(...))

        result = pipeline.enrich(prospect_data)
    """

    def __init__(self, name: str = "default"):
        self.name = name
        self.steps: List[EnrichmentStep] = []
        self._step_order: List[str] = []

    def add_step(self, step: EnrichmentStep) -> None:
        """Add an enrichment step to the pipeline."""
        self.steps.append(step)
        self._recalculate_order()

    def _recalculate_order(self) -> None:
        """Recalculate step execution order based on dependencies."""
        # Topological sort for dependency ordering
        visited = set()
        order = []

        def visit(step_name: str) -> None:
            if step_name in visited:
                return
            visited.add(step_name)

            step = next((s for s in self.steps if s.name == step_name), None)
            if step:
                for dep in step.depends_on:
                    visit(dep)
                order.append(step_name)

        for step in self.steps:
            visit(step.name)

        self._step_order = order

    def get_step(self, name: str) -> Optional[EnrichmentStep]:
        """Get a step by name."""
        return next((s for s in self.steps if s.name == name), None)

    def enrich(
        self,
        prospect_id: str,
        initial_data: Dict[str, Any],
    ) -> ProspectRecord:
        """
        Run the enrichment pipeline on a prospect.

        Args:
            prospect_id: Unique identifier for the prospect
            initial_data: Starting data for the prospect

        Returns:
            Enriched ProspectRecord
        """
        record = ProspectRecord(
            prospect_id=prospect_id,
            initial_data=initial_data,
        )

        for step_name in self._step_order:
            step = self.get_step(step_name)
            if not step:
                continue

            # Check dependencies
            deps_met = all(
                any(
                    r.step_name == dep and r.status == EnrichmentStatus.COMPLETED
                    for r in record.enrichment_results
                )
                for dep in step.depends_on
            )

            if not deps_met:
                # Skip this step if dependencies not met
                result = EnrichmentResult(
                    step_name=step.name,
                    status=EnrichmentStatus.SKIPPED,
                    error="Dependencies not met",
                )
                record.enrichment_results.append(result)
                continue

            # Execute the step
            result = step.execute(record.all_data)
            record.merge_enrichment(result)

            # If required step failed, stop pipeline
            if step.required and result.status == EnrichmentStatus.FAILED:
                break

        return record

    def enrich_batch(
        self,
        prospects: List[Dict[str, Any]],
        id_field: str = "id",
        parallel: bool = True,
        max_workers: int = 5,
    ) -> List[ProspectRecord]:
        """
        Enrich multiple prospects.

        Args:
            prospects: List of prospect data dictionaries
            id_field: Field name containing the prospect ID
            parallel: Whether to run in parallel
            max_workers: Maximum number of parallel workers

        Returns:
            List of enriched ProspectRecords
        """
        if not parallel:
            return [
                self.enrich(p.get(id_field, str(i)), p)
                for i, p in enumerate(prospects)
            ]

        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    self.enrich,
                    p.get(id_field, str(i)),
                    p,
                )
                for i, p in enumerate(prospects)
            ]
            results = [f.result() for f in futures]

        return results

    def get_pipeline_stats(
        self, records: List[ProspectRecord]
    ) -> Dict[str, Any]:
        """Get statistics about pipeline execution."""
        stats = {
            "total_prospects": len(records),
            "fully_enriched": sum(1 for r in records if r.enrichment_complete),
            "step_stats": {},
        }

        for step in self.steps:
            step_results = [
                r for record in records
                for r in record.enrichment_results
                if r.step_name == step.name
            ]

            completed = sum(1 for r in step_results if r.status == EnrichmentStatus.COMPLETED)
            failed = sum(1 for r in step_results if r.status == EnrichmentStatus.FAILED)
            skipped = sum(1 for r in step_results if r.status == EnrichmentStatus.SKIPPED)

            durations = [r.duration_seconds for r in step_results if r.duration_seconds]
            avg_duration = sum(durations) / len(durations) if durations else 0

            stats["step_stats"][step.name] = {
                "completed": completed,
                "failed": failed,
                "skipped": skipped,
                "success_rate": completed / len(step_results) if step_results else 0,
                "avg_duration_seconds": avg_duration,
            }

        return stats

    def export_config(self) -> Dict[str, Any]:
        """Export pipeline configuration."""
        return {
            "name": self.name,
            "steps": [
                {
                    "name": s.name,
                    "source_name": s.source_name,
                    "fields_to_fetch": s.fields_to_fetch,
                    "required": s.required,
                    "depends_on": s.depends_on,
                    "timeout_seconds": s.timeout_seconds,
                    "retry_count": s.retry_count,
                    "enabled": s.enabled,
                }
                for s in self.steps
            ],
            "execution_order": self._step_order,
        }


def create_default_pipeline() -> EnrichmentPipeline:
    """
    Create a default enrichment pipeline with common steps.

    This pipeline follows the three-tier data architecture:
    1. Foundational data (company basics)
    2. Activity signals (hiring, tech, funding)
    3. Market voice (sentiment, reviews)
    """
    pipeline = EnrichmentPipeline(name="default")

    # Tier 1: Foundational
    pipeline.add_step(EnrichmentStep(
        name="company_basics",
        source_name="clearbit",
        fields_to_fetch=["domain", "name", "industry", "employee_count", "founded_year"],
        fetch_function=lambda d: {"company_enriched": True},  # Placeholder
        required=True,
    ))

    # Tier 2: Activity Signals
    pipeline.add_step(EnrichmentStep(
        name="tech_stack",
        source_name="builtwith",
        fields_to_fetch=["technologies", "tech_categories"],
        fetch_function=lambda d: {"tech_enriched": True},  # Placeholder
        depends_on=["company_basics"],
    ))

    pipeline.add_step(EnrichmentStep(
        name="job_postings",
        source_name="linkedin_jobs",
        fields_to_fetch=["open_positions", "role_types", "posting_dates"],
        fetch_function=lambda d: {"jobs_enriched": True},  # Placeholder
        depends_on=["company_basics"],
    ))

    pipeline.add_step(EnrichmentStep(
        name="funding_data",
        source_name="crunchbase",
        fields_to_fetch=["funding_rounds", "total_funding", "last_funding_date"],
        fetch_function=lambda d: {"funding_enriched": True},  # Placeholder
        depends_on=["company_basics"],
    ))

    # Tier 3: Market Voice
    pipeline.add_step(EnrichmentStep(
        name="reviews",
        source_name="g2",
        fields_to_fetch=["rating", "review_count", "sentiment"],
        fetch_function=lambda d: {"reviews_enriched": True},  # Placeholder
        depends_on=["company_basics"],
    ))

    return pipeline
