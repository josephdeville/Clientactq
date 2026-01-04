"""
ClayWorks Metrics Module
========================

Metrics tracking and benchmarking for GTM performance.

Baseline (Traditional Outreach):
- Cold email response rate: 0.5-1%
- LinkedIn connection accept: 15-25%
- LinkedIn InMail response: 3-5%

Target (Blueprint Framework):
- PQS email response rate: 15-25%
- PVP email response rate: 20-30%
- LinkedIn with PQS/PVP messaging: 25-40%
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class MetricType(Enum):
    """Types of metrics tracked."""
    PROSPECTS_RESEARCHED = "prospects_researched"
    MESSAGES_SENT = "messages_sent"
    OPENS = "opens"
    REPLIES = "replies"
    POSITIVE_REPLIES = "positive_replies"
    MEETINGS_BOOKED = "meetings_booked"
    PIPELINE_CREATED = "pipeline_created"
    DEALS_WON = "deals_won"


@dataclass
class MetricsBenchmark:
    """Benchmarks for comparing performance."""
    # Baseline (Traditional Outreach)
    baseline_email_response: float = 0.005  # 0.5%
    baseline_linkedin_accept: float = 0.20  # 20%
    baseline_inmail_response: float = 0.04  # 4%

    # Target (Blueprint Framework)
    target_pqs_response: float = 0.20  # 20%
    target_pvp_response: float = 0.25  # 25%
    target_linkedin_pqs: float = 0.32  # 32%

    # Weekly targets
    target_prospects_per_week: int = 50
    target_messages_per_week: int = 50
    target_open_rate: float = 0.60  # 60%
    target_reply_rate: float = 0.15  # 15%
    target_positive_rate: float = 0.10  # 10%
    target_meeting_rate: float = 0.05  # 5%


@dataclass
class MetricEntry:
    """A single metric entry."""
    metric_type: MetricType
    value: float
    period: str  # e.g., "2024-W01" for week 1
    recipe_name: Optional[str] = None
    channel: Optional[str] = None
    recorded_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_type": self.metric_type.value,
            "value": self.value,
            "period": self.period,
            "recipe_name": self.recipe_name,
            "channel": self.channel,
            "recorded_at": self.recorded_at.isoformat(),
        }


@dataclass
class WeeklyMetrics:
    """Weekly metrics snapshot."""
    week: str  # e.g., "2024-W01"
    prospects_researched: int = 0
    messages_sent: int = 0
    opens: int = 0
    replies: int = 0
    positive_replies: int = 0
    meetings_booked: int = 0
    pipeline_created: float = 0.0

    @property
    def open_rate(self) -> float:
        return self.opens / self.messages_sent if self.messages_sent > 0 else 0

    @property
    def reply_rate(self) -> float:
        return self.replies / self.messages_sent if self.messages_sent > 0 else 0

    @property
    def positive_rate(self) -> float:
        return self.positive_replies / self.messages_sent if self.messages_sent > 0 else 0

    @property
    def meeting_rate(self) -> float:
        return self.meetings_booked / self.messages_sent if self.messages_sent > 0 else 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "week": self.week,
            "prospects_researched": self.prospects_researched,
            "messages_sent": self.messages_sent,
            "opens": self.opens,
            "replies": self.replies,
            "positive_replies": self.positive_replies,
            "meetings_booked": self.meetings_booked,
            "pipeline_created": self.pipeline_created,
            "rates": {
                "open_rate": self.open_rate,
                "reply_rate": self.reply_rate,
                "positive_rate": self.positive_rate,
                "meeting_rate": self.meeting_rate,
            },
        }


class MetricsTracker:
    """
    Metrics tracking for GTM performance.

    Tracks weekly metrics and compares against benchmarks.
    """

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.benchmark = MetricsBenchmark()
        self.entries: List[MetricEntry] = []
        self.weekly_metrics: Dict[str, WeeklyMetrics] = {}

    def record_metric(
        self,
        metric_type: MetricType,
        value: float,
        period: Optional[str] = None,
        recipe_name: Optional[str] = None,
        channel: Optional[str] = None,
    ) -> None:
        """Record a metric entry."""
        if period is None:
            # Use current week
            now = datetime.now()
            period = f"{now.year}-W{now.isocalendar()[1]:02d}"

        entry = MetricEntry(
            metric_type=metric_type,
            value=value,
            period=period,
            recipe_name=recipe_name,
            channel=channel,
        )
        self.entries.append(entry)

        # Update weekly metrics
        self._update_weekly_metrics(entry)

    def _update_weekly_metrics(self, entry: MetricEntry) -> None:
        """Update weekly metrics from an entry."""
        week = entry.period
        if week not in self.weekly_metrics:
            self.weekly_metrics[week] = WeeklyMetrics(week=week)

        metrics = self.weekly_metrics[week]
        value = int(entry.value)

        if entry.metric_type == MetricType.PROSPECTS_RESEARCHED:
            metrics.prospects_researched += value
        elif entry.metric_type == MetricType.MESSAGES_SENT:
            metrics.messages_sent += value
        elif entry.metric_type == MetricType.OPENS:
            metrics.opens += value
        elif entry.metric_type == MetricType.REPLIES:
            metrics.replies += value
        elif entry.metric_type == MetricType.POSITIVE_REPLIES:
            metrics.positive_replies += value
        elif entry.metric_type == MetricType.MEETINGS_BOOKED:
            metrics.meetings_booked += value
        elif entry.metric_type == MetricType.PIPELINE_CREATED:
            metrics.pipeline_created += entry.value

    def get_weekly_metrics(self, week: str) -> Optional[WeeklyMetrics]:
        """Get metrics for a specific week."""
        return self.weekly_metrics.get(week)

    def get_current_week_metrics(self) -> Optional[WeeklyMetrics]:
        """Get metrics for the current week."""
        now = datetime.now()
        week = f"{now.year}-W{now.isocalendar()[1]:02d}"
        return self.get_weekly_metrics(week)

    def compare_to_benchmark(
        self, metrics: WeeklyMetrics
    ) -> Dict[str, Any]:
        """Compare weekly metrics to benchmarks."""
        return {
            "prospects_researched": {
                "actual": metrics.prospects_researched,
                "target": self.benchmark.target_prospects_per_week,
                "status": "on_target" if metrics.prospects_researched >= self.benchmark.target_prospects_per_week else "below",
            },
            "messages_sent": {
                "actual": metrics.messages_sent,
                "target": self.benchmark.target_messages_per_week,
                "status": "on_target" if metrics.messages_sent >= self.benchmark.target_messages_per_week else "below",
            },
            "open_rate": {
                "actual": metrics.open_rate,
                "target": self.benchmark.target_open_rate,
                "status": "on_target" if metrics.open_rate >= self.benchmark.target_open_rate else "below",
                "vs_baseline": metrics.open_rate / 0.20 if metrics.open_rate > 0 else 0,  # vs typical 20% open
            },
            "reply_rate": {
                "actual": metrics.reply_rate,
                "target": self.benchmark.target_reply_rate,
                "status": "on_target" if metrics.reply_rate >= self.benchmark.target_reply_rate else "below",
                "vs_baseline": metrics.reply_rate / self.benchmark.baseline_email_response,
            },
            "meeting_rate": {
                "actual": metrics.meeting_rate,
                "target": self.benchmark.target_meeting_rate,
                "status": "on_target" if metrics.meeting_rate >= self.benchmark.target_meeting_rate else "below",
            },
        }

    def get_metrics_by_recipe(self) -> Dict[str, Dict[str, float]]:
        """Get metrics aggregated by recipe."""
        recipe_metrics: Dict[str, Dict[str, float]] = {}

        for entry in self.entries:
            if entry.recipe_name:
                if entry.recipe_name not in recipe_metrics:
                    recipe_metrics[entry.recipe_name] = {}

                metric_name = entry.metric_type.value
                current = recipe_metrics[entry.recipe_name].get(metric_name, 0)
                recipe_metrics[entry.recipe_name][metric_name] = current + entry.value

        # Calculate rates for each recipe
        for recipe_name, metrics in recipe_metrics.items():
            sent = metrics.get("messages_sent", 0)
            if sent > 0:
                metrics["open_rate"] = metrics.get("opens", 0) / sent
                metrics["reply_rate"] = metrics.get("replies", 0) / sent
                metrics["meeting_rate"] = metrics.get("meetings_booked", 0) / sent

        return recipe_metrics

    def get_trend(self, num_weeks: int = 4) -> List[Dict[str, Any]]:
        """Get trend data for the last N weeks."""
        # Sort weeks and get last N
        sorted_weeks = sorted(self.weekly_metrics.keys(), reverse=True)[:num_weeks]
        sorted_weeks.reverse()  # Chronological order

        return [
            {
                "week": week,
                **self.weekly_metrics[week].to_dict(),
                "benchmark_comparison": self.compare_to_benchmark(self.weekly_metrics[week]),
            }
            for week in sorted_weeks
        ]

    def calculate_improvement(self) -> Dict[str, Any]:
        """Calculate improvement over time."""
        sorted_weeks = sorted(self.weekly_metrics.keys())

        if len(sorted_weeks) < 2:
            return {"insufficient_data": True}

        first_week = self.weekly_metrics[sorted_weeks[0]]
        last_week = self.weekly_metrics[sorted_weeks[-1]]

        def calc_change(old: float, new: float) -> float:
            if old == 0:
                return 0
            return (new - old) / old * 100

        return {
            "period": f"{sorted_weeks[0]} to {sorted_weeks[-1]}",
            "weeks_tracked": len(sorted_weeks),
            "reply_rate_change": calc_change(first_week.reply_rate, last_week.reply_rate),
            "meeting_rate_change": calc_change(first_week.meeting_rate, last_week.meeting_rate),
            "volume_change": calc_change(first_week.messages_sent, last_week.messages_sent),
            "vs_baseline_improvement": (
                last_week.reply_rate / self.benchmark.baseline_email_response
                if last_week.reply_rate > 0 else 0
            ),
        }

    def export_data(self, filepath: str) -> None:
        """Export all metrics data to JSON."""
        data = {
            "client_name": self.client_name,
            "exported_at": datetime.now().isoformat(),
            "weekly_metrics": {
                week: metrics.to_dict()
                for week, metrics in self.weekly_metrics.items()
            },
            "entries": [e.to_dict() for e in self.entries],
            "by_recipe": self.get_metrics_by_recipe(),
            "improvement": self.calculate_improvement(),
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate data for a metrics dashboard."""
        current = self.get_current_week_metrics()

        return {
            "current_week": current.to_dict() if current else None,
            "trend": self.get_trend(4),
            "by_recipe": self.get_metrics_by_recipe(),
            "benchmarks": {
                "baseline": {
                    "email_response": self.benchmark.baseline_email_response,
                    "linkedin_accept": self.benchmark.baseline_linkedin_accept,
                    "inmail_response": self.benchmark.baseline_inmail_response,
                },
                "target": {
                    "pqs_response": self.benchmark.target_pqs_response,
                    "pvp_response": self.benchmark.target_pvp_response,
                    "linkedin_pqs": self.benchmark.target_linkedin_pqs,
                },
            },
            "improvement": self.calculate_improvement(),
        }
