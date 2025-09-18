from sqlalchemy import Column, String, Text, Enum
import enum

from app.db.database import Base

class JobStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    batch_id = Column(String, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    filename = Column(String, nullable=True)
    result = Column(Text, nullable=True)