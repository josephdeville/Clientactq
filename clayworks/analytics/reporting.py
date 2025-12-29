"""
ClayWorks Reporting Module
==========================

Report generation for GTM performance and insights.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

from .metrics import MetricsTracker, WeeklyMetrics


@dataclass
class ReportSection:
    """A section of a report."""
    title: str
    content: str
    data: Optional[Dict[str, Any]] = None
    chart_type: Optional[str] = None  # bar, line, pie, table


@dataclass
class Report:
    """A generated report."""
    title: str
    report_type: str
    generated_at: datetime
    period: str
    sections: List[ReportSection]
    summary: str
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "report_type": self.report_type,
            "generated_at": self.generated_at.isoformat(),
            "period": self.period,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "sections": [
                {
                    "title": s.title,
                    "content": s.content,
                    "data": s.data,
                    "chart_type": s.chart_type,
                }
                for s in self.sections
            ],
        }

    def to_markdown(self) -> str:
        """Export report as Markdown."""
        lines = [
            f"# {self.title}",
            f"*Generated: {self.generated_at.strftime('%Y-%m-%d %H:%M')}*",
            f"*Period: {self.period}*",
            "",
            "## Summary",
            self.summary,
            "",
        ]

        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append(section.content)
            lines.append("")

            if section.data and section.chart_type == "table":
                # Render as markdown table
                if isinstance(section.data, dict):
                    lines.append("| Metric | Value |")
                    lines.append("|--------|-------|")
                    for key, value in section.data.items():
                        lines.append(f"| {key} | {value} |")
                    lines.append("")

        lines.append("## Recommendations")
        for i, rec in enumerate(self.recommendations, 1):
            lines.append(f"{i}. {rec}")

        return "\n".join(lines)


class ReportGenerator:
    """
    Report generation for GTM performance.

    Generates:
    - Weekly performance reports
    - Recipe comparison reports
    - Improvement analysis reports
    - Executive summaries
    """

    def __init__(self, metrics_tracker: MetricsTracker):
        self.metrics = metrics_tracker

    def generate_weekly_report(self, week: Optional[str] = None) -> Report:
        """Generate a weekly performance report."""
        if week is None:
            now = datetime.now()
            week = f"{now.year}-W{now.isocalendar()[1]:02d}"

        weekly_data = self.metrics.get_weekly_metrics(week)

        if not weekly_data:
            return Report(
                title=f"Weekly Report - {week}",
                report_type="weekly",
                generated_at=datetime.now(),
                period=week,
                sections=[],
                summary="No data available for this week.",
                recommendations=["Start tracking metrics to generate reports."],
            )

        comparison = self.metrics.compare_to_benchmark(weekly_data)

        sections = [
            ReportSection(
                title="Activity Metrics",
                content="Overview of outreach activity this week.",
                data={
                    "Prospects Researched": weekly_data.prospects_researched,
                    "Messages Sent": weekly_data.messages_sent,
                    "Opens": weekly_data.opens,
                    "Replies": weekly_data.replies,
                    "Meetings Booked": weekly_data.meetings_booked,
                },
                chart_type="table",
            ),
            ReportSection(
                title="Performance Rates",
                content="Conversion rates compared to targets.",
                data={
                    "Open Rate": f"{weekly_data.open_rate:.1%} (target: {self.metrics.benchmark.target_open_rate:.1%})",
                    "Reply Rate": f"{weekly_data.reply_rate:.1%} (target: {self.metrics.benchmark.target_reply_rate:.1%})",
                    "Positive Rate": f"{weekly_data.positive_rate:.1%} (target: {self.metrics.benchmark.target_positive_rate:.1%})",
                    "Meeting Rate": f"{weekly_data.meeting_rate:.1%} (target: {self.metrics.benchmark.target_meeting_rate:.1%})",
                },
                chart_type="table",
            ),
            ReportSection(
                title="Pipeline Impact",
                content=f"Pipeline created this week: ${weekly_data.pipeline_created:,.0f}",
                data={"pipeline_created": weekly_data.pipeline_created},
            ),
        ]

        # Generate recommendations based on comparison
        recommendations = []
        if comparison["reply_rate"]["status"] == "below":
            recommendations.append(
                "Reply rate is below target. Consider improving message personalization or testing new PQS approaches."
            )
        if comparison["prospects_researched"]["status"] == "below":
            recommendations.append(
                "Research volume is below target. Scale up prospecting activities."
            )
        if weekly_data.positive_rate < 0.05:
            recommendations.append(
                "Low positive response rate. Review messaging for value proposition clarity."
            )

        if not recommendations:
            recommendations.append("Performance is on target. Continue current approach.")

        summary = (
            f"This week: {weekly_data.messages_sent} messages sent with "
            f"{weekly_data.reply_rate:.1%} reply rate. "
            f"{weekly_data.meetings_booked} meetings booked."
        )

        return Report(
            title=f"Weekly Report - {week}",
            report_type="weekly",
            generated_at=datetime.now(),
            period=week,
            sections=sections,
            summary=summary,
            recommendations=recommendations,
        )

    def generate_recipe_comparison(self) -> Report:
        """Generate a recipe comparison report."""
        by_recipe = self.metrics.get_metrics_by_recipe()

        if not by_recipe:
            return Report(
                title="Recipe Comparison Report",
                report_type="recipe_comparison",
                generated_at=datetime.now(),
                period="All time",
                sections=[],
                summary="No recipe data available.",
                recommendations=["Tag metrics with recipe names to enable comparison."],
            )

        sections = []
        for recipe_name, data in by_recipe.items():
            sections.append(ReportSection(
                title=f"Recipe: {recipe_name}",
                content=f"Performance metrics for {recipe_name}",
                data={
                    "Messages Sent": int(data.get("messages_sent", 0)),
                    "Reply Rate": f"{data.get('reply_rate', 0):.1%}",
                    "Meeting Rate": f"{data.get('meeting_rate', 0):.1%}",
                },
                chart_type="table",
            ))

        # Find top performer
        top_recipe = max(
            by_recipe.items(),
            key=lambda x: x[1].get("reply_rate", 0),
        )

        recommendations = [
            f"Top performing recipe: {top_recipe[0]} with {top_recipe[1].get('reply_rate', 0):.1%} reply rate.",
            "Consider scaling the top recipe and testing variations.",
        ]

        return Report(
            title="Recipe Comparison Report",
            report_type="recipe_comparison",
            generated_at=datetime.now(),
            period="All time",
            sections=sections,
            summary=f"Compared {len(by_recipe)} recipes. Top performer: {top_recipe[0]}.",
            recommendations=recommendations,
        )

    def generate_improvement_report(self) -> Report:
        """Generate an improvement analysis report."""
        improvement = self.metrics.calculate_improvement()

        if improvement.get("insufficient_data"):
            return Report(
                title="Improvement Analysis",
                report_type="improvement",
                generated_at=datetime.now(),
                period="N/A",
                sections=[],
                summary="Insufficient data for improvement analysis.",
                recommendations=["Track metrics for at least 2 weeks to enable analysis."],
            )

        sections = [
            ReportSection(
                title="Period Analyzed",
                content=f"Analysis from {improvement['period']} ({improvement['weeks_tracked']} weeks)",
                data=None,
            ),
            ReportSection(
                title="Key Improvements",
                content="Change in key metrics over the analysis period.",
                data={
                    "Reply Rate Change": f"{improvement['reply_rate_change']:+.1f}%",
                    "Meeting Rate Change": f"{improvement['meeting_rate_change']:+.1f}%",
                    "Volume Change": f"{improvement['volume_change']:+.1f}%",
                    "vs Baseline": f"{improvement['vs_baseline_improvement']:.1f}x better than traditional outreach",
                },
                chart_type="table",
            ),
        ]

        recommendations = []
        if improvement["reply_rate_change"] > 0:
            recommendations.append(
                "Reply rate is improving. Document what's working and scale it."
            )
        else:
            recommendations.append(
                "Reply rate declining. Review recent changes and test alternatives."
            )

        if improvement["vs_baseline_improvement"] > 10:
            recommendations.append(
                f"Performing {improvement['vs_baseline_improvement']:.0f}x better than baseline. "
                "Consider expanding to new segments."
            )

        return Report(
            title="Improvement Analysis",
            report_type="improvement",
            generated_at=datetime.now(),
            period=improvement["period"],
            sections=sections,
            summary=(
                f"Over {improvement['weeks_tracked']} weeks: "
                f"reply rate changed {improvement['reply_rate_change']:+.1f}%, "
                f"performing {improvement['vs_baseline_improvement']:.1f}x vs baseline."
            ),
            recommendations=recommendations,
        )

    def generate_executive_summary(self) -> Report:
        """Generate an executive summary report."""
        current = self.metrics.get_current_week_metrics()
        improvement = self.metrics.calculate_improvement()
        by_recipe = self.metrics.get_metrics_by_recipe()

        sections = []

        # Current status
        if current:
            sections.append(ReportSection(
                title="Current Week Performance",
                content="Snapshot of this week's activity and results.",
                data={
                    "Messages Sent": current.messages_sent,
                    "Reply Rate": f"{current.reply_rate:.1%}",
                    "Meetings Booked": current.meetings_booked,
                    "Pipeline": f"${current.pipeline_created:,.0f}",
                },
                chart_type="table",
            ))

        # Improvement trend
        if not improvement.get("insufficient_data"):
            sections.append(ReportSection(
                title="Performance Trend",
                content=f"Changes over {improvement.get('weeks_tracked', 0)} weeks.",
                data={
                    "Reply Rate Trend": f"{improvement.get('reply_rate_change', 0):+.1f}%",
                    "vs Traditional Outreach": f"{improvement.get('vs_baseline_improvement', 0):.1f}x better",
                },
                chart_type="table",
            ))

        # Top recipes
        if by_recipe:
            top_recipes = sorted(
                by_recipe.items(),
                key=lambda x: x[1].get("reply_rate", 0),
                reverse=True,
            )[:3]

            sections.append(ReportSection(
                title="Top Performing Recipes",
                content="Best performing data recipes by reply rate.",
                data={
                    name: f"{data.get('reply_rate', 0):.1%} reply rate"
                    for name, data in top_recipes
                },
                chart_type="table",
            ))

        recommendations = [
            "Continue scaling top-performing recipes.",
            "Test new PQS/PVP variations monthly.",
            "Review and update data sources quarterly.",
        ]

        summary = "Executive overview of GTM framework performance."
        if current:
            summary = (
                f"Current week: {current.reply_rate:.1%} reply rate from "
                f"{current.messages_sent} messages."
            )

        return Report(
            title="Executive Summary",
            report_type="executive",
            generated_at=datetime.now(),
            period="Current",
            sections=sections,
            summary=summary,
            recommendations=recommendations,
        )

    def export_all_reports(self, output_dir: str) -> List[str]:
        """Generate and export all report types."""
        reports = [
            ("weekly_report.md", self.generate_weekly_report()),
            ("recipe_comparison.md", self.generate_recipe_comparison()),
            ("improvement_analysis.md", self.generate_improvement_report()),
            ("executive_summary.md", self.generate_executive_summary()),
        ]

        exported = []
        for filename, report in reports:
            filepath = f"{output_dir}/{filename}"
            with open(filepath, "w") as f:
                f.write(report.to_markdown())
            exported.append(filepath)

        return exported
