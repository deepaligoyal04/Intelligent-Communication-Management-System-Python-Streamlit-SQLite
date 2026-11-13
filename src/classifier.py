"""Rule-based text classification and workflow suggestions."""
import re

CATEGORY_KEYWORDS = {
    "Event-related": ["event", "seminar", "workshop", "conference", "registration", "venue", "schedule", "speaker", "invitation"],
    "Alumni communication": ["alumni", "batch", "reunion", "graduation", "alumnus", "alumna", "former student"],
    "General enquiry": ["enquiry", "inquiry", "information", "admission", "course", "eligibility", "timing", "fee", "contact"],
    "Media and publicity": ["media", "press", "publicity", "coverage", "interview", "photograph", "news", "journalist", "promotion"],
    "Technical support": ["technical", "login", "password", "website", "portal", "error", "bug", "access", "server", "software", "wifi"]
}

DEPARTMENTS = {
    "Event-related": "Events / Administration",
    "Alumni communication": "Alumni Relations Office",
    "General enquiry": "Helpdesk / Student Affairs",
    "Media and publicity": "Public Relations / Media Cell",
    "Technical support": "IT Support"
}

TEMPLATES = {
    "Event-related": "Hello {name},\\n\\nThank you for contacting us regarding {subject}. Your request has been forwarded to the Events / Administration team. They will review the details and get back to you.\\n\\nRegards,\\nEvents Team",
    "Alumni communication": "Hello {name},\\n\\nThank you for reaching out. We have shared your message regarding {subject} with the Alumni Relations Office. The team will respond with the relevant information.\\n\\nRegards,\\nAlumni Relations Team",
    "General enquiry": "Hello {name},\\n\\nThank you for your enquiry about {subject}. Your request has been received and forwarded to the concerned helpdesk. We will get back to you shortly.\\n\\nRegards,\\nHelpdesk",
    "Media and publicity": "Hello {name},\\n\\nThank you for your media request regarding {subject}. We have forwarded it to the Public Relations / Media Cell for review and coordination.\\n\\nRegards,\\nMedia Cell",
    "Technical support": "Hello {name},\\n\\nThank you for reporting the issue regarding {subject}. Your request has been routed to IT Support. If possible, please share a screenshot and the steps needed to reproduce the issue.\\n\\nRegards,\\nIT Support"
}

HIGH_TERMS = ["urgent", "immediately", "asap", "critical", "not working", "system down", "deadline today", "security issue"]
MEDIUM_TERMS = ["soon", "this week", "follow up", "problem", "issue", "requesting"]
LOW_TERMS = ["when convenient", "general information", "no rush"]

def _normalise(text):
    return re.sub(r"[^a-z0-9\s]", " ", str(text).lower())

def classify_request(subject, message):
    text = _normalise(f"{subject} {message}")
    scores = {category: sum(1 for word in words if word in text) for category, words in CATEGORY_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "General enquiry"

def detect_priority(subject, message):
    text = _normalise(f"{subject} {message}")
    if any(term in text for term in HIGH_TERMS):
        return "High"
    if any(term in text for term in MEDIUM_TERMS):
        return "Medium"
    if any(term in text for term in LOW_TERMS):
        return "Low"
    return "Medium"

def department_for(category):
    return DEPARTMENTS.get(category, "Helpdesk / Student Affairs")

def suggest_response(category, sender, subject):
    template = TEMPLATES.get(category, TEMPLATES["General enquiry"])
    return template.format(name=sender or "there", subject=subject or "your request")
