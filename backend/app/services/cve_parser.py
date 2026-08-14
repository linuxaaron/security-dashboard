from datetime import datetime
from typing import Any


def parse_datetime(value: str | None) -> datetime | None:
    """Convert an NVD ISO-8601 timestamp to datetime."""
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def extract_description(
    descriptions: list[dict[str, Any]],
) -> str:
    """Return the English CVE description when available."""
    for description in descriptions:
        if description.get("lang") == "en":
            return description.get("value", "")

    return descriptions[0].get("value", "") if descriptions else ""


def extract_cvss(
    metrics: dict[str, Any],
) -> tuple[float | None, str]:
    """Extract the highest-priority available CVSS score."""

    cvss_v4 = metrics.get("cvssMetricV40", [])

    if cvss_v4:
        data = cvss_v4[0].get("cvssData", {})
        return (
            data.get("baseScore"),
            data.get("baseSeverity", "unknown").lower(),
        )

    cvss_v31 = metrics.get("cvssMetricV31", [])

    if cvss_v31:
        data = cvss_v31[0].get("cvssData", {})
        return (
            data.get("baseScore"),
            data.get("baseSeverity", "unknown").lower(),
        )

    cvss_v30 = metrics.get("cvssMetricV30", [])

    if cvss_v30:
        data = cvss_v30[0].get("cvssData", {})
        return (
            data.get("baseScore"),
            data.get("baseSeverity", "unknown").lower(),
        )

    return None, "unknown"


def extract_cwes(
    weaknesses: list[dict[str, Any]],
) -> list[str]:
    """Extract CWE identifiers."""
    cwes: list[str] = []

    for weakness in weaknesses:
        for description in weakness.get("description", []):
            value = description.get("value")

            if value and value.startswith("CWE-"):
                cwes.append(value)

    return sorted(set(cwes))


def normalize_cve(
    cve: dict[str, Any],
) -> dict[str, Any]:
    """Convert an NVD CVE object into our internal representation."""

    score, severity = extract_cvss(
        cve.get("metrics", {})
    )

    return {
        "cve_id": cve.get("id"),
        "title": cve.get("id"),
        "description": extract_description(
            cve.get("descriptions", [])
        ),
        "cvss_score": score,
        "severity": severity,
        "status": "open",
        "published_at": parse_datetime(
            cve.get("published")
        ),
        "last_modified": parse_datetime(
            cve.get("lastModified")
        ),
        "cwes": extract_cwes(
            cve.get("weaknesses", [])
        ),
    }
