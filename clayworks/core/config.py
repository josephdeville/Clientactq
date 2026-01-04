"""
ClayWorks Configuration Module
==============================

Central configuration management for the ClayWorks framework.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class DataSourceConfig:
    """Configuration for a data source."""
    name: str
    tier: int  # 1 = Foundational, 2 = Activity Signals, 3 = Market Voice
    source_type: str  # api, manual, scrape, database
    access_method: str
    update_frequency: str  # daily, weekly, monthly
    api_key_env: Optional[str] = None
    base_url: Optional[str] = None
    rate_limit: Optional[int] = None
    enabled: bool = True


@dataclass
class ScoringConfig:
    """Configuration for prospect scoring."""
    threshold_minimum: int = 70
    max_score: int = 100
    weights: Dict[str, int] = field(default_factory=lambda: {
        "obligation_urgency": 30,
        "hiring_signal": 25,
        "technology_gap": 25,
        "company_fit": 20,
    })


@dataclass
class MessagingConfig:
    """Configuration for messaging."""
    max_subject_words: int = 5
    max_email_sentences: int = 6
    personalization_fields: List[str] = field(default_factory=lambda: [
        "company_name",
        "contact_first_name",
        "specific_data_point",
        "deadline_or_trigger",
        "peer_company_example",
        "quantified_result",
    ])


@dataclass
class MetricsConfig:
    """Configuration for metrics tracking."""
    # Baseline (Traditional Outreach)
    baseline_email_response: float = 0.005  # 0.5%
    baseline_linkedin_accept: float = 0.20  # 20%
    baseline_inmail_response: float = 0.04  # 4%

    # Target (Blueprint Framework)
    target_pqs_response: float = 0.20  # 20%
    target_pvp_response: float = 0.25  # 25%
    target_linkedin_pqs: float = 0.32  # 32%


class ClayWorksConfig:
    """
    Central configuration management for ClayWorks framework.

    Usage:
        config = ClayWorksConfig()
        config.load_from_file("config.json")
        config.data_sources.append(DataSourceConfig(...))
    """

    def __init__(self, config_path: Optional[str] = None):
        self.client_name: str = ""
        self.vertical: str = ""
        self.data_sources: List[DataSourceConfig] = []
        self.scoring: ScoringConfig = ScoringConfig()
        self.messaging: MessagingConfig = MessagingConfig()
        self.metrics: MetricsConfig = MetricsConfig()
        self.custom_settings: Dict[str, Any] = {}

        if config_path:
            self.load_from_file(config_path)

    def load_from_file(self, config_path: str) -> None:
        """Load configuration from a JSON file."""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, "r") as f:
            data = json.load(f)

        self.client_name = data.get("client_name", "")
        self.vertical = data.get("vertical", "")

        # Load data sources
        for source_data in data.get("data_sources", []):
            self.data_sources.append(DataSourceConfig(**source_data))

        # Load scoring config
        if "scoring" in data:
            self.scoring = ScoringConfig(**data["scoring"])

        # Load messaging config
        if "messaging" in data:
            self.messaging = MessagingConfig(**data["messaging"])

        # Load metrics config
        if "metrics" in data:
            self.metrics = MetricsConfig(**data["metrics"])

        self.custom_settings = data.get("custom_settings", {})

    def save_to_file(self, config_path: str) -> None:
        """Save configuration to a JSON file."""
        data = {
            "client_name": self.client_name,
            "vertical": self.vertical,
            "data_sources": [
                {
                    "name": ds.name,
                    "tier": ds.tier,
                    "source_type": ds.source_type,
                    "access_method": ds.access_method,
                    "update_frequency": ds.update_frequency,
                    "api_key_env": ds.api_key_env,
                    "base_url": ds.base_url,
                    "rate_limit": ds.rate_limit,
                    "enabled": ds.enabled,
                }
                for ds in self.data_sources
            ],
            "scoring": {
                "threshold_minimum": self.scoring.threshold_minimum,
                "max_score": self.scoring.max_score,
                "weights": self.scoring.weights,
            },
            "messaging": {
                "max_subject_words": self.messaging.max_subject_words,
                "max_email_sentences": self.messaging.max_email_sentences,
                "personalization_fields": self.messaging.personalization_fields,
            },
            "metrics": {
                "baseline_email_response": self.metrics.baseline_email_response,
                "baseline_linkedin_accept": self.metrics.baseline_linkedin_accept,
                "baseline_inmail_response": self.metrics.baseline_inmail_response,
                "target_pqs_response": self.metrics.target_pqs_response,
                "target_pvp_response": self.metrics.target_pvp_response,
                "target_linkedin_pqs": self.metrics.target_linkedin_pqs,
            },
            "custom_settings": self.custom_settings,
        }

        path = Path(config_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def add_data_source(
        self,
        name: str,
        tier: int,
        source_type: str,
        access_method: str,
        update_frequency: str,
        **kwargs
    ) -> DataSourceConfig:
        """Add a new data source to the configuration."""
        source = DataSourceConfig(
            name=name,
            tier=tier,
            source_type=source_type,
            access_method=access_method,
            update_frequency=update_frequency,
            **kwargs
        )
        self.data_sources.append(source)
        return source

    def get_tier_sources(self, tier: int) -> List[DataSourceConfig]:
        """Get all data sources for a specific tier."""
        return [ds for ds in self.data_sources if ds.tier == tier]

    def get_enabled_sources(self) -> List[DataSourceConfig]:
        """Get all enabled data sources."""
        return [ds for ds in self.data_sources if ds.enabled]

    @property
    def foundational_sources(self) -> List[DataSourceConfig]:
        """Tier 1: Foundational Records (High Reliability)."""
        return self.get_tier_sources(1)

    @property
    def activity_sources(self) -> List[DataSourceConfig]:
        """Tier 2: Activity & Operations Signals."""
        return self.get_tier_sources(2)

    @property
    def market_voice_sources(self) -> List[DataSourceConfig]:
        """Tier 3: Market Voice (Qualitative Signals)."""
        return self.get_tier_sources(3)

    def validate(self) -> List[str]:
        """Validate the configuration and return any issues."""
        issues = []

        if not self.client_name:
            issues.append("Client name is required")

        if not self.vertical:
            issues.append("Vertical/industry is required")

        if not self.data_sources:
            issues.append("At least one data source is required")

        # Check for at least one source per tier
        for tier in [1, 2, 3]:
            if not self.get_tier_sources(tier):
                tier_names = {1: "Foundational", 2: "Activity", 3: "Market Voice"}
                issues.append(f"No {tier_names[tier]} (Tier {tier}) data sources configured")

        # Validate scoring weights sum to 100
        total_weight = sum(self.scoring.weights.values())
        if total_weight != 100:
            issues.append(f"Scoring weights should sum to 100, got {total_weight}")

        return issues
