from sqlalchemy.orm import Session
from app.db.session import SessionLocal, Base, engine
from app.models.ticket import Ticket

def seed():
    Base.metadata.create_all(bind = engine)
    db: Session = SessionLocal()
    try:
        if not db.query(Ticket).count():
            db.add_all([
                Ticket(subject = "Refund request", description = "Please refund my order #1234", requester_email = "a@example.com"),
                Ticket(subject = "Password reset", description = "I cannot log in; password reset fails", requester_email = "b@example.com"),
            ])
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
