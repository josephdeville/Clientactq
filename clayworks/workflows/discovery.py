"""
ClayWorks Discovery Phase Module
================================

Phase 1: Discovery

OBJECTIVES:
- Map client's customer segments using ICP analysis
- Identify unique data sources for each segment
- Validate data accessibility
- Document existing customer patterns

DELIVERABLES:
- ICP definition document with 2-3 primary segments
- Data source matrix (Tier 1, 2, 3 for each segment)
- Sample data pulls (25 records per segment)
- Historical customer analysis
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Status of a workflow task."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


@dataclass
class ICPSegment:
    """Ideal Customer Profile segment definition."""
    name: str
    description: str
    industry_verticals: List[str]
    company_size_range: tuple  # (min, max) employees
    revenue_range: Optional[tuple] = None  # (min, max) revenue
    geographic_focus: List[str] = field(default_factory=list)
    key_characteristics: List[str] = field(default_factory=list)
    pain_points: List[str] = field(default_factory=list)
    buying_triggers: List[str] = field(default_factory=list)
    decision_makers: List[str] = field(default_factory=list)
    priority: int = 1  # 1 = highest priority

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "industry_verticals": self.industry_verticals,
            "company_size_range": self.company_size_range,
            "revenue_range": self.revenue_range,
            "geographic_focus": self.geographic_focus,
            "key_characteristics": self.key_characteristics,
            "pain_points": self.pain_points,
            "buying_triggers": self.buying_triggers,
            "decision_makers": self.decision_makers,
            "priority": self.priority,
        }


@dataclass
class DataSourceEntry:
    """Entry in the data source matrix."""
    source_name: str
    tier: int  # 1, 2, or 3
    data_points: List[str]
    access_method: str
    access_validated: bool = False
    api_available: bool = False
    cost: Optional[str] = None
    notes: str = ""


@dataclass
class CustomerAnalysis:
    """Analysis of an existing customer."""
    company_name: str
    how_they_found_you: str
    key_characteristics: List[str]
    aha_moment: str
    deal_size: Optional[float] = None
    sales_cycle_days: Optional[int] = None
    retention_status: str = ""
    expansion_potential: str = ""


@dataclass
class DiscoveryTask:
    """A task in the discovery phase."""
    name: str
    description: str
    week: int  # 1 or 2
    status: TaskStatus = TaskStatus.NOT_STARTED
    completed_at: Optional[datetime] = None
    notes: str = ""
    blockers: List[str] = field(default_factory=list)


class DiscoveryPhase:
    """
    Phase 1: Discovery

    Activities:
    Week 1:
    - Interview sales team: "Describe your last 5 best customers"
    - Interview CS team: "Which customers have highest retention/expansion?"
    - Pull list of closed-won deals from last 12 months
    - Analyze common attributes of best customers

    Week 2:
    - Research public data sources for each segment
    - Test API access and data quality
    - Create data source documentation
    - Identify gaps requiring paid tools
    """

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # Deliverables
        self.icp_segments: List[ICPSegment] = []
        self.data_source_matrix: Dict[str, List[DataSourceEntry]] = {}
        self.sample_records: Dict[str, List[Dict[str, Any]]] = {}
        self.customer_analyses: List[CustomerAnalysis] = []

        # Tasks
        self.tasks = self._initialize_tasks()

    def _initialize_tasks(self) -> List[DiscoveryTask]:
        """Initialize all discovery tasks."""
        return [
            # Week 1 tasks
            DiscoveryTask(
                name="sales_interview",
                description="Interview sales team: Describe your last 5 best customers",
                week=1,
            ),
            DiscoveryTask(
                name="cs_interview",
                description="Interview CS team: Which customers have highest retention/expansion?",
                week=1,
            ),
            DiscoveryTask(
                name="pull_closed_won",
                description="Pull list of closed-won deals from last 12 months",
                week=1,
            ),
            DiscoveryTask(
                name="analyze_attributes",
                description="Analyze common attributes of best customers",
                week=1,
            ),
            # Week 2 tasks
            DiscoveryTask(
                name="research_sources",
                description="Research public data sources for each segment",
                week=2,
            ),
            DiscoveryTask(
                name="test_api_access",
                description="Test API access and data quality",
                week=2,
            ),
            DiscoveryTask(
                name="create_documentation",
                description="Create data source documentation",
                week=2,
            ),
            DiscoveryTask(
                name="identify_gaps",
                description="Identify gaps requiring paid tools",
                week=2,
            ),
        ]

    def start(self) -> None:
        """Start the discovery phase."""
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark the discovery phase as complete."""
        self.completed_at = datetime.now()

    def add_icp_segment(self, segment: ICPSegment) -> None:
        """Add an ICP segment."""
        self.icp_segments.append(segment)

    def add_data_source(
        self, segment_name: str, source: DataSourceEntry
    ) -> None:
        """Add a data source to the matrix for a segment."""
        if segment_name not in self.data_source_matrix:
            self.data_source_matrix[segment_name] = []
        self.data_source_matrix[segment_name].append(source)

    def add_sample_records(
        self, segment_name: str, records: List[Dict[str, Any]]
    ) -> None:
        """Add sample records for a segment."""
        self.sample_records[segment_name] = records

    def add_customer_analysis(self, analysis: CustomerAnalysis) -> None:
        """Add a customer analysis."""
        self.customer_analyses.append(analysis)

    def update_task_status(
        self, task_name: str, status: TaskStatus, notes: str = ""
    ) -> None:
        """Update the status of a task."""
        for task in self.tasks:
            if task.name == task_name:
                task.status = status
                task.notes = notes
                if status == TaskStatus.COMPLETED:
                    task.completed_at = datetime.now()
                break

    def get_progress(self) -> Dict[str, Any]:
        """Get progress summary."""
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        blocked = sum(1 for t in self.tasks if t.status == TaskStatus.BLOCKED)

        return {
            "total_tasks": total_tasks,
            "completed": completed,
            "blocked": blocked,
            "progress_percentage": (completed / total_tasks * 100) if total_tasks > 0 else 0,
            "icp_segments_defined": len(self.icp_segments),
            "data_sources_identified": sum(len(v) for v in self.data_source_matrix.values()),
            "sample_records_collected": sum(len(v) for v in self.sample_records.values()),
            "customers_analyzed": len(self.customer_analyses),
        }

    def get_deliverables(self) -> Dict[str, Any]:
        """Get all deliverables."""
        return {
            "icp_segments": [s.to_dict() for s in self.icp_segments],
            "data_source_matrix": {
                segment: [
                    {
                        "source": s.source_name,
                        "tier": s.tier,
                        "data_points": s.data_points,
                        "validated": s.access_validated,
                    }
                    for s in sources
                ]
                for segment, sources in self.data_source_matrix.items()
            },
            "sample_record_counts": {
                segment: len(records)
                for segment, records in self.sample_records.items()
            },
            "customer_patterns": self._extract_customer_patterns(),
        }

    def _extract_customer_patterns(self) -> Dict[str, Any]:
        """Extract patterns from customer analyses."""
        if not self.customer_analyses:
            return {}

        # Aggregate characteristics
        all_characteristics = []
        for analysis in self.customer_analyses:
            all_characteristics.extend(analysis.key_characteristics)

        # Count occurrences
        char_counts = {}
        for char in all_characteristics:
            char_counts[char] = char_counts.get(char, 0) + 1

        # Get top characteristics
        top_chars = sorted(
            char_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]

        # Average deal size and cycle
        deal_sizes = [a.deal_size for a in self.customer_analyses if a.deal_size]
        cycle_days = [a.sales_cycle_days for a in self.customer_analyses if a.sales_cycle_days]

        return {
            "common_characteristics": dict(top_chars),
            "avg_deal_size": sum(deal_sizes) / len(deal_sizes) if deal_sizes else None,
            "avg_sales_cycle_days": sum(cycle_days) / len(cycle_days) if cycle_days else None,
            "total_customers_analyzed": len(self.customer_analyses),
        }

    def validate_readiness(self) -> Dict[str, Any]:
        """Validate readiness to proceed to Phase 2."""
        issues = []

        if len(self.icp_segments) < 2:
            issues.append("Need at least 2 ICP segments defined")

        if not self.data_source_matrix:
            issues.append("No data sources identified")

        for segment in self.icp_segments:
            segment_sources = self.data_source_matrix.get(segment.name, [])
            tiers_covered = set(s.tier for s in segment_sources)
            if not tiers_covered.issuperset({1, 2, 3}):
                issues.append(f"Segment '{segment.name}' missing data sources for all tiers")

        total_samples = sum(len(v) for v in self.sample_records.values())
        if total_samples < 25:
            issues.append(f"Need at least 25 sample records (have {total_samples})")

        if len(self.customer_analyses) < 3:
            issues.append("Need at least 3 customer analyses")

        incomplete_tasks = [t for t in self.tasks if t.status != TaskStatus.COMPLETED]

        return {
            "ready": len(issues) == 0 and len(incomplete_tasks) == 0,
            "issues": issues,
            "incomplete_tasks": [t.name for t in incomplete_tasks],
        }
