from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key = True, index = True)
    subject = Column(String(200), nullable = False)
    description = Column(Text, nullable = False)
    requester_email = Column(String(200), nullable = False, index = True)
    status = Column(String(20), default = "open", index = True)  # open|pending|solved
    priority = Column(String(20), default = "normal")            # low|normal|high|urgent
    created_at = Column(DateTime(timezone=True), server_default = func.now())
    updated_at = Column(DateTime(timezone=True), onupdate = func.now())
