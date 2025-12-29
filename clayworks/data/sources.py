"""
ClayWorks Data Sources Module
=============================

Three-Tier Data Architecture for GTM:

Tier 1: Foundational Records (High Reliability)
    - Government registries
    - Industry-specific databases
    - Official certification/compliance registries
    - Public financial filings

Tier 2: Activity & Operations Signals
    - Job postings
    - Employee count changes
    - Technology stack
    - Funding/M&A activity
    - Leadership changes

Tier 3: Market Voice (Qualitative Signals)
    - Reviews (G2/Capterra)
    - Industry forums/communities
    - Conference presentations
    - Blog posts/podcasts
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json


class DataTier(Enum):
    """Data source tier classification."""
    FOUNDATIONAL = 1  # High reliability records
    ACTIVITY = 2      # Operations and activity signals
    MARKET_VOICE = 3  # Qualitative signals


class AccessMethod(Enum):
    """Methods for accessing data sources."""
    API = "api"
    SCRAPE = "scrape"
    MANUAL = "manual"
    DATABASE = "database"
    WEBHOOK = "webhook"
    IMPORT = "import"


class UpdateFrequency(Enum):
    """How often data should be refreshed."""
    REALTIME = "realtime"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


@dataclass
class DataSource:
    """
    A data source definition.

    Example sources by tier:
    - Tier 1: SAM.gov, SEC filings, State registries
    - Tier 2: LinkedIn Jobs, BuiltWith, Crunchbase
    - Tier 3: G2 Reviews, Reddit, Industry forums
    """
    name: str
    tier: DataTier
    access_method: AccessMethod
    update_frequency: UpdateFrequency
    description: str = ""
    base_url: Optional[str] = None
    api_key_env: Optional[str] = None
    rate_limit: Optional[int] = None  # requests per minute
    fields_provided: List[str] = field(default_factory=list)
    enabled: bool = True
    last_synced: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "tier": self.tier.value,
            "access_method": self.access_method.value,
            "update_frequency": self.update_frequency.value,
            "description": self.description,
            "base_url": self.base_url,
            "api_key_env": self.api_key_env,
            "rate_limit": self.rate_limit,
            "fields_provided": self.fields_provided,
            "enabled": self.enabled,
            "last_synced": self.last_synced.isoformat() if self.last_synced else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSource":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            tier=DataTier(data["tier"]),
            access_method=AccessMethod(data["access_method"]),
            update_frequency=UpdateFrequency(data["update_frequency"]),
            description=data.get("description", ""),
            base_url=data.get("base_url"),
            api_key_env=data.get("api_key_env"),
            rate_limit=data.get("rate_limit"),
            fields_provided=data.get("fields_provided", []),
            enabled=data.get("enabled", True),
            last_synced=datetime.fromisoformat(data["last_synced"]) if data.get("last_synced") else None,
            metadata=data.get("metadata", {}),
        )


@dataclass
class DataSourceQuery:
    """A query against a data source."""
    source_name: str
    query_params: Dict[str, Any]
    fields_requested: List[str]
    filters: Dict[str, Any] = field(default_factory=dict)


class DataSourceManager:
    """
    Manages data sources across all three tiers.

    Questions each tier should answer:

    Tier 1 - Foundational:
        - What are they legally obligated to do?
        - What certifications/licenses do they hold or need?
        - What contracts/obligations are on record?

    Tier 2 - Activity:
        - What are they actively hiring for? (reveals gaps/priorities)
        - How is their team structured? (reveals capacity)
        - What technology do they use? (reveals maturity/gaps)
        - Recent funding? (reveals growth pressure/resources)

    Tier 3 - Market Voice:
        - What are they complaining about?
        - What solutions have they tried and rejected?
        - What language do they use to describe their problems?
    """

    def __init__(self):
        self.sources: Dict[str, DataSource] = {}
        self._data_fetchers: Dict[str, Callable] = {}

    def add_source(self, source: DataSource) -> None:
        """Add a data source."""
        self.sources[source.name] = source

    def register_fetcher(
        self, source_name: str, fetcher: Callable[[DataSourceQuery], Dict[str, Any]]
    ) -> None:
        """Register a data fetching function for a source."""
        self._data_fetchers[source_name] = fetcher

    def get_source(self, name: str) -> Optional[DataSource]:
        """Get a data source by name."""
        return self.sources.get(name)

    def get_tier_sources(self, tier: DataTier) -> List[DataSource]:
        """Get all sources for a specific tier."""
        return [s for s in self.sources.values() if s.tier == tier]

    def get_enabled_sources(self) -> List[DataSource]:
        """Get all enabled sources."""
        return [s for s in self.sources.values() if s.enabled]

    def fetch_data(
        self, query: DataSourceQuery
    ) -> Dict[str, Any]:
        """
        Fetch data from a source.

        Args:
            query: Query specification

        Returns:
            Dictionary with fetched data
        """
        source = self.sources.get(query.source_name)
        if not source:
            raise ValueError(f"Unknown source: {query.source_name}")

        if not source.enabled:
            raise ValueError(f"Source disabled: {query.source_name}")

        fetcher = self._data_fetchers.get(query.source_name)
        if not fetcher:
            raise ValueError(f"No fetcher registered for: {query.source_name}")

        result = fetcher(query)

        # Update last synced
        source.last_synced = datetime.now()

        return result

    def aggregate_prospect_data(
        self, prospect_id: str, queries: List[DataSourceQuery]
    ) -> Dict[str, Any]:
        """
        Aggregate data from multiple sources for a prospect.

        Returns combined data from all queried sources.
        """
        aggregated = {"prospect_id": prospect_id, "sources": {}}

        for query in queries:
            try:
                data = self.fetch_data(query)
                aggregated["sources"][query.source_name] = {
                    "data": data,
                    "success": True,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                aggregated["sources"][query.source_name] = {
                    "data": None,
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }

        return aggregated

    def export_sources(self, filepath: str) -> None:
        """Export all sources to JSON file."""
        data = {
            name: source.to_dict()
            for name, source in self.sources.items()
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def import_sources(self, filepath: str) -> None:
        """Import sources from JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)

        for name, source_data in data.items():
            source = DataSource.from_dict(source_data)
            self.add_source(source)


# Pre-built common data sources
COMMON_SOURCES = {
    # Tier 1: Foundational Records
    "sam_gov": DataSource(
        name="sam_gov",
        tier=DataTier.FOUNDATIONAL,
        access_method=AccessMethod.API,
        update_frequency=UpdateFrequency.DAILY,
        description="System for Award Management - Federal contracts",
        base_url="https://api.sam.gov",
        fields_provided=["contract_awards", "registrations", "exclusions"],
    ),
    "sec_filings": DataSource(
        name="sec_filings",
        tier=DataTier.FOUNDATIONAL,
        access_method=AccessMethod.API,
        update_frequency=UpdateFrequency.DAILY,
        description="SEC EDGAR filings",
        base_url="https://data.sec.gov",
        fields_provided=["10k", "10q", "8k", "financial_data"],
    ),
    "state_registry": DataSource(
        name="state_registry",
        tier=DataTier.FOUNDATIONAL,
        access_method=AccessMethod.MANUAL,
        update_frequency=UpdateFrequency.MONTHLY,
        description="State business registrations",
        fields_provided=["incorporation_date", "registered_agent", "status"],
    ),

    # Tier 2: Activity Signals
    "linkedin_jobs": DataSource(
        name="linkedin_jobs",
        tier=DataTier.ACTIVITY,
        access_method=AccessMethod.SCRAPE,
        update_frequency=UpdateFrequency.DAILY,
        description="LinkedIn job postings",
        base_url="https://www.linkedin.com/jobs",
        rate_limit=100,
        fields_provided=["job_title", "posted_date", "description", "requirements"],
    ),
    "builtwith": DataSource(
        name="builtwith",
        tier=DataTier.ACTIVITY,
        access_method=AccessMethod.API,
        update_frequency=UpdateFrequency.WEEKLY,
        description="Technology stack detection",
        base_url="https://api.builtwith.com",
        api_key_env="BUILTWITH_API_KEY",
        fields_provided=["technologies", "first_detected", "last_detected"],
    ),
    "crunchbase": DataSource(
        name="crunchbase",
        tier=DataTier.ACTIVITY,
        access_method=AccessMethod.API,
        update_frequency=UpdateFrequency.WEEKLY,
        description="Funding and company data",
        base_url="https://api.crunchbase.com",
        api_key_env="CRUNCHBASE_API_KEY",
        fields_provided=["funding_rounds", "investors", "employee_count", "founded_date"],
    ),
    "linkedin_company": DataSource(
        name="linkedin_company",
        tier=DataTier.ACTIVITY,
        access_method=AccessMethod.SCRAPE,
        update_frequency=UpdateFrequency.WEEKLY,
        description="LinkedIn company profiles",
        rate_limit=50,
        fields_provided=["employee_count", "follower_count", "specialties", "updates"],
    ),

    # Tier 3: Market Voice
    "g2_reviews": DataSource(
        name="g2_reviews",
        tier=DataTier.MARKET_VOICE,
        access_method=AccessMethod.SCRAPE,
        update_frequency=UpdateFrequency.WEEKLY,
        description="G2 software reviews",
        base_url="https://www.g2.com",
        fields_provided=["rating", "review_text", "pros", "cons", "use_case"],
    ),
    "reddit": DataSource(
        name="reddit",
        tier=DataTier.MARKET_VOICE,
        access_method=AccessMethod.API,
        update_frequency=UpdateFrequency.DAILY,
        description="Reddit discussions",
        base_url="https://www.reddit.com",
        fields_provided=["posts", "comments", "subreddit", "sentiment"],
    ),
    "industry_forums": DataSource(
        name="industry_forums",
        tier=DataTier.MARKET_VOICE,
        access_method=AccessMethod.SCRAPE,
        update_frequency=UpdateFrequency.WEEKLY,
        description="Industry-specific forums and communities",
        fields_provided=["discussions", "pain_points", "recommendations"],
    ),
}


def create_default_source_manager() -> DataSourceManager:
    """Create a DataSourceManager with common sources pre-configured."""
    manager = DataSourceManager()
    for source in COMMON_SOURCES.values():
        manager.add_source(source)
    return manager
