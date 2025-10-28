from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db, Base, engine
from app.models.ticket import Ticket
from app.schemas.tickets import TicketCreate, TicketUpdate, TicketOut
from app.schemas.common import Message
from app.services.reply_engine import generate_reply
from app.utils.ids import new_job_id

# Ensure tables exist on import (simple dev approach)
Base.metadata.create_all(bind = engine)

router = APIRouter(prefix = "/tickets", tags = ["tickets"])

@router.post("/", response_model = TicketOut)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db)):
    ticket = Ticket(
        subject = payload.subject,
        description = payload.description,
        requester_email = payload.requester_email,
        priority = payload.priority or "normal"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.get("/", response_model = List[TicketOut])
def list_tickets(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Ticket)
    if status:
        q = q.filter(Ticket.status == status)
    return q.order_by(Ticket.id.desc()).all()

@router.get("/{ticket_id}", response_model = TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    return ticket

@router.patch("/{ticket_id}", response_model = TicketOut)
def update_ticket(ticket_id: int, payload: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")

    for field, value in payload.model_dump(exclude_unset = True).items():
        setattr(ticket, field, value)

    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

@router.post("/{ticket_id}/auto-reply", response_model = Message)
def auto_reply(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")

    job_id = new_job_id()
    agent = generate_reply(ticket.subject, ticket.description)
    # In a real integration, you would POST this back to Zendesk as a comment.
    return Message(message = f"[job_id={job_id}] {agent.response} (confidence={agent.confidence:.2f})")
