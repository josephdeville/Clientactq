"""
ClayWorks Validators Module
===========================

Input validation utilities for the ClayWorks framework.
"""

import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


def validate_email(email: str) -> Dict[str, Any]:
    """
    Validate an email address.

    Returns:
        Dict with 'valid' bool and optional 'error' message
    """
    if not email:
        return {"valid": False, "error": "Email is required"}

    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(pattern, email):
        return {"valid": False, "error": "Invalid email format"}

    # Check for common issues
    if ".." in email:
        return {"valid": False, "error": "Email contains consecutive dots"}

    if email.startswith(".") or email.endswith("."):
        return {"valid": False, "error": "Email cannot start or end with a dot"}

    return {"valid": True}


def validate_url(url: str) -> Dict[str, Any]:
    """
    Validate a URL.

    Returns:
        Dict with 'valid' bool and optional 'error' message
    """
    if not url:
        return {"valid": False, "error": "URL is required"}

    try:
        result = urlparse(url)

        if not result.scheme:
            return {"valid": False, "error": "URL must include scheme (http/https)"}

        if result.scheme not in ["http", "https"]:
            return {"valid": False, "error": "URL scheme must be http or https"}

        if not result.netloc:
            return {"valid": False, "error": "URL must include domain"}

        return {"valid": True, "domain": result.netloc}

    except Exception as e:
        return {"valid": False, "error": f"Invalid URL: {str(e)}"}


def validate_company_name(name: str) -> Dict[str, Any]:
    """
    Validate a company name.

    Returns:
        Dict with 'valid' bool and optional 'error' message
    """
    if not name:
        return {"valid": False, "error": "Company name is required"}

    if len(name) < 2:
        return {"valid": False, "error": "Company name too short"}

    if len(name) > 200:
        return {"valid": False, "error": "Company name too long"}

    # Check for suspicious patterns
    suspicious_patterns = [
        r"^[0-9]+$",  # All numbers
        r"^[\W]+$",   # All special characters
    ]

    for pattern in suspicious_patterns:
        if re.match(pattern, name):
            return {"valid": False, "error": "Company name appears invalid"}

    return {"valid": True, "normalized": name.strip()}


def validate_prospect_data(
    data: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Validate prospect data completeness and quality.

    Args:
        data: Prospect data dictionary
        required_fields: List of required field names

    Returns:
        Dict with validation results
    """
    if required_fields is None:
        required_fields = ["company_name", "contact_email"]

    issues = []
    warnings = []

    # Check required fields
    for field in required_fields:
        if field not in data or not data[field]:
            issues.append(f"Missing required field: {field}")

    # Validate specific fields if present
    if "contact_email" in data and data["contact_email"]:
        email_result = validate_email(data["contact_email"])
        if not email_result["valid"]:
            issues.append(f"Invalid email: {email_result['error']}")

    if "company_website" in data and data["company_website"]:
        url_result = validate_url(data["company_website"])
        if not url_result["valid"]:
            warnings.append(f"Invalid website URL: {url_result['error']}")

    if "company_name" in data and data["company_name"]:
        name_result = validate_company_name(data["company_name"])
        if not name_result["valid"]:
            issues.append(f"Invalid company name: {name_result['error']}")

    # Check for data quality
    if "employee_count" in data:
        try:
            count = int(data["employee_count"])
            if count < 0:
                warnings.append("Employee count is negative")
            if count > 10000000:
                warnings.append("Employee count seems unusually high")
        except (ValueError, TypeError):
            warnings.append("Employee count is not a valid number")

    # Calculate completeness score
    all_fields = [
        "company_name", "contact_email", "contact_first_name",
        "contact_last_name", "contact_title", "company_website",
        "industry", "employee_count", "funding_stage", "tech_stack",
    ]
    present_fields = sum(1 for f in all_fields if f in data and data[f])
    completeness = present_fields / len(all_fields)

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "completeness": completeness,
        "fields_present": present_fields,
        "fields_total": len(all_fields),
    }


def validate_recipe_conditions(conditions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate recipe condition definitions.

    Returns:
        Dict with validation results
    """
    valid_operators = [
        "equals", "not_equals", "contains", "not_contains",
        "greater_than", "less_than", "greater_or_equal", "less_or_equal",
        "in_list", "not_in_list", "exists", "not_exists",
        "matches_regex", "within_days",
    ]

    issues = []

    for i, condition in enumerate(conditions):
        if "field" not in condition:
            issues.append(f"Condition {i}: missing 'field'")

        if "operator" not in condition:
            issues.append(f"Condition {i}: missing 'operator'")
        elif condition["operator"] not in valid_operators:
            issues.append(f"Condition {i}: invalid operator '{condition['operator']}'")

        if "value" not in condition and condition.get("operator") not in ["exists", "not_exists"]:
            issues.append(f"Condition {i}: missing 'value'")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "condition_count": len(conditions),
    }


def validate_scoring_model(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Validate a scoring model definition.

    Returns:
        Dict with validation results
    """
    issues = []
    warnings = []

    total_points = 0
    total_weight = 0

    for i, component in enumerate(components):
        if "name" not in component:
            issues.append(f"Component {i}: missing 'name'")

        if "points" not in component:
            issues.append(f"Component {i}: missing 'points'")
        else:
            try:
                points = int(component["points"])
                total_points += points
                if points < 0:
                    issues.append(f"Component {i}: points cannot be negative")
                if points > 50:
                    warnings.append(f"Component {i}: high point value ({points})")
            except (ValueError, TypeError):
                issues.append(f"Component {i}: points must be a number")

        if "weight_percentage" in component:
            try:
                weight = float(component["weight_percentage"])
                total_weight += weight
            except (ValueError, TypeError):
                warnings.append(f"Component {i}: weight_percentage should be a number")

    # Check total weight sums to 100
    if total_weight > 0 and abs(total_weight - 100) > 0.1:
        warnings.append(f"Total weight is {total_weight}, should be 100")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "total_points": total_points,
        "total_weight": total_weight,
        "component_count": len(components),
    }
