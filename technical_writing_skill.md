# Technical Writing & GTM Communication Skill

## Overview
This skill guides Claude in creating clear, concise technical documentation, client-facing materials, and professional correspondence for GTM engineering contexts.

## Core Principles

### Writing Philosophy
- **Clarity over cleverness**: Say exactly what you mean
- **Brevity without sacrificing precision**: Every word should earn its place
- **Action-oriented**: Tell the reader what to do, not just what to know
- **Audience-aware**: Write for the reader's context and expertise level

### Voice and Tone
- **Professional but not stuffy**: Conversational without being casual
- **Confident but not arrogant**: Assert expertise without condescension
- **Direct but not blunt**: Get to the point while remaining respectful
- **Technical but accessible**: Explain complexity without oversimplifying

### Forbidden Patterns
Never use these:
- "I hope this message finds you well"
- "Just following up"
- "Circling back"
- "As per my last email"
- Em dashes (—)
- Excessive exclamation points
- Corporate jargon ("synergy," "circle back," "move the needle" unless being ironic)

## Technical Documentation

### Structure for System Documentation
```
# [System Name]

## Purpose
What this system does and why it exists (2-3 sentences)

## Architecture
High-level diagram or description of components

## Data Flow
Step-by-step: what happens when the system runs

## Configuration
Required settings, API keys, environment variables

## Maintenance
How often to review, what to monitor, when to update

## Troubleshooting
Common issues and solutions

## Owner
Who maintains this (name, email, Slack handle)
```

### Code Comments Best Practices
```javascript
// Good: Explains WHY, not WHAT
// Using composite score to prioritize leads with both good fit and recent intent
const leadScore = (firmographicScore * 0.6) + (behavioralScore * 0.4);

// Bad: States the obvious
// Calculate lead score by multiplying firmographic score by 0.6 and behavioral score by 0.4
const leadScore = (firmographicScore * 0.6) + (behavioralScore * 0.4);

// Good: Documents non-obvious business logic
// 24-hour threshold based on SLA with sales team
if (hoursSinceCreation > 24) {
  sendEscalationAlert();
}

// Bad: Redundant with code
// If hours since creation is greater than 24
if (hoursSinceCreation > 24) {
  sendEscalationAlert();
}
```

### API Documentation Template
```
## [Endpoint Name]

**Method**: POST  
**Endpoint**: `/api/v1/leads/enrich`  
**Authentication**: Bearer token in Authorization header

**Purpose**: Enriches lead records with company and contact data

**Request Body**:
```json
{
  "email": "john@example.com",
  "company_domain": "example.com",
  "enrich_company": true,
  "enrich_contact": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "contact": { ... },
    "company": { ... }
  },
  "credits_used": 2
}
```

**Error Responses**:
- `400`: Invalid email format
- `401`: Invalid or expired API key
- `429`: Rate limit exceeded
- `500`: Server error

**Example**:
```bash
curl -X POST https://api.example.com/v1/leads/enrich \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```
```

### Process Documentation Template
```
# [Process Name]

## When to Use This
Triggering conditions or scenarios

## Prerequisites
What needs to be in place before starting

## Step-by-Step Instructions
1. [First action]
   - Expected result: [what should happen]
   - If it fails: [what to do]

2. [Second action]
   - Expected result: [what should happen]
   - If it fails: [what to do]

## Validation
How to confirm it worked correctly

## Rollback Procedure
What to do if something goes wrong

## Frequency
How often this process runs (daily, weekly, monthly, ad-hoc)
```

## Client-Facing Materials

### Proposal Structure
```
# [Project Name] - Proposal

## Executive Summary
The problem, proposed solution, and expected outcome (3-4 sentences)

## Current State
What the client is dealing with now (pain points, inefficiencies)

## Proposed Solution
What you'll build/implement (high-level, non-technical)

## Deliverables
Specific outputs the client will receive:
- [Deliverable 1]: Description
- [Deliverable 2]: Description
- [Deliverable 3]: Description

## Timeline
Phase 1 (Weeks 1-2): [Activities]
Phase 2 (Weeks 3-4): [Activities]
Phase 3 (Weeks 5-6): [Activities]

## Investment
[Total project cost]
- Breakdown if relevant (discovery, implementation, ongoing)

## Success Metrics
How we'll measure if this worked:
- [Metric 1]: Current state → Target state
- [Metric 2]: Current state → Target state

## Next Steps
What happens if client wants to proceed
```

### Case Study Template
```
# [Client Name]: [Result-Focused Headline]

## The Challenge
[What problem were they facing? Be specific about impact.]

## The Solution
[What did you build/implement? Focus on approach, not technical details.]

## The Results
- [Quantified outcome 1]
- [Quantified outcome 2]
- [Quantified outcome 3]

## Client Quote
"[Testimonial highlighting the value delivered]"
- [Name, Title, Company]

## Technical Approach (Optional)
[For technical audiences, what technologies/methodologies you used]
```

### Project Update Template
```
Subject: [Project Name] - [Status] Update

[Client Name],

Here's where we are on [project name]:

**Completed This Week:**
- [Accomplishment 1]
- [Accomplishment 2]

**In Progress:**
- [Task 1] - On track for [date]
- [Task 2] - Waiting on [dependency]

**Coming Next:**
- [Next milestone] - Target: [date]

**Blockers:**
[If none: "None at this time."]
[If any: Specific blocker and what you need from client]

**Questions for You:**
1. [Specific question requiring client input]
2. [Another question if needed]

Let me know if you need anything clarified.

[Your Name]
```

## Email Communication

### Cold Outreach Template (B2B)
```
Subject: [Specific Pain Point] at [Company Name]

[First Name],

I noticed [Company Name] recently [specific trigger: hired for a role, announced funding, launched product].

Most [industry/role] teams we work with run into [specific pain point] when [scaling/expanding/etc].

We built [solution description in one sentence] for companies like [similar company 1] and [similar company 2].

Would it make sense to show you how [specific outcome] in [timeframe]?

If not a fit, happy to point you toward alternatives.

[Your Name]
[Title]
[Calendar link]
```

### Follow-Up Email (After No Response)
```
Subject: Re: [Original Subject]

[First Name],

Following up on my note from [day of week].

If [original problem] isn't a priority right now, no worries.

But if it's on your radar for [quarter/year], happy to share how [similar company] tackled it.

Otherwise, I'll leave you to it.

[Your Name]
```

### Meeting Request Email
```
Subject: 20 minutes to discuss [specific topic]?

[First Name],

[Context: how you know them or why you're reaching out]

I wanted to run something by you: [specific question or topic].

Would you have 20 minutes this week or next?

[Calendar link] or let me know what works better.

Thanks,
[Your Name]
```

### Post-Meeting Follow-Up
```
Subject: Summary - [Meeting Topic]

[First Name],

Thanks for the time today. Here's what we covered:

**What I Heard:**
- [Pain point 1]
- [Pain point 2]
- [Goal or constraint]

**What I'm Thinking:**
[Your proposed approach in 2-3 sentences]

**Next Steps:**
- [Action item for you with deadline]
- [Action item for them if applicable]
- [Follow-up meeting if scheduled]

Let me know if I missed anything.

[Your Name]
```

### Delivering Bad News
```
Subject: Update on [Project/Deliverable]

[First Name],

I need to flag something on [project name].

**What Happened:**
[Specific issue without sugarcoating]

**Impact:**
[How this affects timeline/budget/scope]

**What I'm Doing:**
[Your plan to address it]

**What I Need From You:**
[Specific ask if any, otherwise say "Nothing right now"]

I'll have an update for you by [specific time].

[Your Name]
```

## Internal Communication

### Slack Message Best Practices

**Good Slack Message**:
```
@john - Quick question on the Clay table for Accuris.

Should I enrich all 5,000 records or just the ones with lead_score > 60?

Running test batch now, but wanted to confirm before full run.
```

**Bad Slack Message**:
```
Hey! Hope you're having a great day! So I was thinking about the Clay thing and wasn't totally sure what to do, there's like a bunch of records and I don't know if we should do all of them or just some? Let me know when you get a chance! Thanks!! 😊
```

**Asking for Help**:
```
@channel - Running into an issue with the HubSpot API.

**What I'm trying to do:** Batch update 500 contacts
**What's happening:** Getting 429 rate limit errors after ~100 updates
**What I've tried:** Adding 100ms delay between requests, still hitting limit

Anyone dealt with this before?

[Code snippet or error message]
```

### Status Update Template (Internal)
```
**Project:** [Name]
**Status:** On Track / At Risk / Blocked

**This Week:**
- ✅ Completed: [Task 1]
- ✅ Completed: [Task 2]
- 🔄 In Progress: [Task 3]

**Next Week:**
- [Planned task 1]
- [Planned task 2]

**Blockers:**
[None or specific blocker with who can unblock it]
```

## Error Messages and User Feedback

### Writing Good Error Messages
```
// Bad: Cryptic and unhelpful
Error: ERR_INVALID_INPUT

// Good: Specific and actionable
Error: Email format is invalid. Please use format: name@domain.com

// Bad: Technical jargon
Error: NULL_POINTER_EXCEPTION in lead_scoring_module.js:42

// Good: User-friendly with action
Error: Unable to calculate lead score because company size is missing. 
Please add company size to continue.

// Bad: Vague
Error: Something went wrong

// Good: Specific with next steps
Error: Could not connect to HubSpot API. 
Check that your API key is valid in Settings > Integrations.
```

### User-Facing Notifications
```
// Success message
✅ Successfully enriched 247 contacts. View results in HubSpot.

// Warning message
⚠️ 15 contacts skipped due to invalid email format. Download error report.

// Progress update
⏳ Enriching contacts... 180/500 complete (estimated 2 minutes remaining)

// Action required
🔔 3 contacts need manual review. Click here to review now.
```

## Technical Presentations

### Slide Deck Structure
```
1. Title Slide
   - Project name
   - Date
   - Your name/role

2. Problem Statement
   - What's broken/inefficient today
   - Impact (quantified if possible)

3. Proposed Solution
   - High-level approach
   - Key components
   - Simple diagram

4. Technical Architecture (if audience is technical)
   - System diagram
   - Data flow
   - Integration points

5. Implementation Plan
   - Phases/milestones
   - Timeline
   - Dependencies

6. Expected Outcomes
   - Quantified benefits
   - Success metrics
   - Risks/mitigations

7. Next Steps
   - What needs to be decided
   - What happens next
   - Timeline for decision
```

### Demo Script Template
```
**Setup (30 seconds):**
"Today I'm showing you how [system] solves [problem]."

**Context (1 minute):**
"Right now, [current painful process]. This means [impact on team/business]."

**Demo (3-5 minutes):**
"Here's how it works with [system]:"

[Show, don't tell. Click through actual system.]

"Notice that [highlight key difference]. This is what changes [outcome]."

**Impact (1 minute):**
"Based on testing, this should [quantified outcome]."

**Questions (remainder of time):**
"What questions do you have?"
```

## Version Control and Change Logs

### Git Commit Message Format
```
[Type]: Brief description of change

- Specific change 1
- Specific change 2

Fixes: [Issue number if applicable]

Types:
- feat: New feature
- fix: Bug fix
- refactor: Code restructure without functional change
- docs: Documentation update
- chore: Maintenance task
```

**Examples**:
```
feat: Add lead scoring calculation

- Implement firmographic scoring (company size, industry)
- Implement behavioral scoring (website visits, content downloads)
- Add composite score calculation with 60/40 weighting

---

fix: Prevent duplicate contact creation in HubSpot

- Add email lookup before create operation
- Update existing record if found
- Log duplicate prevention in activity log

---

refactor: Simplify Clay table enrichment logic

- Consolidate three separate tables into single workflow
- Reduce total enrichment credits by 40%
- Improve execution time from 5min to 2min
```

### Change Log Template
```
# [System Name] Change Log

## [Version] - [Date]

### Added
- [New feature or capability]

### Changed
- [Modified behavior or configuration]

### Fixed
- [Bug fix or issue resolution]

### Removed
- [Deprecated feature or functionality]

---

## Example:

## v2.1.0 - 2024-01-15

### Added
- Lead scoring now includes intent signal weighting
- Slack notifications for high-value lead assignments

### Changed
- Updated territory routing to check rep capacity before assignment
- Enrichment runs now batched to reduce API calls by 30%

### Fixed
- Resolved issue causing duplicate HubSpot contacts
- Fixed date formatting in enrichment timestamp field

### Removed
- Deprecated legacy scoring algorithm (replaced with composite model)
```

## Documentation Maintenance

### When to Update Documentation
- **Immediately**: When process changes that affects daily operations
- **Weekly**: Status updates for active projects
- **Monthly**: Review and update troubleshooting guides
- **Quarterly**: Full audit of all documentation for accuracy

### Documentation Review Checklist
- [ ] Does this document still reflect current system behavior?
- [ ] Are all links and references still valid?
- [ ] Is the owner/maintainer information current?
- [ ] Are there new edge cases to document?
- [ ] Can a new team member follow these instructions successfully?
- [ ] Are screenshots/diagrams up to date?

## Style Guide Quick Reference

### Capitalization
- Product names: As branded (HubSpot, Clay, Make, not Hubspot, clay, make)
- Job titles: Title case in formal docs, lowercase in casual writing
- API endpoints: Lowercase with underscores (/api/v1/lead_enrichment)

### Numbers
- Spell out: one through nine
- Use numerals: 10 and above
- Exceptions: Always use numerals for percentages, measurements, scores

### Lists
- Use bullet points for unordered items
- Use numbered lists for sequential steps
- Keep list items parallel in structure

### Formatting
- Bold: UI elements, important warnings
- Italics: Emphasis (use sparingly)
- Code blocks: Code, API endpoints, terminal commands
- Links: Descriptive text, not "click here"

### Acronyms
- Spell out first use: Customer Relationship Management (CRM)
- Use acronym thereafter: CRM
- Exception: Industry-standard terms (API, URL, SQL)
