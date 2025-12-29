"""
ClayWorks Automation Phase Module
=================================

Phase 3: Automation MVP

OBJECTIVES:
- Build automated workflows for validated recipes
- Create message templates with dynamic personalization
- Establish testing protocols
- Deploy to small test segments

DELIVERABLES:
- Clay/n8n workflows for each validated recipe
- Message templates with variable insertion points
- A/B testing framework
- Automated prospect scoring model
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum


class WorkflowStatus(Enum):
    """Status of an automation workflow."""
    DRAFT = "draft"
    TESTING = "testing"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class ABTestStatus(Enum):
    """Status of an A/B test."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    WINNER_SELECTED = "winner_selected"


@dataclass
class WorkflowStep:
    """A step in an automation workflow."""
    name: str
    step_type: str  # trigger, enrichment, filter, action
    config: Dict[str, Any]
    order: int
    enabled: bool = True


@dataclass
class AutomationWorkflow:
    """An automation workflow definition."""
    name: str
    recipe_name: str
    description: str
    trigger_type: str  # scheduled, webhook, manual
    trigger_config: Dict[str, Any]
    steps: List[WorkflowStep] = field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.DRAFT
    created_at: datetime = field(default_factory=datetime.now)
    last_run_at: Optional[datetime] = None
    prospects_processed: int = 0
    messages_sent: int = 0

    def add_step(self, step: WorkflowStep) -> None:
        """Add a step to the workflow."""
        step.order = len(self.steps)
        self.steps.append(step)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "recipe_name": self.recipe_name,
            "description": self.description,
            "trigger_type": self.trigger_type,
            "status": self.status.value,
            "steps": [
                {
                    "name": s.name,
                    "type": s.step_type,
                    "order": s.order,
                    "enabled": s.enabled,
                }
                for s in self.steps
            ],
            "prospects_processed": self.prospects_processed,
            "messages_sent": self.messages_sent,
        }


@dataclass
class MessageVariant:
    """A message variant for A/B testing."""
    variant_id: str
    variant_name: str
    subject: str
    body: str
    sends: int = 0
    opens: int = 0
    replies: int = 0
    meetings: int = 0

    @property
    def open_rate(self) -> float:
        return self.opens / self.sends if self.sends > 0 else 0

    @property
    def reply_rate(self) -> float:
        return self.replies / self.sends if self.sends > 0 else 0


@dataclass
class ABTest:
    """An A/B test definition."""
    test_id: str
    test_name: str
    recipe_name: str
    test_element: str  # subject, hook, cta, full_message
    variants: List[MessageVariant]
    status: ABTestStatus = ABTestStatus.PENDING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    winner_variant_id: Optional[str] = None
    minimum_sample_size: int = 25
    significance_threshold: float = 0.95

    def get_winner(self) -> Optional[MessageVariant]:
        """Get the winning variant based on reply rate."""
        if not self.variants:
            return None

        # Check if minimum sample size met
        for variant in self.variants:
            if variant.sends < self.minimum_sample_size:
                return None

        # Return variant with highest reply rate
        sorted_variants = sorted(
            self.variants, key=lambda v: v.reply_rate, reverse=True
        )
        return sorted_variants[0]


class AutomationPhase:
    """
    Phase 3: Automation MVP

    Activities:
    Week 5:
    - Build Clay table with data source integrations
    - Create scoring model (0-100 based on signals)
    - Build message templates with merge fields
    - Test workflow end-to-end with sample data

    Week 6:
    - Deploy to 25-50 prospects weekly
    - Set up response tracking
    - Create A/B test variants (subject lines, hooks, CTAs)
    - Document workflow maintenance procedures
    """

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # Workflows
        self.workflows: List[AutomationWorkflow] = []

        # A/B tests
        self.ab_tests: List[ABTest] = []

        # Scoring model
        self.scoring_model: Dict[str, Any] = {}

        # Templates
        self.message_templates: Dict[str, Dict[str, str]] = {}

    def start(self) -> None:
        """Start the automation phase."""
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark the phase as complete."""
        self.completed_at = datetime.now()

    def create_workflow(
        self,
        name: str,
        recipe_name: str,
        description: str,
        trigger_type: str = "scheduled",
        trigger_config: Optional[Dict[str, Any]] = None,
    ) -> AutomationWorkflow:
        """Create a new automation workflow."""
        workflow = AutomationWorkflow(
            name=name,
            recipe_name=recipe_name,
            description=description,
            trigger_type=trigger_type,
            trigger_config=trigger_config or {},
        )
        self.workflows.append(workflow)
        return workflow

    def add_workflow_step(
        self,
        workflow_name: str,
        step_name: str,
        step_type: str,
        config: Dict[str, Any],
    ) -> None:
        """Add a step to a workflow."""
        for workflow in self.workflows:
            if workflow.name == workflow_name:
                step = WorkflowStep(
                    name=step_name,
                    step_type=step_type,
                    config=config,
                    order=len(workflow.steps),
                )
                workflow.add_step(step)
                break

    def set_scoring_model(
        self,
        components: List[Dict[str, Any]],
        threshold: int = 70,
    ) -> None:
        """Set up the automated scoring model."""
        self.scoring_model = {
            "components": components,
            "threshold": threshold,
            "max_score": sum(c.get("points", 0) for c in components),
            "created_at": datetime.now().isoformat(),
        }

    def add_message_template(
        self,
        template_name: str,
        subject: str,
        body: str,
        variables: List[str],
    ) -> None:
        """Add a message template."""
        self.message_templates[template_name] = {
            "subject": subject,
            "body": body,
            "variables": variables,
            "created_at": datetime.now().isoformat(),
        }

    def create_ab_test(
        self,
        test_name: str,
        recipe_name: str,
        test_element: str,
        variants: List[Dict[str, str]],
    ) -> ABTest:
        """Create a new A/B test."""
        test = ABTest(
            test_id=f"ab_{len(self.ab_tests) + 1}",
            test_name=test_name,
            recipe_name=recipe_name,
            test_element=test_element,
            variants=[
                MessageVariant(
                    variant_id=f"v{i}",
                    variant_name=v.get("name", f"Variant {i}"),
                    subject=v.get("subject", ""),
                    body=v.get("body", ""),
                )
                for i, v in enumerate(variants)
            ],
        )
        self.ab_tests.append(test)
        return test

    def update_ab_test_metrics(
        self,
        test_id: str,
        variant_id: str,
        sends: int = 0,
        opens: int = 0,
        replies: int = 0,
        meetings: int = 0,
    ) -> None:
        """Update metrics for an A/B test variant."""
        for test in self.ab_tests:
            if test.test_id == test_id:
                for variant in test.variants:
                    if variant.variant_id == variant_id:
                        variant.sends += sends
                        variant.opens += opens
                        variant.replies += replies
                        variant.meetings += meetings
                        break

    def get_workflow_metrics(self) -> Dict[str, Any]:
        """Get metrics for all workflows."""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": sum(
                1 for w in self.workflows if w.status == WorkflowStatus.ACTIVE
            ),
            "total_prospects_processed": sum(
                w.prospects_processed for w in self.workflows
            ),
            "total_messages_sent": sum(
                w.messages_sent for w in self.workflows
            ),
            "workflows": [w.to_dict() for w in self.workflows],
        }

    def get_ab_test_results(self) -> List[Dict[str, Any]]:
        """Get results for all A/B tests."""
        results = []
        for test in self.ab_tests:
            winner = test.get_winner()
            results.append({
                "test_id": test.test_id,
                "test_name": test.test_name,
                "test_element": test.test_element,
                "status": test.status.value,
                "variants": [
                    {
                        "id": v.variant_id,
                        "name": v.variant_name,
                        "sends": v.sends,
                        "reply_rate": v.reply_rate,
                    }
                    for v in test.variants
                ],
                "winner": winner.variant_name if winner else None,
            })
        return results

    def activate_workflow(self, workflow_name: str) -> bool:
        """Activate a workflow for production use."""
        for workflow in self.workflows:
            if workflow.name == workflow_name:
                workflow.status = WorkflowStatus.ACTIVE
                return True
        return False

    def generate_workflow_template(
        self, workflow_name: str, platform: str = "clay"
    ) -> Dict[str, Any]:
        """Generate a workflow template for Clay/n8n."""
        for workflow in self.workflows:
            if workflow.name == workflow_name:
                if platform == "clay":
                    return self._generate_clay_template(workflow)
                elif platform == "n8n":
                    return self._generate_n8n_template(workflow)
        return {}

    def _generate_clay_template(
        self, workflow: AutomationWorkflow
    ) -> Dict[str, Any]:
        """Generate Clay table template."""
        return {
            "platform": "clay",
            "table_name": workflow.name,
            "columns": [
                {"name": "Company", "type": "text", "source": "input"},
                {"name": "Domain", "type": "url", "source": "input"},
                {"name": "Contact Email", "type": "email", "source": "enrichment"},
                {"name": "Score", "type": "number", "source": "formula"},
                {"name": "Message", "type": "text", "source": "ai"},
            ],
            "enrichments": [
                {
                    "step": step.name,
                    "type": step.step_type,
                    "config": step.config,
                }
                for step in workflow.steps
                if step.step_type == "enrichment"
            ],
            "filters": [
                step.config
                for step in workflow.steps
                if step.step_type == "filter"
            ],
            "scoring": self.scoring_model,
        }

    def _generate_n8n_template(
        self, workflow: AutomationWorkflow
    ) -> Dict[str, Any]:
        """Generate n8n workflow template."""
        nodes = []
        connections = {}

        # Add trigger node
        nodes.append({
            "id": "trigger",
            "type": f"n8n-nodes-base.{workflow.trigger_type}Trigger",
            "position": [0, 0],
            "parameters": workflow.trigger_config,
        })

        # Add step nodes
        prev_node = "trigger"
        for i, step in enumerate(workflow.steps):
            node_id = f"step_{i}"
            nodes.append({
                "id": node_id,
                "type": f"n8n-nodes-base.{step.step_type}",
                "position": [(i + 1) * 200, 0],
                "parameters": step.config,
            })
            connections[prev_node] = {"main": [[{"node": node_id, "type": "main", "index": 0}]]}
            prev_node = node_id

        return {
            "platform": "n8n",
            "name": workflow.name,
            "nodes": nodes,
            "connections": connections,
        }

    def validate_readiness(self) -> Dict[str, Any]:
        """Validate readiness to proceed to Phase 4."""
        issues = []

        active_workflows = [
            w for w in self.workflows if w.status == WorkflowStatus.ACTIVE
        ]
        if not active_workflows:
            issues.append("Need at least 1 active workflow")

        if not self.scoring_model:
            issues.append("Scoring model not configured")

        if not self.message_templates:
            issues.append("No message templates defined")

        total_sent = sum(w.messages_sent for w in self.workflows)
        if total_sent < 25:
            issues.append(f"Need at least 25 automated messages sent (have {total_sent})")

        return {
            "ready": len(issues) == 0,
            "issues": issues,
            "active_workflows": [w.name for w in active_workflows],
            "metrics": self.get_workflow_metrics(),
        }
