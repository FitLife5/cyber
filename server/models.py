from datetime import datetime, timezone
from decimal import Decimal
import enum
from sqlalchemy import String, Text, Integer, Numeric, DateTime, ForeignKey, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="analyst", nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    incidents: Mapped[list["Incident"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    playbooks: Mapped[list["Playbook"]] = relationship(back_populates="author")


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    threat_level: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="incidents")
    messages: Mapped[list["AnalysisMessage"]] = relationship(back_populates="incident", cascade="all, delete-orphan")


class AnalysisMessage(Base):
    __tablename__ = "analysis_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole, name="message_role_enum"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    incident: Mapped["Incident"] = relationship(back_populates="messages")
    llm_call: Mapped["LlmCallLog | None"] = relationship(back_populates="message", uselist=False)
    playbook_links: Mapped[list["IncidentPlaybook"]] = relationship(back_populates="message", cascade="all, delete-orphan")


class LlmCallLog(Base):
    __tablename__ = "llm_call_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    message_id: Mapped[int] = mapped_column(
        ForeignKey("analysis_messages.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    input_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    output_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_usd: Mapped[Decimal] = mapped_column(Numeric(12, 6), default=Decimal("0.000000"), nullable=False)

    message: Mapped["AnalysisMessage"] = relationship(back_populates="llm_call")


class Playbook(Base):
    __tablename__ = "playbooks"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    qdrant_point_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )

    author: Mapped["User | None"] = relationship(back_populates="playbooks")
    message_links: Mapped[list["IncidentPlaybook"]] = relationship(back_populates="playbook")


class IncidentPlaybook(Base):
    __tablename__ = "incident_playbooks"

    message_id: Mapped[int] = mapped_column(ForeignKey("analysis_messages.id", ondelete="CASCADE"), primary_key=True)
    playbook_id: Mapped[int] = mapped_column(ForeignKey("playbooks.id", ondelete="CASCADE"), primary_key=True)
    similarity_score: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)

    message: Mapped["AnalysisMessage"] = relationship(back_populates="playbook_links")
    playbook: Mapped["Playbook"] = relationship(back_populates="message_links")