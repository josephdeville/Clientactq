#!/usr/bin/env python3
"""
Audio Software Companies Scraper - Batch 3
Scrapes Native Instruments, Arturia, Output, Spectrasonics, Spitfire Audio, Splice
"""

import os
import csv
import json
import time
import re
import requests
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin
from html2text import html2text

import pandas as pd
from dotenv import load_dotenv
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
RATE_LIMIT_DELAY = 1  # seconds between requests
MAX_RETRIES = 3
REQUEST_TIMEOUT = 15

# Page path variations to try
PAGE_PATHS = {
    "homepage": [""],
    "pricing": ["/pricing", "/buy", "/shop", "/plans", "/store", "/products"],
    "careers": ["/careers", "/jobs", "/join-us", "/company/careers", "/about/careers"],
    "blog": ["/blog", "/resources", "/news", "/learn", "/articles"],
    "about": ["/about", "/company", "/about-us", "/our-story"],
}

# Analysis prompts
HOMEPAGE_PROMPT = """Analyze this homepage content and extract:
1. Primary value proposition (1-2 sentences)
2. Target customer type (e.g., "professional audio engineers", "music producers")
3. Pricing model mentioned (if any: subscription, perpetual, freemium, etc.)
4. Free trial/demo offering (yes/no + details)
5. Community links (Discord, forum, Slack, etc.)

Return as JSON with keys: value_proposition, target_customer, pricing_model_hint, free_trial_demo, community_links
If info not found, use null."""

PRICING_PROMPT = """Analyze this pricing page and extract:
1. Pricing model (subscription/perpetual/both/rent-to-own/freemium)
2. All price points and tiers (list each tier with name and price)
3. Free trial details (duration, limitations)
4. Educational/student discounts available

Return as JSON with keys: pricing_model, price_tiers, free_trial_details, educational_discount
If info not found, use null."""

CAREERS_PROMPT = """Analyze this careers page and extract:
1. Any GTM roles open? (Sales, Marketing, Growth, DevRel, Community, Partnerships)
2. List specific GTM job titles if found
3. Company growth signals (hiring aggressively, new offices, team expansion mentions)
4. Total number of open positions if shown

Return as JSON with keys: has_gtm_roles, gtm_job_titles, growth_signals, total_open_positions
If info not found, use null."""

BLOG_PROMPT = """Analyze this blog/resources page and extract:
1. Last 3 post titles and their dates (if visible)
2. Estimated publishing frequency (daily/weekly/monthly/sporadic)
3. Content type focus (tutorials, product updates, industry news, user stories)

Return as JSON with keys: recent_posts, publishing_frequency, content_focus
If info not found, use null."""

ABOUT_PROMPT = """Analyze this about page and extract:
1. Year founded
2. Acquisition status (independent, acquired by X, parent company)
3. Company size hints (employee count, team descriptions)
4. Headquarters location

Return as JSON with keys: year_founded, acquisition_status, company_size, headquarters
If info not found, use null."""

GTM_SYNTHESIS_PROMPT = """Based on this company data, provide:

1. GTM Strategy Summary (2-3 sentences describing their go-to-market approach)
2. GTM Gaps & Opportunities (2-3 bullet points on what they could improve)
3. Opportunity Score (1-10, where 10 = highest opportunity for GTM consulting engagement)

Score criteria:
- 8-10: Growing company, hiring GTM roles, active content, modern pricing
- 5-7: Established but could modernize, some gaps in GTM
- 1-4: Mature/static, limited growth signals, or already optimized

Company Data:
{company_data}

Return as JSON with keys: gtm_strategy_summary, gtm_gaps_opportunities (as array of strings), opportunity_score (as integer)"""


class CompanyScraper:
    def __init__(self):
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")

        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = []

    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page and convert to markdown."""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            if response.status_code == 200:
                # Convert HTML to markdown
                markdown = html2text(response.text)
                return markdown
            else:
                print(f"    Status {response.status_code}")
            return None
        except Exception as e:
            print(f"    Error fetching {url}: {e}")
            return None

    def find_and_scrape_page(self, base_url: str, page_type: str) -> Optional[str]:
        """Try multiple path variations to find and scrape a page."""
        paths = PAGE_PATHS.get(page_type, [""])

        for path in paths:
            url = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
            time.sleep(RATE_LIMIT_DELAY)

            print(f"    Trying: {url}")
            content = self.fetch_page(url)
            if content and len(content) > 200:  # Minimum content threshold
                print(f"    ✓ Found {page_type}")
                return content

        print(f"    ✗ No {page_type} page found")
        return None

    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def analyze_with_claude(self, content: str, prompt: str) -> dict:
        """Analyze content using Claude API."""
        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}\n\nContent to analyze:\n{content[:15000]}"
                    }
                ]
            )

            response_text = response.content[0].text

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except json.JSONDecodeError:
            print(f"    JSON decode error")
            return {}
        except Exception as e:
            print(f"    Claude analysis error: {e}")
            return {}

    def synthesize_gtm(self, company_data: dict) -> dict:
        """Generate GTM synthesis from all collected data."""
        data_summary = json.dumps(company_data, indent=2, default=str)

        try:
            response = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[
                    {
                        "role": "user",
                        "content": GTM_SYNTHESIS_PROMPT.format(company_data=data_summary)
                    }
                ]
            )

            response_text = response.content[0].text
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            print(f"    GTM synthesis error: {e}")
            return {}

    def process_company(self, company: dict) -> dict:
        """Process a single company - scrape all pages and analyze."""
        name = company['Company Name']
        website = company['Website']

        print(f"\n{'='*80}")
        print(f"Processing: {name}")
        print(f"Website: {website}")
        print('='*80)

        result = {
            'company_name': name,
            'description': company['Description'],
            'website': website,
            'linkedin': company['LinkedIn'],
            'scrape_timestamp': datetime.now().isoformat(),
        }

        # Scrape and analyze each page type
        page_analyses = {}

        # Homepage
        print("\n[1/5] HOMEPAGE")
        homepage_content = self.find_and_scrape_page(website, "homepage")
        if homepage_content:
            homepage_analysis = self.analyze_with_claude(homepage_content, HOMEPAGE_PROMPT)
            page_analyses['homepage'] = homepage_analysis
            result.update({
                'value_proposition': homepage_analysis.get('value_proposition'),
                'target_customer': homepage_analysis.get('target_customer'),
                'pricing_model_hint': homepage_analysis.get('pricing_model_hint'),
                'free_trial_demo': homepage_analysis.get('free_trial_demo'),
                'community_links': homepage_analysis.get('community_links'),
            })

        # Pricing page
        print("\n[2/5] PRICING")
        pricing_content = self.find_and_scrape_page(website, "pricing")
        if pricing_content:
            pricing_analysis = self.analyze_with_claude(pricing_content, PRICING_PROMPT)
            page_analyses['pricing'] = pricing_analysis
            result.update({
                'pricing_model': pricing_analysis.get('pricing_model'),
                'price_tiers': pricing_analysis.get('price_tiers'),
                'free_trial_details': pricing_analysis.get('free_trial_details'),
                'educational_discount': pricing_analysis.get('educational_discount'),
            })

        # Careers page
        print("\n[3/5] CAREERS")
        careers_content = self.find_and_scrape_page(website, "careers")
        if careers_content:
            careers_analysis = self.analyze_with_claude(careers_content, CAREERS_PROMPT)
            page_analyses['careers'] = careers_analysis
            result.update({
                'has_gtm_roles': careers_analysis.get('has_gtm_roles'),
                'gtm_job_titles': careers_analysis.get('gtm_job_titles'),
                'growth_signals': careers_analysis.get('growth_signals'),
                'total_open_positions': careers_analysis.get('total_open_positions'),
            })

        # Blog page
        print("\n[4/5] BLOG")
        blog_content = self.find_and_scrape_page(website, "blog")
        if blog_content:
            blog_analysis = self.analyze_with_claude(blog_content, BLOG_PROMPT)
            page_analyses['blog'] = blog_analysis
            result.update({
                'recent_posts': blog_analysis.get('recent_posts'),
                'publishing_frequency': blog_analysis.get('publishing_frequency'),
                'content_focus': blog_analysis.get('content_focus'),
            })

        # About page
        print("\n[5/5] ABOUT")
        about_content = self.find_and_scrape_page(website, "about")
        if about_content:
            about_analysis = self.analyze_with_claude(about_content, ABOUT_PROMPT)
            page_analyses['about'] = about_analysis
            result.update({
                'year_founded': about_analysis.get('year_founded'),
                'acquisition_status': about_analysis.get('acquisition_status'),
                'company_size': about_analysis.get('company_size'),
                'headquarters': about_analysis.get('headquarters'),
            })

        # GTM Synthesis
        print("\n[SYNTHESIS] Analyzing GTM strategy...")
        gtm_synthesis = self.synthesize_gtm({
            'company': name,
            'description': company['Description'],
            **page_analyses
        })
        result.update({
            'gtm_strategy_summary': gtm_synthesis.get('gtm_strategy_summary'),
            'gtm_gaps_opportunities': gtm_synthesis.get('gtm_gaps_opportunities'),
            'opportunity_score': gtm_synthesis.get('opportunity_score'),
        })

        print(f"\n✓ Completed: {name}")
        return result

    def process_all_companies(self, input_csv: str):
        """Process all companies from CSV and return results."""
        # Read input CSV
        df = pd.read_csv(input_csv)
        companies = df.to_dict('records')

        print(f"\n{'#'*80}")
        print(f"# BATCH 3 SCRAPING - {len(companies)} companies")
        print(f"# Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'#'*80}\n")

        results = []
        for i, company in enumerate(companies, 1):
            print(f"\n\n[COMPANY {i}/{len(companies)}]")
            try:
                result = self.process_company(company)
                results.append(result)

            except Exception as e:
                print(f"\n✗ FAILED: {company['Company Name']} - {e}")
                results.append({
                    'company_name': company['Company Name'],
                    'description': company['Description'],
                    'website': company['Website'],
                    'linkedin': company['LinkedIn'],
                    'error': str(e)
                })

        return results


def main():
    input_csv = "batch3_companies.csv"

    scraper = CompanyScraper()
    results = scraper.process_all_companies(input_csv)

    # Save as JSON
    output_file = f"batch3_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n\n{'#'*80}")
    print(f"# SCRAPING COMPLETE")
    print(f"# Results saved to: {output_file}")
    print(f"# Total companies: {len(results)}")
    print(f"{'#'*80}\n")

    # Print summary
    print("\nJSON OUTPUT:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
