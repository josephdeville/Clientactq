"""
ClayWorks Helpers Module
========================

Helper functions for the ClayWorks framework.
"""

import re
from typing import Optional, Any, Union
from datetime import datetime, date


def slugify(text: str) -> str:
    """
    Convert text to a URL-safe slug.

    Args:
        text: Input text

    Returns:
        Slugified string
    """
    # Convert to lowercase
    slug = text.lower()

    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)

    # Remove non-alphanumeric characters (except hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)

    # Remove consecutive hyphens
    slug = re.sub(r'-+', '-', slug)

    # Remove leading/trailing hyphens
    slug = slug.strip('-')

    return slug


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)].rstrip() + suffix


def format_currency(
    amount: Union[int, float],
    currency: str = "USD",
    compact: bool = False,
) -> str:
    """
    Format a number as currency.

    Args:
        amount: Amount to format
        currency: Currency code
        compact: Use compact notation (K, M, B)

    Returns:
        Formatted currency string
    """
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "$")

    if compact:
        if amount >= 1_000_000_000:
            return f"{symbol}{amount / 1_000_000_000:.1f}B"
        if amount >= 1_000_000:
            return f"{symbol}{amount / 1_000_000:.1f}M"
        if amount >= 1_000:
            return f"{symbol}{amount / 1_000:.1f}K"

    return f"{symbol}{amount:,.0f}"


def format_percentage(
    value: float,
    decimal_places: int = 1,
    include_sign: bool = False,
) -> str:
    """
    Format a decimal as a percentage.

    Args:
        value: Decimal value (0.15 = 15%)
        decimal_places: Number of decimal places
        include_sign: Include + for positive values

    Returns:
        Formatted percentage string
    """
    percentage = value * 100

    if include_sign and percentage > 0:
        return f"+{percentage:.{decimal_places}f}%"

    return f"{percentage:.{decimal_places}f}%"


def parse_date(
    date_str: str,
    formats: Optional[list] = None,
) -> Optional[datetime]:
    """
    Parse a date string in various formats.

    Args:
        date_str: Date string to parse
        formats: List of format strings to try

    Returns:
        Parsed datetime or None
    """
    if formats is None:
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%SZ",
        ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    return None


def get_week_string(dt: Optional[datetime] = None) -> str:
    """
    Get a week string in format YYYY-WXX.

    Args:
        dt: Datetime (defaults to now)

    Returns:
        Week string like "2024-W01"
    """
    if dt is None:
        dt = datetime.now()

    year = dt.year
    week = dt.isocalendar()[1]

    return f"{year}-W{week:02d}"


def days_until(target_date: Union[datetime, date, str]) -> int:
    """
    Calculate days until a target date.

    Args:
        target_date: Target date

    Returns:
        Number of days (negative if past)
    """
    if isinstance(target_date, str):
        parsed = parse_date(target_date)
        if parsed is None:
            raise ValueError(f"Cannot parse date: {target_date}")
        target_date = parsed

    if isinstance(target_date, datetime):
        target_date = target_date.date()

    today = date.today()
    delta = target_date - today

    return delta.days


def normalize_company_name(name: str) -> str:
    """
    Normalize a company name for matching.

    Args:
        name: Company name

    Returns:
        Normalized name
    """
    # Convert to lowercase
    normalized = name.lower()

    # Remove common suffixes
    suffixes = [
        r'\s*,?\s*(inc\.?|incorporated)$',
        r'\s*,?\s*(llc|l\.l\.c\.)$',
        r'\s*,?\s*(ltd\.?|limited)$',
        r'\s*,?\s*(corp\.?|corporation)$',
        r'\s*,?\s*(co\.?)$',
    ]

    for suffix in suffixes:
        normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)

    # Remove extra whitespace
    normalized = ' '.join(normalized.split())

    return normalized.strip()


def extract_domain(url_or_email: str) -> Optional[str]:
    """
    Extract domain from URL or email.

    Args:
        url_or_email: URL or email address

    Returns:
        Domain string or None
    """
    if "@" in url_or_email:
        # Email
        parts = url_or_email.split("@")
        if len(parts) == 2:
            return parts[1].lower()
    else:
        # URL
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url_or_email)
            domain = parsed.netloc or parsed.path.split("/")[0]
            # Remove www prefix
            if domain.startswith("www."):
                domain = domain[4:]
            return domain.lower()
        except Exception:
            pass

    return None


def safe_get(data: dict, *keys: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary values.

    Args:
        data: Dictionary to query
        *keys: Keys to traverse
        default: Default value if not found

    Returns:
        Value or default
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def merge_dicts(*dicts: dict) -> dict:
    """
    Deep merge multiple dictionaries.

    Args:
        *dicts: Dictionaries to merge

    Returns:
        Merged dictionary
    """
    result = {}

    for d in dicts:
        if d is None:
            continue

        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge_dicts(result[key], value)
            else:
                result[key] = value

    return result
