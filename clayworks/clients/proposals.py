"""
ClayWorks Proposal Generator Module
===================================

Generate client proposals based on the Blueprint GTM methodology.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime

from .intake import ClientIntake, IntakeData


@dataclass
class ProposalSection:
    """A section of a proposal."""
    title: str
    content: str
    page_count: float = 1.0


@dataclass
class Proposal:
    """A generated proposal."""
    client_name: str
    title: str
    sections: List[ProposalSection]
    generated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0"

    def to_markdown(self) -> str:
        """Export proposal as Markdown."""
        lines = [
            f"# {self.title}",
            f"*Prepared for: {self.client_name}*",
            f"*Date: {self.generated_at.strftime('%B %d, %Y')}*",
            "",
            "---",
            "",
        ]

        for section in self.sections:
            lines.append(f"## {section.title}")
            lines.append("")
            lines.append(section.content)
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    @property
    def total_pages(self) -> float:
        """Estimate total page count."""
        return sum(s.page_count for s in self.sections)


class ProposalGenerator:
    """
    Proposal Generator based on Blueprint GTM methodology.

    Document Structure:
    1. EXECUTIVE SUMMARY (1 page)
    2. CURRENT STATE ANALYSIS (1 page)
    3. FRAMEWORK OVERVIEW (1-2 pages)
    4. CLIENT-SPECIFIC EXAMPLES (2-3 pages)
    5. IMPLEMENTATION COMPONENTS (2 pages)
    6. STRATEGIC ADVANTAGES (1 page)
    7. IMPLEMENTATION TIMELINE (1-2 pages)
    8. INVESTMENT & ROI (1 page)
    9. NEXT STEPS (0.5 page)
    10. CONCLUSION
    """

    def __init__(self, intake: Optional[ClientIntake] = None):
        self.intake = intake

    def generate(
        self,
        client_name: str,
        intake_data: Optional[IntakeData] = None,
        custom_examples: Optional[List[Dict[str, str]]] = None,
    ) -> Proposal:
        """Generate a complete proposal."""
        sections = [
            self._generate_executive_summary(client_name, intake_data),
            self._generate_current_state(intake_data),
            self._generate_framework_overview(),
            self._generate_client_examples(client_name, intake_data, custom_examples),
            self._generate_implementation_components(),
            self._generate_strategic_advantages(),
            self._generate_timeline(),
            self._generate_investment_roi(intake_data),
            self._generate_next_steps(client_name),
            self._generate_conclusion(),
        ]

        return Proposal(
            client_name=client_name,
            title=f"Blueprint GTM Framework Proposal for {client_name}",
            sections=sections,
        )

    def _generate_executive_summary(
        self, client_name: str, intake: Optional[IntakeData]
    ) -> ProposalSection:
        """Generate executive summary section."""
        content = f"""
> "The message isn't the problem. The LIST is the message." - Jordan Crawford

### Market Context

{client_name} operates in a market where every competitor has access to the same data sources (ZoomInfo, Apollo, LinkedIn) and uses identical outreach tactics. This creates a race to the bottom where:

- Response rates decline as prospects become numb to generic outreach
- Sales cycles lengthen as trust becomes harder to establish
- Customer acquisition costs rise without corresponding value

### The Opportunity

By implementing the Blueprint GTM Framework, {client_name} can transform outreach from "spray and pray" to precision targeting. This means:

- **Targeting prospects at their moment of need** based on verifiable data signals
- **Delivering value before the first conversation** through actionable insights
- **Achieving 15-25% response rates** vs. industry standard 0.5-1%

### Expected Outcomes

- 30-50x improvement in email response rates
- 50% reduction in sales cycle length for qualified opportunities
- Sustainable competitive advantage through proprietary data approaches
"""
        return ProposalSection(
            title="1. Executive Summary",
            content=content.strip(),
            page_count=1.0,
        )

    def _generate_current_state(
        self, intake: Optional[IntakeData]
    ) -> ProposalSection:
        """Generate current state analysis section."""
        current_issues = ""
        if intake:
            not_working = intake.get_response("whats_not_working")
            if not_working:
                current_issues = f"\n\n### Current Challenges\n\n{not_working}"

        content = f"""
### The "2011 Playbook Problem"

Most companies operate with a GTM playbook that hasn't evolved:

1. **Purchase lists** from ZoomInfo/Apollo based on generic firmographics
2. **Write persona-based templates** with generic pain points
3. **Add superficial personalization** ({{first_name}}, {{company}}, {{recent_news}})
4. **Automate at scale** through Outreach/SalesLoft
5. **Accept sub-0.5% response rates** as "industry standard"

**This fails because every competitor has the same data and uses identical tactics.**

### The Relevance Gap

When a prospect receives generic outreach, they face cognitive burden:

- "How does this apply to MY specific situation?"
- "Do they understand MY timeline?"
- "Do they understand MY resource constraints?"
- "Do they understand MY technology environment?"

**Result:** Delete. Not because they don't need help, but because the sender hasn't demonstrated understanding of their SPECIFIC, CURRENT reality.{current_issues}
"""
        return ProposalSection(
            title="2. Current State Analysis",
            content=content.strip(),
            page_count=1.0,
        )

    def _generate_framework_overview(self) -> ProposalSection:
        """Generate framework overview section."""
        content = """
### The Two Frameworks

**1. Pain-Qualified Segments (PQS)**

PQS identifies companies experiencing specific, verifiable pain points through public data signals. Instead of targeting by firmographics, we target by situation.

**The "Mirror Effect":** Create messages that make prospects think: *"How did they know we're dealing with exactly this?"*

Structure (Mirror-Insight-Ask):
- **Mirror:** State verifiable data point reflecting their specific situation
- **Insight:** Share non-obvious pattern from peer companies
- **Ask:** Low-friction question inviting dialogue

**2. Permissionless Value Propositions (PVP)**

PVP delivers immediate, actionable insights based on public data analysis—before any sales conversation.

**The Test:** "Would they literally pay for this insight?"

Structure (Data Hook-Value-Action):
- **Data Hook:** Lead with specific, quantified finding about their situation
- **Value:** Explain why this matters NOW and what peer companies did
- **Action:** Offer more value (not a meeting)

### Why This Works

When you lead with verified knowledge of their situation, you bypass the relevance gap entirely. They don't have to wonder if you understand their challenges—you've already proven it.
"""
        return ProposalSection(
            title="3. Framework Overview",
            content=content.strip(),
            page_count=1.5,
        )

    def _generate_client_examples(
        self,
        client_name: str,
        intake: Optional[IntakeData],
        custom_examples: Optional[List[Dict[str, str]]],
    ) -> ProposalSection:
        """Generate client-specific examples section."""
        examples = custom_examples or []

        if intake:
            # Generate examples based on intake data
            triggers = intake.get_response("buying_triggers") or []
            problem = intake.get_response("problem_solved") or "your solution"

            if triggers:
                examples.append({
                    "name": "Trigger-Based PQS Example",
                    "description": f"Targeting companies showing: {triggers[0] if triggers else 'buying signals'}",
                    "subject": f"Re: {triggers[0] if triggers else 'your situation'}",
                    "body": f"""Your [observable signal] combined with [second signal] suggests you're evaluating solutions for {problem}.

Most companies in this position initially try [common approach]—but the ones who succeeded discovered that [better approach] led to [quantified result].

Curious if [specific challenge] is on your radar?""",
                })

        if not examples:
            # Default examples
            examples = [
                {
                    "name": "PQS Example: Compliance Deadline",
                    "subject": "FedRAMP deadline by Q4",
                    "body": """Your FedRAMP listing combined with your recent ISSM job posting suggests you're building compliance capability under deadline pressure.

Most GovCon companies in this position initially try hiring an internal team—but the ones who achieved ATO on schedule discovered that [specific approach] reduced their timeline by 40%. They avoided the common mistake of [mistake].

Curious if documentation gaps are showing up for your team?""",
                },
                {
                    "name": "PVP Example: Tech Stack Audit",
                    "subject": "Your authentication infrastructure gaps",
                    "body": """Analysis of your public tech stack shows 3 potential security gaps—including legacy auth methods on your customer portal and missing MFA on your admin systems.

With SOC 2 requirements tightening, these gaps could delay your next audit. Companies who addressed these proactively reduced remediation costs by 60%.

Want the complete security assessment for your infrastructure?""",
                },
            ]

        example_content = ""
        for ex in examples:
            example_content += f"""
### {ex.get('name', 'Example')}

**Subject:** {ex.get('subject', '')}

{ex.get('body', '')}

---
"""

        content = f"""
The following examples are customized for {client_name}'s target market:

{example_content}

### Why These Work

Each example follows the framework principles:
- **Verifiable data points** that can be confirmed through public sources
- **Specific situation** rather than generic pain points
- **Peer insights** that provide non-obvious value
- **Low-friction ask** that invites dialogue without pressure
"""
        return ProposalSection(
            title="4. Client-Specific Examples",
            content=content.strip(),
            page_count=2.5,
        )

    def _generate_implementation_components(self) -> ProposalSection:
        """Generate implementation components section."""
        content = """
### Data Source Architecture

**Tier 1: Foundational Records (High Reliability)**
- Government registries and contract databases
- Industry-specific databases and certifications
- Public financial filings and disclosures

**Tier 2: Activity & Operations Signals**
- Job postings (LinkedIn, Indeed)
- Technology stack detection (BuiltWith, Wappalyzer)
- Funding and M&A activity (Crunchbase, PitchBook)
- Employee count changes

**Tier 3: Market Voice (Qualitative)**
- G2/Capterra reviews
- Industry forums and communities
- Conference presentations and webinars

### Data Synthesis Engine

We build automated workflows that:
1. **Aggregate** data from multiple sources for each prospect
2. **Score** prospects based on signal strength (0-100)
3. **Generate** personalized messaging using templates
4. **Validate** data accuracy before outreach

### Message Development Process

1. Identify 2-3 primary PQS/PVP approaches
2. Create templates with dynamic personalization fields
3. A/B test subject lines, hooks, and CTAs
4. Continuously refine based on response data
"""
        return ProposalSection(
            title="5. Implementation Components",
            content=content.strip(),
            page_count=2.0,
        )

    def _generate_strategic_advantages(self) -> ProposalSection:
        """Generate strategic advantages section."""
        content = """
### Sustainable Competitive Advantages

**1. Data Moat**
Custom data combinations create insights competitors can't replicate. While others use the same ZoomInfo/Apollo data, your approach synthesizes unique signals.

**2. Execution Barrier**
The operational excellence required to execute this framework—data pipelines, message templates, A/B testing—creates a moat that takes months to build.

**3. Compound Learning**
Every outreach generates data that improves the next iteration. Response patterns, winning subject lines, and effective hooks become proprietary IP.

**4. Response Rate Dominance**
15-25% response rates vs. 0.5% industry standard means:
- 30-50x more conversations from same volume
- Higher quality conversations (they already know you understand them)
- Faster deal velocity

**5. Sales Cycle Compression**
When prospects feel understood from first touch:
- Trust is established earlier
- Discovery calls are more productive
- Objection handling is reduced
- Time-to-close decreases significantly
"""
        return ProposalSection(
            title="6. Strategic Advantages",
            content=content.strip(),
            page_count=1.0,
        )

    def _generate_timeline(self) -> ProposalSection:
        """Generate implementation timeline section."""
        content = """
### 8-Week Implementation Roadmap

**Phase 1: Discovery (Weeks 1-2)**
- Map customer segments using ICP analysis
- Identify unique data sources for each segment
- Validate data accessibility and quality
- Document existing customer success patterns

*Deliverables: ICP document, Data source matrix, Sample data pulls*

**Phase 2: Recipe Development (Weeks 3-4)**
- Create initial PQS and PVP data recipes
- Manually research 25 test prospects per recipe
- Hand-craft messages and send via personal email
- Validate response rates (target: 15%+)

*Deliverables: 2-3 validated recipes, Response rate baseline*

**Phase 3: Automation MVP (Weeks 5-6)**
- Build automated workflows for validated recipes
- Create message templates with dynamic personalization
- Deploy to 25-50 prospects weekly
- Establish A/B testing framework

*Deliverables: Automated workflows, Scoring model, Message templates*

**Phase 4: Scale (Weeks 7-8)**
- Expand to multi-channel (email + LinkedIn)
- Set up trigger monitoring for real-time signals
- Document processes for team adoption
- Train sales team on new approach

*Deliverables: Multi-channel sequences, Event monitors, Training materials*
"""
        return ProposalSection(
            title="7. Implementation Timeline",
            content=content.strip(),
            page_count=1.5,
        )

    def _generate_investment_roi(
        self, intake: Optional[IntakeData]
    ) -> ProposalSection:
        """Generate investment and ROI section."""
        avg_deal = 50000
        if intake:
            deal_size = intake.get_response("avg_deal_size")
            if deal_size:
                try:
                    avg_deal = int(deal_size)
                except (ValueError, TypeError):
                    pass

        content = f"""
### Technology Stack Investment

| Component | Purpose | Estimated Cost |
|-----------|---------|----------------|
| Clay | Data enrichment and workflows | $500-2000/mo |
| Data APIs | BuiltWith, Crunchbase, etc. | $500-1500/mo |
| Email infrastructure | Deliverability | $100-300/mo |
| CRM integration | Data sync | Existing |

### Expected ROI

**Assumptions:**
- Current response rate: 0.5%
- Target response rate: 15% (30x improvement)
- Average deal size: ${avg_deal:,}
- Monthly outreach volume: 500 messages

**Monthly Impact:**
- Current pipeline generation: 2.5 opportunities
- Projected pipeline generation: 75 opportunities
- Additional pipeline value: ${(75 - 2.5) * avg_deal * 0.2:,.0f}/month

### Payback Period

With typical technology investment of $1,500/month and additional pipeline value significantly exceeding this, ROI is typically achieved within the first month of scaled operation.
"""
        return ProposalSection(
            title="8. Investment & ROI",
            content=content.strip(),
            page_count=1.0,
        )

    def _generate_next_steps(self, client_name: str) -> ProposalSection:
        """Generate next steps section."""
        content = f"""
### Immediate Actions

1. **Schedule Discovery Call** - Deep dive on ICP and existing customer patterns
2. **Data Source Audit** - Identify available data for target segments
3. **Pilot Scope Definition** - Select initial segment for testing
4. **Kickoff Planning** - Align on timeline and resources

### Decision Points

- Which segment to prioritize for initial testing?
- What internal resources will support the initiative?
- What are the success metrics for the pilot?
- Timeline for full rollout after successful pilot?

### Contact

Ready to transform {client_name}'s outbound approach? Let's schedule a discovery call to map your customer segments and identify the highest-impact opportunities.
"""
        return ProposalSection(
            title="9. Next Steps",
            content=content.strip(),
            page_count=0.5,
        )

    def _generate_conclusion(self) -> ProposalSection:
        """Generate conclusion section."""
        content = """
### The Transformation

The Blueprint GTM Framework transforms your outreach from generic spray-and-pray to precision engagement. Instead of hoping prospects self-identify relevance, you demonstrate understanding of their specific situation from the first touch.

> "The message isn't the problem. The LIST is the message."

When you target the right companies at the right moment with verified knowledge of their situation, response rates follow naturally. This isn't about clever copywriting—it's about fundamental alignment between your outreach and your prospect's reality.

---

### Attribution

This framework is based on Jordan Crawford's Blueprint GTM methodology.
Learn more at: https://course.blueprintgtm.com

All strategic concepts, including Pain-Qualified Segments (PQS), Permissionless Value Propositions (PVP), and "The List Is The Message" principle are credited to Jordan Crawford and Blueprint GTM.
"""
        return ProposalSection(
            title="10. Conclusion",
            content=content.strip(),
            page_count=0.5,
        )
