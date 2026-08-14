from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(255), index=True)
    ip_address: Mapped[str] = mapped_column(String(45), index=True)
    operating_system: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    environment: Mapped[str] = mapped_column(
        String(50),
        default="production",
    )
    risk_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    cve_id: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    cvss_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        default="unknown",
    )
    affected_asset: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )


class SecurityEvent(Base):
    __tablename__ = "security_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(
        String(100),
        index=True,
    )
    source: Mapped[str] = mapped_column(String(255))
    severity: Mapped[str] = mapped_column(
        String(20),
        default="low",
    )
    message: Mapped[str] = mapped_column(Text)
    source_ip: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(30),
        default="new",
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True,
    )
