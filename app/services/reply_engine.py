"""
A placeholder that simulates an agent reply to a ticket.
Swap this with a real LLM or rules engine later.
"""
from dataclasses import dataclass

@dataclass
class AgentReply:
    response: str
    confidence: float

def generate_reply(subject: str, description: str) -> AgentReply:
    # Very trivial heuristic
    if "refund" in description.lower():
        text = "Thanks for reaching out. We can process your refund in 3–5 days."
        conf = 0.72
    elif "password" in description.lower():
        text = "Please reset your password via the 'Forgot Password' link. If issues persist, we can assist."
        conf = 0.69
    else:
        text = "Thanks for contacting support. We’re reviewing your request and will get back shortly."
        conf = 0.55
    return AgentReply(text, conf)
