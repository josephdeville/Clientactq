#!/usr/bin/env python3
"""Compile all batch JSON files into a single enriched CSV."""

import json
import pandas as pd
from pathlib import Path

def flatten_company(company: dict, source_file: str) -> dict:
    """Flatten nested company data for CSV."""
    flat = {
        'Company Name': company.get('company_name', company.get('Company Name', '')),
        'Website': company.get('website', company.get('Website', '')),
        'LinkedIn': company.get('linkedin', company.get('LinkedIn', '')),
        'Description': company.get('description', company.get('Description', '')),
    }

    # Homepage data
    hp = company.get('homepage_data', company.get('homepage_general', company.get('homepage', {})))
    if hp:
        flat['Value Proposition'] = hp.get('value_proposition', '')
        flat['Target Customer'] = hp.get('target_customer', '')
        flat['Pricing Model Hint'] = hp.get('pricing_model_hint', '')
        flat['Free Trial/Demo'] = hp.get('free_trial_demo', '')
        flat['Community Links'] = str(hp.get('community_links', '')) if hp.get('community_links') else ''

    # Pricing data
    pricing = company.get('pricing_data', company.get('pricing', {}))
    if pricing:
        flat['Pricing Model'] = pricing.get('pricing_model', '')
        tiers = pricing.get('price_tiers', [])
        if tiers:
            flat['Price Tiers'] = json.dumps(tiers) if isinstance(tiers, list) else str(tiers)
        flat['Free Trial Details'] = pricing.get('free_trial_details', '')
        flat['Subscription Platform'] = pricing.get('subscription_platform', '')
        flat['Educational Discount'] = pricing.get('educational_discount', '')

    # Careers data
    careers = company.get('careers_data', company.get('careers', {}))
    if careers:
        flat['Has GTM Roles'] = careers.get('has_gtm_roles', '')
        gtm_titles = careers.get('gtm_job_titles', [])
        if gtm_titles:
            flat['GTM Job Titles'] = json.dumps(gtm_titles) if isinstance(gtm_titles, list) else str(gtm_titles)
        flat['Growth Signals'] = str(careers.get('growth_signals', ''))
        flat['Total Open Positions'] = careers.get('total_open_positions', '')

    # Blog data
    blog = company.get('blog_data', company.get('blog', company.get('blog_content', {})))
    if blog:
        posts = blog.get('recent_posts', [])
        if posts:
            flat['Recent Posts'] = json.dumps(posts) if isinstance(posts, list) else str(posts)
        flat['Publishing Frequency'] = blog.get('publishing_frequency', '')
        flat['Content Focus'] = blog.get('content_focus', '')
        flat['Educational Programs'] = blog.get('educational_programs', '')

    # About data
    about = company.get('about_data', company.get('about', {}))
    if about:
        flat['Year Founded'] = about.get('year_founded', '')
        flat['Acquisition Status'] = about.get('acquisition_status', '')
        flat['Company Size'] = about.get('company_size', '')
        flat['Headquarters'] = about.get('headquarters', '')
        flat['Recent Milestones'] = about.get('recent_milestones', '')

    # GTM Synthesis
    flat['GTM Strategy Summary'] = company.get('gtm_strategy_summary', '')
    flat['GTM Gaps & Opportunities'] = str(company.get('gtm_gaps_opportunities', ''))
    flat['Opportunity Score'] = company.get('opportunity_score', '')
    flat['Source File'] = source_file

    return flat


def main():
    json_files = [
        'batch1_gtm_analysis.json',
        'audio_companies_gtm_analysis_batch2.json',
        'batch3_gtm_analysis_enriched.json',
        'batch4_gtm_analysis.json',
        'batch5_gtm_analysis.json',
        'audio_companies_batch6_gtm_analysis.json',
        'batch7_gtm_analysis.json',
        'batch8_gtm_analysis.json',
    ]

    all_companies = []

    for json_file in json_files:
        filepath = Path(json_file)
        if not filepath.exists():
            print(f"Warning: {json_file} not found")
            continue

        print(f"Processing {json_file}...")
        with open(filepath) as f:
            data = json.load(f)

        # Handle different JSON structures
        if isinstance(data, list):
            companies = data
        elif isinstance(data, dict):
            companies = data.get('companies', [data])
        else:
            print(f"  Unexpected format in {json_file}")
            continue

        for company in companies:
            flat = flatten_company(company, json_file)
            if flat.get('Company Name'):
                all_companies.append(flat)

        print(f"  Added {len(companies)} companies")

    # Create DataFrame and save
    df = pd.DataFrame(all_companies)

    # Reorder columns
    priority_cols = [
        'Company Name', 'Website', 'LinkedIn', 'Description',
        'Opportunity Score', 'GTM Strategy Summary', 'GTM Gaps & Opportunities',
        'Value Proposition', 'Target Customer', 'Pricing Model', 'Price Tiers',
        'Has GTM Roles', 'GTM Job Titles', 'Growth Signals', 'Total Open Positions',
        'Year Founded', 'Acquisition Status', 'Company Size', 'Headquarters'
    ]

    other_cols = [c for c in df.columns if c not in priority_cols]
    df = df[[c for c in priority_cols if c in df.columns] + other_cols]

    output_file = 'audio_companies_enriched_FINAL.csv'
    df.to_csv(output_file, index=False)
    print(f"\nSaved {len(all_companies)} companies to {output_file}")

    # Print summary
    print("\n=== SUMMARY ===")
    print(f"Total companies: {len(all_companies)}")
    if 'Opportunity Score' in df.columns:
        df['Opportunity Score'] = pd.to_numeric(df['Opportunity Score'], errors='coerce')
        print("\nTop 10 Opportunity Scores:")
        top10 = df.nlargest(10, 'Opportunity Score')[['Company Name', 'Opportunity Score', 'GTM Strategy Summary']]
        for _, row in top10.iterrows():
            print(f"  {row['Opportunity Score']}/10 - {row['Company Name']}")


if __name__ == "__main__":
    main()
