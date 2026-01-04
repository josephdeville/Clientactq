"""
ClayWorks Framework - Main Entry Point
======================================

A comprehensive Go-To-Market (GTM) framework based on Jordan Crawford's
Blueprint methodology.

Usage:
    from clayworks import ClayWorks

    # Initialize the framework
    cw = ClayWorks(client_name="Acme Corp")

    # Start discovery phase
    cw.start_discovery()

    # Create a data recipe
    recipe = cw.create_recipe(
        name="Compliance Deadline",
        target_outcome="Companies facing compliance deadlines",
    )

    # Generate messages
    messages = cw.generate_messages(prospects, recipe)
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from .core import ClayWorksConfig, ProspectScorer, PQSFramework, PVPFramework
from .data import DataSourceManager, DataRecipeBuilder, EnrichmentPipeline
from .messaging import MessageGenerator, PersonalizationEngine
from .workflows import DiscoveryPhase, RecipeDevPhase, AutomationPhase, ScalePhase
from .analytics import MetricsTracker, ReportGenerator
from .clients import ClientIntake, ProposalGenerator


class ClayWorks:
    """
    Main ClayWorks Framework class.

    This is the primary interface for working with the ClayWorks GTM framework.
    It orchestrates all components and provides a unified API.
    """

    def __init__(
        self,
        client_name: str,
        vertical: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        """
        Initialize the ClayWorks framework.

        Args:
            client_name: Name of the client
            vertical: Industry vertical
            config_path: Path to configuration file
        """
        self.client_name = client_name
        self.vertical = vertical
        self.created_at = datetime.now()

        # Initialize configuration
        self.config = ClayWorksConfig(config_path)
        self.config.client_name = client_name
        if vertical:
            self.config.vertical = vertical

        # Initialize core frameworks
        self.pqs = PQSFramework()
        self.pvp = PVPFramework()
        self.scorer = ProspectScorer()

        # Initialize data components
        self.data_sources = DataSourceManager()
        self.recipe_builder = DataRecipeBuilder()
        self.enrichment = EnrichmentPipeline()

        # Initialize messaging
        self.message_generator = MessageGenerator()
        self.personalization = PersonalizationEngine()

        # Initialize workflows
        self.discovery: Optional[DiscoveryPhase] = None
        self.recipe_dev: Optional[RecipeDevPhase] = None
        self.automation: Optional[AutomationPhase] = None
        self.scale: Optional[ScalePhase] = None

        # Initialize analytics
        self.metrics = MetricsTracker(client_name)

        # Initialize client tools
        self.intake = ClientIntake()
        self.proposal_generator = ProposalGenerator(self.intake)

    # ==========================================================================
    # Workflow Management
    # ==========================================================================

    def start_discovery(self) -> DiscoveryPhase:
        """Start the Discovery phase (Phase 1)."""
        self.discovery = DiscoveryPhase(self.client_name)
        self.discovery.start()
        return self.discovery

    def start_recipe_dev(self) -> RecipeDevPhase:
        """Start the Recipe Development phase (Phase 2)."""
        if self.discovery:
            readiness = self.discovery.validate_readiness()
            if not readiness["ready"]:
                print(f"Warning: Discovery phase not complete. Issues: {readiness['issues']}")

        self.recipe_dev = RecipeDevPhase(self.client_name)
        self.recipe_dev.start()
        return self.recipe_dev

    def start_automation(self) -> AutomationPhase:
        """Start the Automation phase (Phase 3)."""
        if self.recipe_dev:
            readiness = self.recipe_dev.validate_readiness()
            if not readiness["ready"]:
                print(f"Warning: Recipe dev phase not complete. Issues: {readiness['issues']}")

        self.automation = AutomationPhase(self.client_name)
        self.automation.start()
        return self.automation

    def start_scale(self) -> ScalePhase:
        """Start the Scale phase (Phase 4)."""
        if self.automation:
            readiness = self.automation.validate_readiness()
            if not readiness["ready"]:
                print(f"Warning: Automation phase not complete. Issues: {readiness['issues']}")

        self.scale = ScalePhase(self.client_name)
        self.scale.start()
        return self.scale

    def get_phase_status(self) -> Dict[str, Any]:
        """Get the status of all phases."""
        return {
            "discovery": {
                "active": self.discovery is not None,
                "progress": self.discovery.get_progress() if self.discovery else None,
            },
            "recipe_dev": {
                "active": self.recipe_dev is not None,
                "metrics": self.recipe_dev.get_all_metrics() if self.recipe_dev else None,
            },
            "automation": {
                "active": self.automation is not None,
                "workflows": self.automation.get_workflow_metrics() if self.automation else None,
            },
            "scale": {
                "active": self.scale is not None,
                "sequences": self.scale.get_sequence_metrics() if self.scale else None,
            },
        }

    # ==========================================================================
    # Data Recipe Management
    # ==========================================================================

    def create_recipe(
        self,
        name: str,
        target_outcome: str,
        target_persona: str = "",
        **kwargs,
    ):
        """
        Create a new data recipe.

        Args:
            name: Recipe name
            target_outcome: What situation we're identifying
            target_persona: Target buyer persona
            **kwargs: Additional recipe parameters
        """
        return (
            self.recipe_builder
            .name(name)
            .target_outcome(target_outcome)
            .target_persona(target_persona)
        )

    # ==========================================================================
    # Message Generation
    # ==========================================================================

    def generate_pqs_message(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_name: str = "compliance_deadline",
    ):
        """Generate a PQS message for a prospect."""
        return self.message_generator.generate_pqs(
            prospect_id=prospect_id,
            prospect_data=prospect_data,
            template_name=template_name,
        )

    def generate_pvp_message(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
        template_name: str = "tech_stack_audit",
    ):
        """Generate a PVP message for a prospect."""
        return self.message_generator.generate_pvp(
            prospect_id=prospect_id,
            prospect_data=prospect_data,
            template_name=template_name,
        )

    def generate_messages_batch(
        self,
        prospects: List[Dict[str, Any]],
        template_key: str,
        id_field: str = "id",
    ):
        """Generate messages for multiple prospects."""
        return self.message_generator.generate_batch(
            prospects=prospects,
            template_key=template_key,
            id_field=id_field,
        )

    # ==========================================================================
    # Prospect Scoring
    # ==========================================================================

    def score_prospect(
        self,
        prospect_id: str,
        prospect_data: Dict[str, Any],
    ):
        """Score a single prospect."""
        return self.scorer.score_prospect(prospect_id, prospect_data)

    def score_prospects(
        self,
        prospects: List[Dict[str, Any]],
        id_field: str = "id",
    ):
        """Score multiple prospects and return sorted by score."""
        return self.scorer.score_batch(prospects, id_field)

    def get_qualified_prospects(
        self,
        prospects: List[Dict[str, Any]],
        id_field: str = "id",
    ):
        """Get only prospects that meet the scoring threshold."""
        return self.scorer.get_qualified_prospects(prospects, id_field)

    # ==========================================================================
    # Analytics and Reporting
    # ==========================================================================

    def record_metric(
        self,
        metric_type: str,
        value: float,
        recipe_name: Optional[str] = None,
    ):
        """Record a metric."""
        from .analytics.metrics import MetricType
        self.metrics.record_metric(
            metric_type=MetricType(metric_type),
            value=value,
            recipe_name=recipe_name,
        )

    def get_weekly_report(self, week: Optional[str] = None):
        """Generate a weekly performance report."""
        report_gen = ReportGenerator(self.metrics)
        return report_gen.generate_weekly_report(week)

    def get_executive_summary(self):
        """Generate an executive summary report."""
        report_gen = ReportGenerator(self.metrics)
        return report_gen.generate_executive_summary()

    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for a metrics dashboard."""
        return self.metrics.generate_dashboard_data()

    # ==========================================================================
    # Client Tools
    # ==========================================================================

    def start_intake(self) -> ClientIntake:
        """Start a new client intake."""
        self.intake.start_intake(self.client_name)
        return self.intake

    def generate_proposal(self, custom_examples: Optional[List[Dict[str, str]]] = None):
        """Generate a client proposal."""
        intake_data = self.intake.get_intake(self.client_name)
        return self.proposal_generator.generate(
            client_name=self.client_name,
            intake_data=intake_data,
            custom_examples=custom_examples,
        )

    # ==========================================================================
    # Export and Import
    # ==========================================================================

    def export_config(self, filepath: str):
        """Export configuration to file."""
        self.config.save_to_file(filepath)

    def export_metrics(self, filepath: str):
        """Export metrics to file."""
        self.metrics.export_data(filepath)

    def export_data_sources(self, filepath: str):
        """Export data sources to file."""
        self.data_sources.export_sources(filepath)


def create_framework(
    client_name: str,
    vertical: Optional[str] = None,
) -> ClayWorks:
    """
    Create a new ClayWorks framework instance.

    This is the recommended way to initialize the framework.

    Args:
        client_name: Name of the client
        vertical: Industry vertical

    Returns:
        Configured ClayWorks instance
    """
    return ClayWorks(client_name=client_name, vertical=vertical)


# Convenience function for quick start
def quick_start(client_name: str) -> ClayWorks:
    """
    Quick start the ClayWorks framework with sensible defaults.

    Args:
        client_name: Name of the client

    Returns:
        Ready-to-use ClayWorks instance
    """
    cw = create_framework(client_name)

    # Add common data sources
    from .data.sources import COMMON_SOURCES
    for source in COMMON_SOURCES.values():
        cw.data_sources.add_source(source)

    # Set up default scoring
    from .core.scoring import create_default_scorer
    cw.scorer = create_default_scorer()

    return cw
