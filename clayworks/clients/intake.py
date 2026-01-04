"""
ClayWorks Client Intake Module
==============================

Client intake questionnaire processing for gathering information
before building a proposal.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class IntakeQuestion:
    """A question in the intake questionnaire."""
    id: str
    category: str
    question: str
    required: bool = True
    question_type: str = "text"  # text, number, list, multi_select
    options: List[str] = field(default_factory=list)
    help_text: str = ""


@dataclass
class IntakeResponse:
    """A response to an intake question."""
    question_id: str
    response: Any
    responded_at: datetime = field(default_factory=datetime.now)


@dataclass
class IntakeData:
    """Complete intake data for a client."""
    client_name: str
    responses: Dict[str, IntakeResponse] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def get_response(self, question_id: str) -> Optional[Any]:
        """Get the response for a specific question."""
        response = self.responses.get(question_id)
        return response.response if response else None

    def is_complete(self, required_questions: List[str]) -> bool:
        """Check if all required questions have been answered."""
        return all(q in self.responses for q in required_questions)


class ClientIntake:
    """
    Client Intake Questionnaire.

    Categories:
    1. COMPANY BASICS
    2. ICP DEFINITION
    3. CURRENT GTM
    4. PAIN POINTS & TRIGGERS
    5. DATA & SIGNALS
    6. COMPETITIVE LANDSCAPE
    7. SUCCESS PATTERNS
    """

    def __init__(self):
        self.questions: List[IntakeQuestion] = self._build_questions()
        self.intakes: Dict[str, IntakeData] = {}

    def _build_questions(self) -> List[IntakeQuestion]:
        """Build the intake questionnaire."""
        return [
            # COMPANY BASICS
            IntakeQuestion(
                id="company_name",
                category="Company Basics",
                question="Company name and website",
                required=True,
            ),
            IntakeQuestion(
                id="product_description",
                category="Company Basics",
                question="What do you sell? (1-2 sentences)",
                required=True,
            ),
            IntakeQuestion(
                id="avg_deal_size",
                category="Company Basics",
                question="Average deal size",
                question_type="number",
                required=True,
            ),
            IntakeQuestion(
                id="sales_cycle_length",
                category="Company Basics",
                question="Sales cycle length (days)",
                question_type="number",
                required=True,
            ),
            IntakeQuestion(
                id="team_size",
                category="Company Basics",
                question="Current team size (sales, marketing, ops)",
                required=True,
            ),

            # ICP DEFINITION
            IntakeQuestion(
                id="ideal_customer",
                category="ICP Definition",
                question="Describe your ideal customer in detail",
                required=True,
            ),
            IntakeQuestion(
                id="target_industries",
                category="ICP Definition",
                question="What industries/verticals do you serve?",
                question_type="list",
                required=True,
            ),
            IntakeQuestion(
                id="company_size_sweet_spot",
                category="ICP Definition",
                question="Company size sweet spot (employees, revenue)",
                required=True,
            ),
            IntakeQuestion(
                id="primary_buyer",
                category="ICP Definition",
                question="Who is your primary buyer (title, role)?",
                required=True,
            ),
            IntakeQuestion(
                id="buying_committee",
                category="ICP Definition",
                question="Who else is involved in buying decisions?",
                question_type="list",
            ),

            # CURRENT GTM
            IntakeQuestion(
                id="lead_gen_methods",
                category="Current GTM",
                question="How do you currently generate leads?",
                question_type="list",
                required=True,
            ),
            IntakeQuestion(
                id="current_tools",
                category="Current GTM",
                question="What tools do you use? (CRM, outreach, data)",
                question_type="list",
                required=True,
            ),
            IntakeQuestion(
                id="current_response_rates",
                category="Current GTM",
                question="Current response rates on outbound",
                question_type="number",
            ),
            IntakeQuestion(
                id="whats_working",
                category="Current GTM",
                question="What's working well today?",
            ),
            IntakeQuestion(
                id="whats_not_working",
                category="Current GTM",
                question="What's not working?",
                required=True,
            ),

            # PAIN POINTS & TRIGGERS
            IntakeQuestion(
                id="problem_solved",
                category="Pain Points & Triggers",
                question="What specific problem do you solve?",
                required=True,
            ),
            IntakeQuestion(
                id="buying_triggers",
                category="Pain Points & Triggers",
                question="What triggers a company to need your solution?",
                question_type="list",
                required=True,
            ),
            IntakeQuestion(
                id="external_events",
                category="Pain Points & Triggers",
                question="What external events/deadlines affect your buyers?",
                question_type="list",
            ),
            IntakeQuestion(
                id="alternatives_tried",
                category="Pain Points & Triggers",
                question="What do prospects typically try before buying from you?",
                question_type="list",
            ),
            IntakeQuestion(
                id="deal_stall_reasons",
                category="Pain Points & Triggers",
                question="Why do deals stall or get lost?",
                question_type="list",
            ),

            # DATA & SIGNALS
            IntakeQuestion(
                id="public_data_sources",
                category="Data & Signals",
                question="What public data exists about your target companies?",
                question_type="list",
            ),
            IntakeQuestion(
                id="industry_databases",
                category="Data & Signals",
                question="Are there industry databases or registries relevant to your buyers?",
                question_type="list",
            ),
            IntakeQuestion(
                id="signal_job_titles",
                category="Data & Signals",
                question="What job titles indicate a company needs your solution?",
                question_type="list",
            ),
            IntakeQuestion(
                id="good_fit_tech",
                category="Data & Signals",
                question="What technology stack signals a good fit?",
                question_type="list",
            ),
            IntakeQuestion(
                id="bad_fit_tech",
                category="Data & Signals",
                question="What technology stack signals a bad fit?",
                question_type="list",
            ),

            # COMPETITIVE LANDSCAPE
            IntakeQuestion(
                id="main_competitors",
                category="Competitive Landscape",
                question="Who are your main competitors?",
                question_type="list",
                required=True,
            ),
            IntakeQuestion(
                id="how_prospects_find_alternatives",
                category="Competitive Landscape",
                question="How do prospects typically find alternatives?",
            ),
            IntakeQuestion(
                id="competitive_advantage",
                category="Competitive Landscape",
                question="What do you do better than competitors?",
                required=True,
            ),
            IntakeQuestion(
                id="competitor_positioning",
                category="Competitive Landscape",
                question="What do competitors say about themselves?",
            ),

            # SUCCESS PATTERNS
            IntakeQuestion(
                id="best_customer_stories",
                category="Success Patterns",
                question="Describe your last 3 best customers—how did they find you?",
                required=True,
            ),
            IntakeQuestion(
                id="common_characteristics",
                category="Success Patterns",
                question="What did those customers have in common?",
                question_type="list",
            ),
            IntakeQuestion(
                id="aha_moment",
                category="Success Patterns",
                question='What was the "aha moment" that made them buy?',
                required=True,
            ),
        ]

    def start_intake(self, client_name: str) -> IntakeData:
        """Start a new intake for a client."""
        intake = IntakeData(client_name=client_name)
        self.intakes[client_name] = intake
        return intake

    def get_questions_by_category(self) -> Dict[str, List[IntakeQuestion]]:
        """Get questions organized by category."""
        categories: Dict[str, List[IntakeQuestion]] = {}
        for q in self.questions:
            if q.category not in categories:
                categories[q.category] = []
            categories[q.category].append(q)
        return categories

    def record_response(
        self, client_name: str, question_id: str, response: Any
    ) -> bool:
        """Record a response to a question."""
        if client_name not in self.intakes:
            return False

        intake = self.intakes[client_name]
        intake.responses[question_id] = IntakeResponse(
            question_id=question_id,
            response=response,
        )
        return True

    def get_intake(self, client_name: str) -> Optional[IntakeData]:
        """Get intake data for a client."""
        return self.intakes.get(client_name)

    def validate_intake(self, client_name: str) -> Dict[str, Any]:
        """Validate that all required questions have been answered."""
        intake = self.intakes.get(client_name)
        if not intake:
            return {"valid": False, "error": "Intake not found"}

        required_ids = [q.id for q in self.questions if q.required]
        missing = [qid for qid in required_ids if qid not in intake.responses]

        return {
            "valid": len(missing) == 0,
            "missing_questions": missing,
            "total_questions": len(self.questions),
            "answered": len(intake.responses),
            "completion_percentage": len(intake.responses) / len(self.questions) * 100,
        }

    def complete_intake(self, client_name: str) -> bool:
        """Mark an intake as complete."""
        intake = self.intakes.get(client_name)
        if not intake:
            return False

        validation = self.validate_intake(client_name)
        if not validation["valid"]:
            return False

        intake.completed_at = datetime.now()
        return True

    def extract_icp_data(self, client_name: str) -> Dict[str, Any]:
        """Extract ICP data from completed intake."""
        intake = self.intakes.get(client_name)
        if not intake:
            return {}

        return {
            "ideal_customer": intake.get_response("ideal_customer"),
            "target_industries": intake.get_response("target_industries"),
            "company_size": intake.get_response("company_size_sweet_spot"),
            "primary_buyer": intake.get_response("primary_buyer"),
            "buying_committee": intake.get_response("buying_committee"),
            "buying_triggers": intake.get_response("buying_triggers"),
            "pain_points": {
                "problem_solved": intake.get_response("problem_solved"),
                "alternatives_tried": intake.get_response("alternatives_tried"),
                "deal_stall_reasons": intake.get_response("deal_stall_reasons"),
            },
        }

    def extract_data_source_hints(self, client_name: str) -> Dict[str, Any]:
        """Extract hints for data source identification."""
        intake = self.intakes.get(client_name)
        if not intake:
            return {}

        return {
            "public_sources": intake.get_response("public_data_sources"),
            "industry_databases": intake.get_response("industry_databases"),
            "signal_job_titles": intake.get_response("signal_job_titles"),
            "good_tech_indicators": intake.get_response("good_fit_tech"),
            "bad_tech_indicators": intake.get_response("bad_fit_tech"),
            "external_events": intake.get_response("external_events"),
        }

    def generate_intake_summary(self, client_name: str) -> str:
        """Generate a text summary of the intake."""
        intake = self.intakes.get(client_name)
        if not intake:
            return "Intake not found."

        lines = [
            f"# Client Intake Summary: {client_name}",
            f"Started: {intake.started_at.strftime('%Y-%m-%d')}",
            f"Status: {'Complete' if intake.completed_at else 'In Progress'}",
            "",
        ]

        for category, questions in self.get_questions_by_category().items():
            lines.append(f"## {category}")
            for q in questions:
                response = intake.get_response(q.id)
                response_text = str(response) if response else "[Not answered]"
                lines.append(f"**{q.question}**")
                lines.append(response_text)
                lines.append("")

        return "\n".join(lines)
