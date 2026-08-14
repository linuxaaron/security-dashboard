from app.services.risk_engine import calculate_risk


def test_low_risk_environment():
    result = calculate_risk(
        average_cvss=1.0,
        critical_count=0,
        high_count=0,
        average_asset_risk=5.0,
        event_count=0,
    )

    assert result.score >= 80
    assert result.level == "low"


def test_critical_vulnerability_reduces_score():
    result = calculate_risk(
        average_cvss=9.8,
        critical_count=1,
        high_count=0,
        average_asset_risk=50.0,
        event_count=5,
    )

    assert result.score < 60
    assert result.level in {"high", "critical"}


def test_score_is_bounded():
    result = calculate_risk(
        average_cvss=10.0,
        critical_count=100,
        high_count=100,
        average_asset_risk=100.0,
        event_count=100,
    )

    assert 0 <= result.score <= 100
