from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    score: float
    level: str
    cvss_component: float
    vulnerability_component: float
    asset_component: float
    event_component: float


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(value, maximum))


def calculate_risk(
    *,
    average_cvss: float,
    critical_count: int,
    high_count: int,
    average_asset_risk: float,
    event_count: int,
) -> RiskResult:
    """
    Calculate a deterministic security score.

    Higher score = better security posture.
    """

    # CVSS 0.0 = 100 points, CVSS 10.0 = 0 points.
    cvss_component = 100.0 - (average_cvss * 10.0)
    cvss_component = clamp(cvss_component)

    # Penalize critical and high vulnerabilities.
    vulnerability_penalty = (
        critical_count * 20.0
        + high_count * 8.0
    )
    vulnerability_component = clamp(
        100.0 - vulnerability_penalty
    )

    # Asset risk is already represented as 0-100 risk.
    asset_component = clamp(
        100.0 - average_asset_risk
    )

    # Each security event costs 3 points, capped at 100.
    event_component = clamp(
        100.0 - (event_count * 3.0)
    )

    score = (
        cvss_component * 0.40
        + vulnerability_component * 0.25
        + asset_component * 0.20
        + event_component * 0.15
    )

    score = round(clamp(score), 2)

    if score >= 80:
        level = "low"
    elif score >= 60:
        level = "medium"
    elif score >= 40:
        level = "high"
    else:
        level = "critical"

    return RiskResult(
        score=score,
        level=level,
        cvss_component=round(cvss_component, 2),
        vulnerability_component=round(vulnerability_component, 2),
        asset_component=round(asset_component, 2),
        event_component=round(event_component, 2),
    )
