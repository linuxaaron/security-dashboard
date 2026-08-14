from app.services.risk_engine import calculate_risk
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.security import Asset, SecurityEvent, Vulnerability

router = APIRouter()



@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return db.scalars(
        select(Asset).order_by(Asset.id.desc())
    ).all()


@router.post(
    "/assets",
    status_code=status.HTTP_201_CREATED,
)
def create_asset(
    payload: dict,
    db: Session = Depends(get_db),
):
    asset = Asset(
        hostname=payload["hostname"],
        ip_address=payload["ip_address"],
        operating_system=payload.get("operating_system"),
        environment=payload.get("environment", "production"),
        risk_score=payload.get("risk_score", 0.0),
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


@router.get("/vulnerabilities")
def list_vulnerabilities(db: Session = Depends(get_db)):
    return db.scalars(
        select(Vulnerability).order_by(Vulnerability.id.desc())
    ).all()


@router.post(
    "/vulnerabilities",
    status_code=status.HTTP_201_CREATED,
)
def create_vulnerability(
    payload: dict,
    db: Session = Depends(get_db),
):
    existing = db.scalar(
        select(Vulnerability).where(
            Vulnerability.cve_id == payload["cve_id"]
        )
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="CVE already exists",
        )

    vulnerability = Vulnerability(**payload)

    db.add(vulnerability)
    db.commit()
    db.refresh(vulnerability)

    return vulnerability


@router.get("/events")
def list_events(db: Session = Depends(get_db)):
    return db.scalars(
        select(SecurityEvent).order_by(
            SecurityEvent.timestamp.desc()
        )
    ).all()


@router.post(
    "/events",
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    payload: dict,
    db: Session = Depends(get_db),
):
    event = SecurityEvent(**payload)

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    assets = db.scalars(select(Asset)).all()
    vulnerabilities = db.scalars(
        select(Vulnerability)
    ).all()
    events = db.scalars(
        select(SecurityEvent)
    ).all()

    asset_count = len(assets)
    vulnerability_count = len(vulnerabilities)

    critical_count = sum(
        1
        for vulnerability in vulnerabilities
        if vulnerability.severity.lower() == "critical"
    )

    high_count = sum(
        1
        for vulnerability in vulnerabilities
        if vulnerability.severity.lower() == "high"
    )

    cvss_values = [
        vulnerability.cvss_score
        for vulnerability in vulnerabilities
        if vulnerability.cvss_score is not None
    ]

    average_cvss = (
        sum(cvss_values) / len(cvss_values)
        if cvss_values
        else 0.0
    )

    average_asset_risk = (
        sum(asset.risk_score for asset in assets) / asset_count
        if asset_count
        else 0.0
    )

    risk = calculate_risk(
        average_cvss=average_cvss,
        critical_count=critical_count,
        high_count=high_count,
        average_asset_risk=average_asset_risk,
        event_count=len(events),
    )

    return {
        "security_score": risk.score,
        "risk_level": risk.level,
        "assets": asset_count,
        "vulnerabilities": vulnerability_count,
        "critical_vulnerabilities": critical_count,
        "high_vulnerabilities": high_count,
        "security_events": len(events),
        "risk_components": {
            "cvss": risk.cvss_component,
            "vulnerabilities": risk.vulnerability_component,
            "assets": risk.asset_component,
            "events": risk.event_component,
        },
    }

@router.post(
    "/vulnerabilities/import/{cve_id}",
    status_code=status.HTTP_201_CREATED,
)
def import_cve(
    cve_id: str,
    db: Session = Depends(get_db),
):
    from app.services.cve_parser import normalize_cve
    from app.services.nvd import NVDService

    cve_id = cve_id.strip().upper()

    existing = db.scalar(
        select(Vulnerability).where(
            Vulnerability.cve_id == cve_id
        )
    )

    if existing:
        return {
            "status": "already_exists",
            "cve": existing,
        }

    cve = NVDService().get_cve(cve_id)

    if cve is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CVE not found: {cve_id}",
        )

    normalized = normalize_cve(cve)

    vulnerability = Vulnerability(
        cve_id=normalized["cve_id"],
        title=normalized["title"],
        description=normalized["description"],
        cvss_score=normalized["cvss_score"],
        severity=normalized["severity"],
        status=normalized["status"],
        published_at=normalized["published_at"],
    )

    db.add(vulnerability)
    db.commit()
    db.refresh(vulnerability)

    return {
        "status": "imported",
        "cve": vulnerability,
        "cwes": normalized["cwes"],
    }
