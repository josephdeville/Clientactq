#!/usr/bin/env python3
"""
Audio Software Companies Scraper & GTM Analyzer
Scrapes company websites using Firecrawl and analyzes with Claude API.
"""

import os
import csv
import json
import time
import re
from datetime import datetime
from typing import Optional
from urllib.parse import urljoin

import pandas as pd
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

load_dotenv()

# Configuration
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
RATE_LIMIT_DELAY = 2  # seconds between requests
MAX_RETRIES = 3

# Page path variations to try
PAGE_PATHS = {
    "homepage": [""],
    "pricing": ["/pricing", "/buy", "/shop", "/plans", "/store", "/purchase"],
    "careers": ["/careers", "/jobs", "/join-us", "/work-with-us", "/about/careers", "/company/careers"],
    "blog": ["/blog", "/resources", "/learn", "/news", "/articles", "/insights"],
    "about": ["/about", "/company", "/about-us", "/who-we-are", "/our-story"],
}

# Analysis prompts
HOMEPAGE_PROMPT = """Analyze this homepage content and extract:
1. Primary value proposition (1-2 sentences)
2. Target customer type (e.g., "professional audio engineers", "indie game developers")
3. Pricing model mentioned (if any: subscription, perpetual, freemium, etc.)
4. Free trial/demo offering (yes/no + details)
5. Community links (Discord, forum, Slack, etc.)

Return as JSON with keys: value_proposition, target_customer, pricing_model_hint, free_trial_demo, community_links
If info not found, use null."""

PRICING_PROMPT = """Analyze this pricing page and extract:
1. Pricing model (subscription/perpetual/both/rent-to-own/freemium)
2. All price points and tiers (list each tier with name and price)
3. Free trial details (duration, limitations)
4. Subscription platform (if applicable: own platform, Splice, Plugin Alliance, etc.)
5. Educational/student discounts available

Return as JSON with keys: pricing_model, price_tiers, free_trial_details, subscription_platform, educational_discount
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
4. Any educational programs or certifications mentioned

Return as JSON with keys: recent_posts, publishing_frequency, content_focus, educational_programs
If info not found, use null."""

ABOUT_PROMPT = """Analyze this about page and extract:
1. Year founded
2. Acquisition status (independent, acquired by X, parent company)
3. Company size hints (employee count, team descriptions)
4. Recent news/milestones mentioned
5. Headquarters location

Return as JSON with keys: year_founded, acquisition_status, company_size, recent_milestones, headquarters
If info not found, use null."""

GTM_SYNTHESIS_PROMPT = """Based on this company data, provide:

1. GTM Strategy Summary (2-3 sentences describing their go-to-market approach)
2. GTM Gaps & Opportunities (2-3 bullet points on what they could improve)
3. Target Opportunity Score (1-10, where 10 = highest opportunity for GTM consulting engagement)

Score criteria:
- 8-10: Growing company, hiring GTM roles, active content, modern pricing
- 5-7: Established but could modernize, some gaps in GTM
- 1-4: Mature/static, limited growth signals, or already optimized

Company Data:
{company_data}

Return as JSON with keys: gtm_strategy_summary, gtm_gaps_opportunities, opportunity_score"""


class CompanyScraper:
    def __init__(self):
        if not FIRECRAWL_API_KEY:
            raise ValueError("FIRECRAWL_API_KEY environment variable required")
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable required")

        self.firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        self.anthropic = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.results = []

    @retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=2, max=10))
    def scrape_page(self, url: str) -> Optional[str]:
        """Scrape a single page using Firecrawl."""
        try:
            result = self.firecrawl.scrape(
                url,
                formats=['markdown'],
                only_main_content=True,
                timeout=30000
            )
            if result and hasattr(result, 'markdown') and result.markdown:
                return result.markdown
            elif result and isinstance(result, dict) and 'markdown' in result:
                return result['markdown']
            return None
        except Exception as e:
            print(f"  Error scraping {url}: {e}")
            return None

    def find_and_scrape_page(self, base_url: str, page_type: str) -> Optional[str]:
        """Try multiple path variations to find and scrape a page."""
        paths = PAGE_PATHS.get(page_type, [""])

        for path in paths:
            url = urljoin(base_url.rstrip('/') + '/', path.lstrip('/'))
            time.sleep(RATE_LIMIT_DELAY)

            content = self.scrape_page(url)
            if content and len(content) > 200:  # Minimum content threshold
                return content

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
                        "content": f"{prompt}\n\nContent to analyze:\n{content[:15000]}"  # Truncate if too long
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
            return {}
        except Exception as e:
            print(f"  Claude analysis error: {e}")
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
            print(f"  GTM synthesis error: {e}")
            return {}

    def process_company(self, company: dict) -> dict:
        """Process a single company - scrape all pages and analyze."""
        name = company['Company Name']
        website = company['Website']

        print(f"\nProcessing: {name} ({website})")

        result = {
            'Company Name': name,
            'Description': company['Description'],
            'Website': website,
            'LinkedIn': company['LinkedIn'],
            'scrape_timestamp': datetime.now().isoformat(),
        }

        # Scrape and analyze each page type
        page_analyses = {}

        # Homepage
        print("  Scraping homepage...")
        homepage_content = self.find_and_scrape_page(website, "homepage")
        if homepage_content:
            homepage_analysis = self.analyze_with_claude(homepage_content, HOMEPAGE_PROMPT)
            page_analyses['homepage'] = homepage_analysis
            result.update({
                'hp_value_proposition': homepage_analysis.get('value_proposition'),
                'hp_target_customer': homepage_analysis.get('target_customer'),
                'hp_pricing_hint': homepage_analysis.get('pricing_model_hint'),
                'hp_free_trial': homepage_analysis.get('free_trial_demo'),
                'hp_community_links': homepage_analysis.get('community_links'),
            })

        # Pricing page
        print("  Scraping pricing...")
        pricing_content = self.find_and_scrape_page(website, "pricing")
        if pricing_content:
            pricing_analysis = self.analyze_with_claude(pricing_content, PRICING_PROMPT)
            page_analyses['pricing'] = pricing_analysis
            result.update({
                'pricing_model': pricing_analysis.get('pricing_model'),
                'price_tiers': json.dumps(pricing_analysis.get('price_tiers')) if pricing_analysis.get('price_tiers') else None,
                'free_trial_details': pricing_analysis.get('free_trial_details'),
                'subscription_platform': pricing_analysis.get('subscription_platform'),
                'educational_discount': pricing_analysis.get('educational_discount'),
            })

        # Careers page
        print("  Scraping careers...")
        careers_content = self.find_and_scrape_page(website, "careers")
        if careers_content:
            careers_analysis = self.analyze_with_claude(careers_content, CAREERS_PROMPT)
            page_analyses['careers'] = careers_analysis
            result.update({
                'has_gtm_roles': careers_analysis.get('has_gtm_roles'),
                'gtm_job_titles': json.dumps(careers_analysis.get('gtm_job_titles')) if careers_analysis.get('gtm_job_titles') else None,
                'growth_signals': careers_analysis.get('growth_signals'),
                'total_open_positions': careers_analysis.get('total_open_positions'),
            })

        # Blog page
        print("  Scraping blog...")
        blog_content = self.find_and_scrape_page(website, "blog")
        if blog_content:
            blog_analysis = self.analyze_with_claude(blog_content, BLOG_PROMPT)
            page_analyses['blog'] = blog_analysis
            result.update({
                'recent_posts': json.dumps(blog_analysis.get('recent_posts')) if blog_analysis.get('recent_posts') else None,
                'publishing_frequency': blog_analysis.get('publishing_frequency'),
                'content_focus': blog_analysis.get('content_focus'),
                'educational_programs': blog_analysis.get('educational_programs'),
            })

        # About page
        print("  Scraping about...")
        about_content = self.find_and_scrape_page(website, "about")
        if about_content:
            about_analysis = self.analyze_with_claude(about_content, ABOUT_PROMPT)
            page_analyses['about'] = about_analysis
            result.update({
                'year_founded': about_analysis.get('year_founded'),
                'acquisition_status': about_analysis.get('acquisition_status'),
                'company_size': about_analysis.get('company_size'),
                'recent_milestones': about_analysis.get('recent_milestones'),
                'headquarters': about_analysis.get('headquarters'),
            })

        # GTM Synthesis
        print("  Synthesizing GTM analysis...")
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

        return result

    def process_all_companies(self, input_csv: str, output_csv: str):
        """Process all companies from CSV and save results."""
        # Read input CSV
        df = pd.read_csv(input_csv)
        companies = df.to_dict('records')

        print(f"Processing {len(companies)} companies...")

        results = []
        for company in tqdm(companies, desc="Companies"):
            try:
                result = self.process_company(company)
                results.append(result)

                # Save progress after each company
                temp_df = pd.DataFrame(results)
                temp_df.to_csv(output_csv.replace('.csv', '_progress.csv'), index=False)

            except Exception as e:
                print(f"  FAILED: {company['Company Name']} - {e}")
                results.append({
                    'Company Name': company['Company Name'],
                    'Description': company['Description'],
                    'Website': company['Website'],
                    'LinkedIn': company['LinkedIn'],
                    'error': str(e)
                })

        # Save final results
        final_df = pd.DataFrame(results)
        final_df.to_csv(output_csv, index=False)
        print(f"\nResults saved to {output_csv}")

        return final_df


def main():
    input_csv = "audio_software_companies.csv"
    output_csv = f"audio_companies_enriched_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    scraper = CompanyScraper()
    scraper.process_all_companies(input_csv, output_csv)


if __name__ == "__main__":
    main()
