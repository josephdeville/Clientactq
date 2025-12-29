# Blueprint GTM Framework Template
## Reverse-Engineered for Any Client or Vertical

---

## SECTION 1: CORE PHILOSOPHY

### The Fundamental Principle
> "The message isn't the problem. The LIST is the message." - Jordan Crawford

**Translation:** Stop optimizing email copy. Start optimizing WHO you're targeting and WHAT you know about their specific situation.

### The Two Frameworks

**1. Pain-Qualified Segments (PQS)**
- Identify companies experiencing specific, verifiable pain points through public data signals
- Create messages that make prospects think: "How did they know we're dealing with exactly this?"
- The "Mirror Effect": Reflect their exact situation back to them with such accuracy they feel seen

**2. Permissionless Value Propositions (PVP)**
- Deliver immediate, actionable insights based on public data analysis
- Provide standalone value BEFORE any sales conversation
- Test: "Would they literally pay for this insight?"

---

## SECTION 2: THE PROBLEM STATEMENT TEMPLATE

### Current State Analysis (Use This Structure)

```
Most [industry] companies operate with a GTM playbook that hasn't changed since 2011:

1. Purchase lists from [ZoomInfo/Apollo] based on [generic firmographics]
2. Write persona-based templates with generic pain points
3. Add superficial personalization ({first_name}, {company}, {recent_news})
4. Automate at scale through [Outreach/SalesLoft]
5. Accept sub-0.5% response rates as "industry standard"

This fails because every competitor has the same data and uses identical tactics.
```

### The Relevance Gap Formula

```
When a prospect receives generic outreach, they face cognitive burden:
- "How does this apply to MY specific situation?"
- "Do they understand MY timeline?"
- "Do they understand MY resource constraints?"
- "Do they understand MY technology environment?"

Result: Delete. Not because they don't need help, but because sender 
hasn't demonstrated understanding of their SPECIFIC, CURRENT reality.
```

---

## SECTION 3: DATA SOURCE MAPPING TEMPLATE

### Three-Tier Data Architecture

**Tier 1: Foundational Records (High Reliability)**
```
Purpose: Establish baseline facts about the company
Sources to identify:
- Government registries (SAM.gov, state filings, regulatory databases)
- Industry-specific databases (your vertical's equivalent of FedRAMP Marketplace)
- Official certification/compliance registries
- Public financial filings (SEC, annual reports)

Questions to answer:
- What are they legally obligated to do?
- What certifications/licenses do they hold or need?
- What contracts/obligations are on record?
```

**Tier 2: Activity & Operations Signals**
```
Purpose: Identify current operational state and changes
Sources to identify:
- Job postings (LinkedIn Jobs, Indeed via Apify)
- Employee count changes (LinkedIn Company Pages)
- Technology stack (BuiltWith, Clearbit, Wappalyzer)
- Funding/M&A activity (Crunchbase, PitchBook)
- Leadership changes (LinkedIn, press releases)

Questions to answer:
- What are they actively hiring for? (reveals gaps/priorities)
- How is their team structured? (reveals capacity)
- What technology do they use? (reveals maturity/gaps)
- Recent funding? (reveals growth pressure/resources)
```

**Tier 3: Market Voice (Qualitative Signals)**
```
Purpose: Understand their pain points and frustrations
Sources to identify:
- G2/Capterra reviews (for their tools AND competitors)
- Industry forums/communities (Reddit, Slack groups, LinkedIn groups)
- Conference presentations/webinars
- Blog posts/podcasts from their leadership
- Support tickets (if accessible)

Questions to answer:
- What are they complaining about?
- What solutions have they tried and rejected?
- What language do they use to describe their problems?
```

### Data Source Identification Worksheet

```
For [CLIENT NAME] in [VERTICAL]:

FOUNDATIONAL RECORDS:
| Data Point Needed | Source | Access Method | Update Frequency |
|-------------------|--------|---------------|------------------|
| [e.g., Contract obligations] | [e.g., USAspending.gov] | [API/Manual] | [Daily/Weekly] |
| | | | |
| | | | |

ACTIVITY SIGNALS:
| Signal | Source | Trigger Criteria | Scoring Weight |
|--------|--------|------------------|----------------|
| [e.g., Compliance hiring] | [LinkedIn Jobs] | [ISSM, CISO posts] | [25 points] |
| | | | |
| | | | |

MARKET VOICE:
| Pain Point Category | Source | Search Terms |
|---------------------|--------|--------------|
| [e.g., Tool frustration] | [G2 Reviews] | [specific product names] |
| | | |
```

---

## SECTION 4: DATA RECIPE TEMPLATES

### What Is a Data Recipe?
A specific combination of data sources that identifies prospects at the exact moment they experience a verifiable pain point.

### Recipe Construction Formula

```
RECIPE NAME: [Descriptive name for internal use]

TARGET OUTCOME: [What situation are we identifying?]

DATA INGREDIENTS:
1. [Source 1] provides [data point] showing [signal]
2. [Source 2] provides [data point] showing [signal]  
3. [Source 3] provides [data point] showing [signal]

COMBINATION LOGIC:
IF [condition from source 1]
AND [condition from source 2]
AND [condition from source 3]
THEN [prospect matches this segment]

SCORING MODEL:
- [Signal 1]: [X] points (weight: [%])
- [Signal 2]: [X] points (weight: [%])
- [Signal 3]: [X] points (weight: [%])
- Threshold for outreach: [X] points minimum

VALIDATION METHOD:
Before messaging, manually verify:
- [ ] [Verification step 1]
- [ ] [Verification step 2]
```

### Example Recipe (Blank Template)

```
RECIPE NAME: [Deadline Collision / Growth Pressure / Tool Migration / etc.]

TARGET OUTCOME: Identify [persona] at [company type] who are experiencing 
[specific situation] within [timeframe]

DATA INGREDIENTS:
1. [Government/Industry Database] shows [obligation/requirement]
2. [Job Board] shows [hiring activity] within last [X] days
3. [Tech Stack Tool] shows [technology indicator]
4. [Company Data] shows [size/stage/funding indicator]

COMBINATION LOGIC:
Company has [obligation from source 1]
AND posted [role type] in last [X] days
AND has [technology gap/indicator]
AND is [size/stage criteria]

SCORING:
- Obligation urgency: 30 points
- Recent hiring signal: 25 points
- Technology gap: 25 points
- Company fit: 20 points
- TOTAL THRESHOLD: 70+ points

OUTPUT: Prospects scoring 70+ enter "[Segment Name]" sequence
```

---

## SECTION 5: MESSAGE FRAMEWORK TEMPLATES

### PQS Message Structure (Mirror-Insight-Ask)

```
SUBJECT: [3-5 words, reference specific data point or deadline]

[SENTENCE 1 - MIRROR]
State verifiable data point reflecting their specific situation.
Format: "Your [specific observable fact] suggests [logical inference]."

[SENTENCE 2-3 - INSIGHT/LEARNING]  
Share non-obvious pattern from peer companies.
Format: "Most [similar companies] in this position initially try [common approach], 
but those who [achieved outcome] found that [counterintuitive insight]."

[SENTENCE 4 - CURIOSITY ASK]
Low-friction question inviting dialogue.
Format: "Curious if you're seeing [specific challenge]?" or 
"Is [specific friction point] showing up for your team?"
```

### PQS Template (Fill-in-the-Blank)

```
Subject: [Their deadline/obligation/situation in 3-5 words]

Your [observable data point from Source 1] [combined with observable 
from Source 2] suggests you're [logical inference about their situation].

Most [peer companies in similar situation] initially try [common 
first approach]—but the ones who [achieved desired outcome] discovered 
that [specific tactic/approach] [quantified result]. They avoided 
[common costly mistake].

Curious if you're seeing [specific symptom of the problem]?
```

### PVP Message Structure (Data Hook-Value-Action)

```
SUBJECT: [Specific finding about THEIR business, 3-5 words]

[PARAGRAPH 1 - DATA HOOK]
Lead with specific, quantified finding about their situation.
Format: "Analysis of [their public data] shows [specific finding with numbers]—
including [named examples if possible]."

[PARAGRAPH 2 - DIRECT VALUE]
Explain why this matters NOW and what peer companies did.
Format: "With [deadline/pressure], you're [required/positioned] to 
[action needed]. [Peer companies] who [addressed this] [achieved result]."

[PARAGRAPH 3 - VALUE EXTENSION]
Offer more related value (not a meeting).
Format: "Want the [complete analysis/full breakdown/detailed assessment]?"
```

### PVP Template (Fill-in-the-Blank)

```
Subject: Your [specific business metric/risk/opportunity]

Analysis of your [public data source] shows [quantified finding]—
[specific examples: "including X, Y, and Z" or "specifically in areas A and B"].

With [external deadline/pressure/requirement], [consequence of inaction 
or opportunity cost]. [Peer companies] who [addressed this proactively] 
[achieved specific, quantified outcome] by [specific approach].

Want the [complete/detailed/full] [analysis type] for your [specific scope]?
```

---

## SECTION 6: IMPLEMENTATION ROADMAP TEMPLATE

### Phase 1: Discovery (Weeks 1-2)

```
OBJECTIVES:
- Map client's customer segments using ICP analysis
- Identify unique data sources for each segment
- Validate data accessibility
- Document existing customer patterns

DELIVERABLES:
□ ICP definition document with 2-3 primary segments
□ Data source matrix (Tier 1, 2, 3 for each segment)
□ Sample data pulls (25 records per segment)
□ Historical customer analysis (what patterns led to best customers?)

ACTIVITIES:
Week 1:
- [ ] Interview sales team: "Describe your last 5 best customers"
- [ ] Interview CS team: "Which customers have highest retention/expansion?"
- [ ] Pull list of closed-won deals from last 12 months
- [ ] Analyze common attributes of best customers

Week 2:
- [ ] Research public data sources for each segment
- [ ] Test API access and data quality
- [ ] Create data source documentation
- [ ] Identify gaps requiring paid tools
```

### Phase 2: Recipe Development (Weeks 3-4)

```
OBJECTIVES:
- Create initial PQS and PVP data recipes
- Manually execute recipes for test prospects
- Hand-craft messages and validate response rates
- Establish baseline metrics

DELIVERABLES:
□ 2-3 data recipes documented with full logic
□ 25 test prospects per recipe (manually researched)
□ Hand-crafted messages for each prospect
□ Response rate data (target: 15%+ validates concept)

ACTIVITIES:
Week 3:
- [ ] Build Recipe 1: [Primary pain point segment]
- [ ] Build Recipe 2: [Secondary pain point segment]
- [ ] Manual research: 25 prospects per recipe
- [ ] Draft messages using PQS/PVP templates

Week 4:
- [ ] Send test messages (personal email, not automation)
- [ ] Track opens, replies, meeting conversions
- [ ] Document message refinements based on responses
- [ ] Identify highest-performing recipe/message combinations
```

### Phase 3: Automation MVP (Weeks 5-6)

```
OBJECTIVES:
- Build automated workflows for validated recipes
- Create message templates with dynamic personalization
- Establish testing protocols
- Deploy to small test segments

DELIVERABLES:
□ Clay/n8n workflows for each validated recipe
□ Message templates with variable insertion points
□ A/B testing framework
□ Automated prospect scoring model

ACTIVITIES:
Week 5:
- [ ] Build Clay table with data source integrations
- [ ] Create scoring model (0-100 based on signals)
- [ ] Build message templates with merge fields
- [ ] Test workflow end-to-end with sample data

Week 6:
- [ ] Deploy to 25-50 prospects weekly
- [ ] Set up response tracking
- [ ] Create A/B test variants (subject lines, hooks, CTAs)
- [ ] Document workflow maintenance procedures
```

### Phase 4: Scale (Weeks 7-8)

```
OBJECTIVES:
- Expand to multi-channel outreach
- Build monitoring for trigger events
- Document processes for team adoption
- Prepare for ongoing operations

DELIVERABLES:
□ Multi-channel sequences (email + LinkedIn + ads)
□ Event monitoring dashboards
□ Team training documentation
□ Ongoing maintenance playbook

ACTIVITIES:
Week 7:
- [ ] Add LinkedIn outreach to sequences
- [ ] Set up trigger monitoring (new contracts, job posts, etc.)
- [ ] Create sales handoff process
- [ ] Document all workflows and recipes

Week 8:
- [ ] Train sales team on new process
- [ ] Establish weekly review cadence
- [ ] Create case study templates for wins
- [ ] Plan quarterly expansion to new segments
```

---

## SECTION 7: METRIC TRACKING FRAMEWORK

### Response Rate Benchmarks

```
BASELINE (Traditional Outreach):
- Cold email response rate: 0.5-1%
- LinkedIn connection accept: 15-25%
- LinkedIn InMail response: 3-5%

TARGET (Blueprint Framework):
- PQS email response rate: 15-25%
- PVP email response rate: 20-30%
- LinkedIn with PQS/PVP messaging: 25-40%
```

### Tracking Dashboard Template

```
WEEKLY METRICS:
| Metric | This Week | Last Week | Target | Trend |
|--------|-----------|-----------|--------|-------|
| Prospects researched | | | 50 | |
| Messages sent | | | 50 | |
| Opens | | | 60% | |
| Replies (any) | | | 15% | |
| Positive replies | | | 10% | |
| Meetings booked | | | 5% | |
| Pipeline created | | | $XXK | |

BY RECIPE:
| Recipe Name | Sent | Reply Rate | Meeting Rate | Notes |
|-------------|------|------------|--------------|-------|
| [Recipe 1] | | | | |
| [Recipe 2] | | | | |

BY MESSAGE VARIANT:
| Variant | Sent | Reply Rate | Winner? |
|---------|------|------------|---------|
| Subject A | | | |
| Subject B | | | |
```

---

## SECTION 8: PROPOSAL DOCUMENT TEMPLATE

### Document Structure

```
1. EXECUTIVE SUMMARY (1 page)
   - Core principle quote
   - Market context (why now?)
   - Unique positioning opportunity
   - Expected outcomes

2. CURRENT STATE ANALYSIS (1 page)
   - The "2011 playbook problem"
   - Why traditional approach fails
   - The relevance gap

3. FRAMEWORK OVERVIEW (1-2 pages)
   - PQS explanation with client-specific example
   - PVP explanation with client-specific example
   - "Mirror Effect" and "Value-First" principles

4. CLIENT-SPECIFIC EXAMPLES (2-3 pages)
   - 3-5 concrete PQS/PVP message examples
   - Data recipes for each
   - Why each works (breakdown)

5. IMPLEMENTATION COMPONENTS (2 pages)
   - Data source identification (Tier 1, 2, 3)
   - Data synthesis engine (workflow description)
   - Message development process

6. STRATEGIC ADVANTAGES (1 page)
   - Data moat concept
   - Execution barrier
   - Compound learning
   - Response rate dominance
   - Sales cycle compression

7. IMPLEMENTATION TIMELINE (1-2 pages)
   - 8-week phased approach
   - Weekly deliverables
   - Milestones and checkpoints

8. INVESTMENT & ROI (1 page)
   - Technology stack costs
   - Team development needs
   - Expected ROI by phase

9. NEXT STEPS (0.5 page)
   - Concrete action items
   - Decision points
   - Timeline to kickoff

10. CONCLUSION
    - Restate transformation (generic → precision)
    - "The List Is The Message"
```

---

## SECTION 9: CLIENT INTAKE QUESTIONNAIRE

Use this to gather information before building a proposal:

```
COMPANY BASICS:
1. Company name and website:
2. What do you sell? (1-2 sentences):
3. Average deal size:
4. Sales cycle length:
5. Current team size (sales, marketing, ops):

ICP DEFINITION:
6. Describe your ideal customer in detail:
7. What industries/verticals do you serve?
8. Company size sweet spot (employees, revenue):
9. Who is your primary buyer (title, role)?
10. Who else is involved in buying decisions?

CURRENT GTM:
11. How do you currently generate leads?
12. What tools do you use? (CRM, outreach, data):
13. Current response rates on outbound:
14. What's working well today?
15. What's not working?

PAIN POINTS & TRIGGERS:
16. What specific problem do you solve?
17. What triggers a company to need your solution?
18. What external events/deadlines affect your buyers?
19. What do prospects typically try before buying from you?
20. Why do deals stall or get lost?

DATA & SIGNALS:
21. What public data exists about your target companies?
22. Are there industry databases or registries relevant to your buyers?
23. What job titles indicate a company needs your solution?
24. What technology stack signals a good fit?
25. What technology stack signals a bad fit?

COMPETITIVE LANDSCAPE:
26. Who are your main competitors?
27. How do prospects typically find alternatives?
28. What do you do better than competitors?
29. What do competitors say about themselves?

SUCCESS PATTERNS:
30. Describe your last 3 best customers—how did they find you?
31. What did those customers have in common?
32. What was the "aha moment" that made them buy?
```

---

## SECTION 10: QUICK-START CHECKLIST

For any new client engagement:

```
□ Complete client intake questionnaire
□ Research 3-5 relevant public data sources
□ Pull sample data (25 records) manually
□ Identify 2-3 potential data recipes
□ Draft 1 PQS message example
□ Draft 1 PVP message example
□ Validate with client that examples resonate
□ Build proposal using document template
□ Present and gather feedback
□ Refine based on client input
□ Begin Phase 1 implementation
```

---

## ATTRIBUTION

This framework is based on Jordan Crawford's Blueprint GTM methodology.
Learn more at: https://course.blueprintgtm.com

All strategic concepts, including Pain-Qualified Segments (PQS), 
Permissionless Value Propositions (PVP), and "The List Is The Message" 
principle are credited to Jordan Crawford and Blueprint GTM.
