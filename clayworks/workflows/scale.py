"""
ClayWorks Scale Phase Module
============================

Phase 4: Scale

OBJECTIVES:
- Expand to multi-channel outreach
- Build monitoring for trigger events
- Document processes for team adoption
- Prepare for ongoing operations

DELIVERABLES:
- Multi-channel sequences (email + LinkedIn + ads)
- Event monitoring dashboards
- Team training documentation
- Ongoing maintenance playbook
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class Channel(Enum):
    """Outreach channels."""
    EMAIL = "email"
    LINKEDIN = "linkedin"
    LINKEDIN_INMAIL = "linkedin_inmail"
    PHONE = "phone"
    ADS = "ads"
    DIRECT_MAIL = "direct_mail"


class TriggerType(Enum):
    """Types of trigger events to monitor."""
    JOB_POSTING = "job_posting"
    FUNDING_ROUND = "funding_round"
    LEADERSHIP_CHANGE = "leadership_change"
    TECH_CHANGE = "tech_change"
    CONTRACT_AWARD = "contract_award"
    EXPANSION = "expansion"
    ACQUISITION = "acquisition"


@dataclass
class SequenceStep:
    """A step in a multi-channel sequence."""
    step_number: int
    channel: Channel
    wait_days: int  # Days to wait from previous step
    action: str  # send_email, send_connection, send_inmail, etc.
    content_template: str
    fallback_action: Optional[str] = None


@dataclass
class MultiChannelSequence:
    """A multi-channel outreach sequence."""
    name: str
    description: str
    target_segment: str
    steps: List[SequenceStep] = field(default_factory=list)
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    # Metrics
    prospects_enrolled: int = 0
    prospects_completed: int = 0
    total_touches: int = 0
    responses: int = 0
    meetings: int = 0

    @property
    def response_rate(self) -> float:
        return self.responses / self.prospects_enrolled if self.prospects_enrolled > 0 else 0

    @property
    def meeting_rate(self) -> float:
        return self.meetings / self.prospects_enrolled if self.prospects_enrolled > 0 else 0


@dataclass
class TriggerMonitor:
    """A trigger event monitor."""
    name: str
    trigger_type: TriggerType
    source: str  # Data source to monitor
    criteria: Dict[str, Any]
    recipe_to_trigger: str  # Which recipe to run when triggered
    active: bool = True
    events_detected: int = 0
    prospects_added: int = 0


@dataclass
class TrainingModule:
    """A training module for team adoption."""
    name: str
    description: str
    content_type: str  # video, document, workshop
    duration_minutes: int
    topics: List[str]
    completed_by: List[str] = field(default_factory=list)


class ScalePhase:
    """
    Phase 4: Scale

    Activities:
    Week 7:
    - Add LinkedIn outreach to sequences
    - Set up trigger monitoring (new contracts, job posts, etc.)
    - Create sales handoff process
    - Document all workflows and recipes

    Week 8:
    - Train sales team on new process
    - Establish weekly review cadence
    - Create case study templates for wins
    - Plan quarterly expansion to new segments
    """

    def __init__(self, client_name: str):
        self.client_name = client_name
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None

        # Multi-channel sequences
        self.sequences: List[MultiChannelSequence] = []

        # Trigger monitors
        self.monitors: List[TriggerMonitor] = []

        # Training modules
        self.training_modules: List[TrainingModule] = []

        # Documentation
        self.documentation: Dict[str, str] = {}

        # Handoff process
        self.handoff_criteria: Dict[str, Any] = {}

        # Review cadence
        self.review_schedule: Dict[str, Any] = {}

    def start(self) -> None:
        """Start the scale phase."""
        self.started_at = datetime.now()

    def complete(self) -> None:
        """Mark the phase as complete."""
        self.completed_at = datetime.now()

    def create_sequence(
        self,
        name: str,
        description: str,
        target_segment: str,
        steps: List[Dict[str, Any]],
    ) -> MultiChannelSequence:
        """Create a multi-channel sequence."""
        sequence = MultiChannelSequence(
            name=name,
            description=description,
            target_segment=target_segment,
            steps=[
                SequenceStep(
                    step_number=i + 1,
                    channel=Channel(s["channel"]),
                    wait_days=s.get("wait_days", 0),
                    action=s["action"],
                    content_template=s.get("content_template", ""),
                )
                for i, s in enumerate(steps)
            ],
        )
        self.sequences.append(sequence)
        return sequence

    def add_trigger_monitor(
        self,
        name: str,
        trigger_type: TriggerType,
        source: str,
        criteria: Dict[str, Any],
        recipe_to_trigger: str,
    ) -> TriggerMonitor:
        """Add a trigger event monitor."""
        monitor = TriggerMonitor(
            name=name,
            trigger_type=trigger_type,
            source=source,
            criteria=criteria,
            recipe_to_trigger=recipe_to_trigger,
        )
        self.monitors.append(monitor)
        return monitor

    def add_training_module(
        self,
        name: str,
        description: str,
        content_type: str,
        duration_minutes: int,
        topics: List[str],
    ) -> TrainingModule:
        """Add a training module."""
        module = TrainingModule(
            name=name,
            description=description,
            content_type=content_type,
            duration_minutes=duration_minutes,
            topics=topics,
        )
        self.training_modules.append(module)
        return module

    def set_handoff_criteria(
        self,
        qualified_score: int,
        required_interactions: int,
        required_signals: List[str],
        handoff_actions: List[str],
    ) -> None:
        """Define the sales handoff criteria."""
        self.handoff_criteria = {
            "qualified_score": qualified_score,
            "required_interactions": required_interactions,
            "required_signals": required_signals,
            "handoff_actions": handoff_actions,
            "set_at": datetime.now().isoformat(),
        }

    def set_review_schedule(
        self,
        weekly_review_day: str,
        monthly_review_day: int,
        quarterly_planning_month: int,
        review_agenda: List[str],
    ) -> None:
        """Set the review cadence."""
        self.review_schedule = {
            "weekly_review_day": weekly_review_day,
            "monthly_review_day": monthly_review_day,
            "quarterly_planning_month": quarterly_planning_month,
            "review_agenda": review_agenda,
        }

    def add_documentation(self, doc_name: str, content: str) -> None:
        """Add documentation."""
        self.documentation[doc_name] = content

    def get_sequence_metrics(self) -> Dict[str, Any]:
        """Get metrics for all sequences."""
        return {
            "total_sequences": len(self.sequences),
            "active_sequences": sum(1 for s in self.sequences if s.active),
            "total_prospects": sum(s.prospects_enrolled for s in self.sequences),
            "total_responses": sum(s.responses for s in self.sequences),
            "total_meetings": sum(s.meetings for s in self.sequences),
            "sequences": [
                {
                    "name": s.name,
                    "segment": s.target_segment,
                    "channels": list(set(step.channel.value for step in s.steps)),
                    "enrolled": s.prospects_enrolled,
                    "response_rate": s.response_rate,
                    "meeting_rate": s.meeting_rate,
                }
                for s in self.sequences
            ],
        }

    def get_monitor_metrics(self) -> Dict[str, Any]:
        """Get metrics for trigger monitors."""
        return {
            "total_monitors": len(self.monitors),
            "active_monitors": sum(1 for m in self.monitors if m.active),
            "total_events_detected": sum(m.events_detected for m in self.monitors),
            "total_prospects_added": sum(m.prospects_added for m in self.monitors),
            "monitors": [
                {
                    "name": m.name,
                    "type": m.trigger_type.value,
                    "active": m.active,
                    "events": m.events_detected,
                    "prospects": m.prospects_added,
                }
                for m in self.monitors
            ],
        }

    def get_training_status(self) -> Dict[str, Any]:
        """Get training module status."""
        return {
            "total_modules": len(self.training_modules),
            "total_duration_minutes": sum(
                m.duration_minutes for m in self.training_modules
            ),
            "modules": [
                {
                    "name": m.name,
                    "type": m.content_type,
                    "duration": m.duration_minutes,
                    "completed_by_count": len(m.completed_by),
                }
                for m in self.training_modules
            ],
        }

    def generate_playbook(self) -> Dict[str, Any]:
        """Generate the maintenance playbook."""
        return {
            "title": f"{self.client_name} GTM Playbook",
            "generated_at": datetime.now().isoformat(),
            "sections": {
                "overview": {
                    "sequences": len(self.sequences),
                    "monitors": len(self.monitors),
                    "documentation": list(self.documentation.keys()),
                },
                "sequences": [
                    {
                        "name": s.name,
                        "steps": [
                            f"Step {step.step_number}: {step.channel.value} - {step.action}"
                            for step in s.steps
                        ],
                    }
                    for s in self.sequences
                ],
                "trigger_monitors": [
                    {
                        "name": m.name,
                        "type": m.trigger_type.value,
                        "criteria": m.criteria,
                    }
                    for m in self.monitors
                ],
                "handoff_process": self.handoff_criteria,
                "review_cadence": self.review_schedule,
                "training": [m.name for m in self.training_modules],
            },
        }

    def validate_completion(self) -> Dict[str, Any]:
        """Validate that all scale phase requirements are met."""
        issues = []

        # Check multi-channel sequences
        if not self.sequences:
            issues.append("No multi-channel sequences defined")
        else:
            for seq in self.sequences:
                channels = set(step.channel for step in seq.steps)
                if len(channels) < 2:
                    issues.append(f"Sequence '{seq.name}' uses only 1 channel")

        # Check trigger monitors
        if not self.monitors:
            issues.append("No trigger monitors configured")

        # Check handoff criteria
        if not self.handoff_criteria:
            issues.append("Sales handoff criteria not defined")

        # Check documentation
        required_docs = [
            "workflow_documentation",
            "recipe_documentation",
            "maintenance_procedures",
        ]
        for doc in required_docs:
            if doc not in self.documentation:
                issues.append(f"Missing documentation: {doc}")

        # Check training
        if not self.training_modules:
            issues.append("No training modules defined")

        return {
            "complete": len(issues) == 0,
            "issues": issues,
            "metrics": {
                "sequences": self.get_sequence_metrics(),
                "monitors": self.get_monitor_metrics(),
                "training": self.get_training_status(),
            },
            "playbook": self.generate_playbook(),
        }
