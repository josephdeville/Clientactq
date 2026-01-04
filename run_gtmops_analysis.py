#!/usr/bin/env python3
"""
ClayWorks GTM:Ops Analysis Runner
=================================

Processes the GTM:Ops CSV through the ClayWorks framework to:
1. Score prospects based on hiring signals
2. Generate PQS/PVP messages for top prospects
3. Output analysis and recommendations
"""

import csv
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Any, Optional


@dataclass
class Prospect:
    """A prospect from the GTM:Ops data."""
    company_name: str
    job_title: str
    location: str
    domain: str
    job_url: str
    posted_on: str
    company_linkedin: str
    boss_name: str
    boss_title: str
    boss_linkedin: str
    boss_email: str

    @property
    def days_since_posted(self) -> int:
        """Calculate days since job was posted."""
        try:
            posted_date = datetime.fromisoformat(self.posted_on.replace('Z', '+00:00'))
            return (datetime.now(posted_date.tzinfo) - posted_date).days
        except:
            return 0

    @property
    def is_senior_role(self) -> bool:
        """Check if this is a senior/leadership role."""
        senior_keywords = ['director', 'head', 'vp', 'vice president', 'senior manager', 'lead', 'principal']
        return any(kw in self.job_title.lower() for kw in senior_keywords)

    @property
    def is_revenue_ops(self) -> bool:
        """Check if this is a RevOps role."""
        revops_keywords = ['revenue operations', 'revops', 'revenue ops', 'gtm operations', 'gtm ops']
        return any(kw in self.job_title.lower() for kw in revops_keywords)

    @property
    def is_sales_ops(self) -> bool:
        """Check if this is a Sales Ops role."""
        return 'sales operations' in self.job_title.lower() or 'sales ops' in self.job_title.lower()

    @property
    def is_marketing_ops(self) -> bool:
        """Check if this is a Marketing Ops role."""
        return 'marketing operations' in self.job_title.lower() or 'marketing ops' in self.job_title.lower()


class GTMOpsScorer:
    """Scorer for GTM:Ops prospects based on Blueprint methodology."""

    def __init__(self, threshold: int = 70):
        self.threshold = threshold

    def score(self, prospect: Prospect) -> Dict[str, Any]:
        """Score a prospect based on multiple signals."""
        scores = {}
        total = 0

        # Recency of posting (max 25 points)
        days = prospect.days_since_posted
        if days <= 3:
            scores['recency'] = 25
        elif days <= 7:
            scores['recency'] = 20
        elif days <= 14:
            scores['recency'] = 15
        elif days <= 30:
            scores['recency'] = 10
        else:
            scores['recency'] = 5
        total += scores['recency']

        # Role seniority (max 25 points)
        if prospect.is_senior_role:
            scores['seniority'] = 25
        else:
            scores['seniority'] = 10
        total += scores['seniority']

        # Role type relevance (max 25 points)
        if prospect.is_revenue_ops:
            scores['role_type'] = 25
        elif prospect.is_sales_ops:
            scores['role_type'] = 20
        elif prospect.is_marketing_ops:
            scores['role_type'] = 15
        else:
            scores['role_type'] = 10
        total += scores['role_type']

        # Contact completeness (max 25 points)
        contact_score = 0
        if prospect.boss_name and prospect.boss_name.strip():
            contact_score += 8
        if prospect.boss_email and prospect.boss_email.strip():
            contact_score += 10
        if prospect.boss_linkedin and prospect.boss_linkedin.strip():
            contact_score += 7
        scores['contact_completeness'] = contact_score
        total += contact_score

        return {
            'total_score': total,
            'max_score': 100,
            'qualifies': total >= self.threshold,
            'breakdown': scores,
            'threshold': self.threshold,
        }


class PQSMessageGenerator:
    """Generate PQS (Pain-Qualified Segment) messages."""

    def generate(self, prospect: Prospect, score_data: Dict) -> Dict[str, str]:
        """Generate a PQS message for a prospect."""

        # Determine the pain point based on role
        if prospect.is_revenue_ops:
            pain_area = "revenue operations"
            common_approach = "hiring a generalist or promoting from within"
            better_approach = "bringing in specialized RevOps expertise that can hit the ground running"
            outcome = "reduced ramp time by 60% and achieved faster pipeline visibility"
            symptom = "data silos between sales, marketing, and CS"
        elif prospect.is_sales_ops:
            pain_area = "sales operations"
            common_approach = "having AEs manage their own pipeline hygiene"
            better_approach = "implementing automated data enrichment and scoring"
            outcome = "increased rep productivity by 40%"
            symptom = "manual CRM updates eating into selling time"
        else:
            pain_area = "marketing operations"
            common_approach = "bolting on more point solutions"
            better_approach = "consolidating their martech stack around a unified data layer"
            outcome = "improved campaign attribution accuracy by 3x"
            symptom = "attribution gaps across the funnel"

        # Build subject line
        role_short = prospect.job_title.split(',')[0].split('-')[0].strip()[:40]
        subject = f"Re: {role_short} role"

        # Build body using Mirror-Insight-Ask structure
        body = f"""Your open {prospect.job_title} posting combined with your team structure suggests you're building out {pain_area} capability.

Most companies in this position initially try {common_approach}—but the ones who scaled efficiently discovered that {better_approach} {outcome}.

Curious if you're seeing {symptom}?"""

        return {
            'subject': subject,
            'body': body,
            'type': 'PQS',
            'pain_area': pain_area,
        }


class PVPMessageGenerator:
    """Generate PVP (Permissionless Value Proposition) messages."""

    def generate(self, prospect: Prospect, score_data: Dict) -> Dict[str, str]:
        """Generate a PVP message for a prospect."""

        # Build subject
        subject = f"{prospect.company_name}'s GTM ops gap analysis"

        # Determine value proposition based on role
        if prospect.is_senior_role:
            finding = f"your {prospect.job_title} posting suggests you're building a strategic ops function"
            value = "Companies hiring senior ops roles who get the structure right from day one see 40% faster time-to-productivity"
            offer = "GTM ops org design framework"
        else:
            finding = f"your open {prospect.job_title} role indicates growing operational complexity"
            value = "Teams that implement proper ops tooling before hiring see 50% better new hire retention"
            offer = "ops tech stack audit template"

        body = f"""Analysis of {prospect.company_name}'s public hiring data shows {finding}.

{value}—specifically by aligning tooling, process, and headcount in the right sequence.

Want the {offer} we've used with similar companies?"""

        return {
            'subject': subject,
            'body': body,
            'type': 'PVP',
            'offer': offer,
        }


def load_csv(filepath: str) -> List[Prospect]:
    """Load prospects from CSV file."""
    prospects = []

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prospect = Prospect(
                company_name=row.get('Company Name', ''),
                job_title=row.get('Job Title', ''),
                location=row.get('Location', ''),
                domain=row.get('Company Domain', ''),
                job_url=row.get('Job LinkedIn URL', ''),
                posted_on=row.get('Posted On', ''),
                company_linkedin=row.get('Company LI Url', ''),
                boss_name=row.get('Boss_Name', ''),
                boss_title=row.get('Boss Title', ''),
                boss_linkedin=row.get('Boss_Linked In', ''),
                boss_email=row.get('New Column (2)', ''),
            )
            if prospect.company_name:  # Skip empty rows
                prospects.append(prospect)

    return prospects


def analyze_prospects(prospects: List[Prospect]) -> Dict[str, Any]:
    """Analyze the prospect list."""
    analysis = {
        'total': len(prospects),
        'by_role_type': {
            'revenue_ops': 0,
            'sales_ops': 0,
            'marketing_ops': 0,
            'other': 0,
        },
        'senior_roles': 0,
        'recent_postings': 0,  # Posted in last 7 days
        'with_email': 0,
    }

    for p in prospects:
        if p.is_revenue_ops:
            analysis['by_role_type']['revenue_ops'] += 1
        elif p.is_sales_ops:
            analysis['by_role_type']['sales_ops'] += 1
        elif p.is_marketing_ops:
            analysis['by_role_type']['marketing_ops'] += 1
        else:
            analysis['by_role_type']['other'] += 1

        if p.is_senior_role:
            analysis['senior_roles'] += 1

        if p.days_since_posted <= 7:
            analysis['recent_postings'] += 1

        if p.boss_email and '@' in p.boss_email:
            analysis['with_email'] += 1

    return analysis


def main():
    """Main analysis runner."""
    print("=" * 60)
    print("ClayWorks GTM:Ops Analysis")
    print("=" * 60)
    print()

    # Load data
    csv_path = "GTM:Ops .csv"
    print(f"Loading data from: {csv_path}")
    prospects = load_csv(csv_path)
    print(f"Loaded {len(prospects)} prospects")
    print()

    # Analyze dataset
    print("-" * 60)
    print("DATASET ANALYSIS")
    print("-" * 60)
    analysis = analyze_prospects(prospects)
    print(f"Total prospects: {analysis['total']}")
    print(f"Role breakdown:")
    print(f"  - Revenue Ops: {analysis['by_role_type']['revenue_ops']}")
    print(f"  - Sales Ops: {analysis['by_role_type']['sales_ops']}")
    print(f"  - Marketing Ops: {analysis['by_role_type']['marketing_ops']}")
    print(f"  - Other GTM: {analysis['by_role_type']['other']}")
    print(f"Senior/Leadership roles: {analysis['senior_roles']}")
    print(f"Posted in last 7 days: {analysis['recent_postings']}")
    print(f"With contact email: {analysis['with_email']}")
    print()

    # Score prospects
    print("-" * 60)
    print("SCORING PROSPECTS")
    print("-" * 60)
    scorer = GTMOpsScorer(threshold=70)
    scored = []

    for prospect in prospects:
        score_data = scorer.score(prospect)
        scored.append({
            'prospect': prospect,
            'score': score_data,
        })

    # Sort by score
    scored.sort(key=lambda x: x['score']['total_score'], reverse=True)

    qualified = [s for s in scored if s['score']['qualifies']]
    print(f"Qualified prospects (score >= 70): {len(qualified)}")
    print(f"Average score: {sum(s['score']['total_score'] for s in scored) / len(scored):.1f}")
    print()

    # Top 20 prospects
    print("-" * 60)
    print("TOP 20 PROSPECTS")
    print("-" * 60)
    for i, item in enumerate(scored[:20], 1):
        p = item['prospect']
        s = item['score']
        print(f"{i:2}. [{s['total_score']:3}] {p.company_name}")
        print(f"      Role: {p.job_title}")
        print(f"      Contact: {p.boss_name} ({p.boss_title})")
        print(f"      Email: {p.boss_email}")
        print()

    # Generate sample messages for top 5
    print("-" * 60)
    print("SAMPLE PQS MESSAGES (Top 5)")
    print("-" * 60)
    pqs_gen = PQSMessageGenerator()
    pvp_gen = PVPMessageGenerator()

    messages_output = []

    for i, item in enumerate(scored[:5], 1):
        p = item['prospect']
        s = item['score']

        pqs = pqs_gen.generate(p, s)
        pvp = pvp_gen.generate(p, s)

        print(f"\n{'='*50}")
        print(f"PROSPECT {i}: {p.company_name}")
        print(f"Score: {s['total_score']}/100")
        print(f"Contact: {p.boss_name} <{p.boss_email}>")
        print(f"{'='*50}")

        print(f"\n--- PQS MESSAGE ---")
        print(f"Subject: {pqs['subject']}")
        print(f"\n{pqs['body']}")

        print(f"\n--- PVP MESSAGE ---")
        print(f"Subject: {pvp['subject']}")
        print(f"\n{pvp['body']}")

        messages_output.append({
            'company': p.company_name,
            'contact_name': p.boss_name,
            'contact_email': p.boss_email,
            'contact_title': p.boss_title,
            'score': s['total_score'],
            'pqs_subject': pqs['subject'],
            'pqs_body': pqs['body'],
            'pvp_subject': pvp['subject'],
            'pvp_body': pvp['body'],
        })

    # Save full results to JSON
    print("\n" + "-" * 60)
    print("SAVING RESULTS")
    print("-" * 60)

    full_results = {
        'analysis_date': datetime.now().isoformat(),
        'total_prospects': len(prospects),
        'qualified_count': len(qualified),
        'dataset_analysis': analysis,
        'top_prospects': [
            {
                'rank': i + 1,
                'company': item['prospect'].company_name,
                'job_title': item['prospect'].job_title,
                'location': item['prospect'].location,
                'domain': item['prospect'].domain,
                'contact_name': item['prospect'].boss_name,
                'contact_title': item['prospect'].boss_title,
                'contact_email': item['prospect'].boss_email,
                'contact_linkedin': item['prospect'].boss_linkedin,
                'score': item['score']['total_score'],
                'score_breakdown': item['score']['breakdown'],
                'qualifies': item['score']['qualifies'],
            }
            for i, item in enumerate(scored[:50])
        ],
        'sample_messages': messages_output,
    }

    with open('gtmops_analysis_results.json', 'w') as f:
        json.dump(full_results, f, indent=2)
    print("Saved full results to: gtmops_analysis_results.json")

    # Save qualified prospects CSV
    with open('gtmops_qualified_prospects.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Rank', 'Score', 'Company', 'Job Title', 'Location', 'Domain',
            'Contact Name', 'Contact Title', 'Contact Email', 'Contact LinkedIn'
        ])
        for i, item in enumerate(qualified, 1):
            p = item['prospect']
            s = item['score']
            writer.writerow([
                i, s['total_score'], p.company_name, p.job_title, p.location,
                p.domain, p.boss_name, p.boss_title, p.boss_email, p.boss_linkedin
            ])
    print(f"Saved {len(qualified)} qualified prospects to: gtmops_qualified_prospects.csv")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
