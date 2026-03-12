from datetime import datetime
import logging

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.document import Document
from app.models.notification import TicketNotification
from app.models.sla_config import SLAConfig
from app.models.voucher import Voucher
from app.schemas.chatbot_schema import ChatbotAskRequest, ChatbotAskResponse
from app.services.openai_service import openai_service

router = APIRouter()
logger = logging.getLogger(__name__)

# System prompt for OpenAI assistant
SYSTEM_PROMPT = """You are a helpful AI assistant for the Asset Management System (ASM). 
You help users with questions about IT asset management, ticketing workflows, document management, 
and SLA compliance. 

Key features of ASM:
- Ticket/Voucher management with statuses: open, assigned, in_progress, resolved, closed
- Priority levels: low, medium, high, critical
- Document submission and tracking
- SLA monitoring and alerts
- User roles: IT, User, Admin, Manager

Be concise, professional, and helpful. If you don't know something specific about the system, 
suggest that the user check with their IT administrator or refer to system documentation.
"""


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def format_ticket_line(ticket: Voucher) -> str:
	return f"{ticket.ticket_number} ({ticket.priority}, {ticket.status})"


@router.post("/ask", response_model=ChatbotAskResponse)
def ask_chatbot(payload: ChatbotAskRequest, db: Session = Depends(get_db)):
	question = payload.message.strip()
	if not question:
		return ChatbotAskResponse(
			reply="Please type a question so I can help.",
			intent="empty_question",
		)

	normalized = question.lower()


	# Try OpenAI for general questions
	openai_status = openai_service.status()
	if openai_status["available"]:
		ai_response = openai_service.get_chat_response(
			user_message=question,
			system_prompt=SYSTEM_PROMPT,
			max_tokens=500,
			temperature=0.7,
		)

		if ai_response:
			return ChatbotAskResponse(
				reply=ai_response,
				intent="ai_response",
				context={"openai_model": openai_status["model"]},
			)

		logger.warning("OpenAI call returned no response; using fallback")
	else:
		logger.info("OpenAI unavailable (%s); using fallback", openai_status["reason"])

	# Fallback if OpenAI not available or failed
	openai_status = openai_service.status()
	now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
	return ChatbotAskResponse(
		reply=(
			"I couldn't fully match that request yet. Try asking about 'ticket summary', 'unread alerts', "
			f"or 'recent documents'. (Checked at {now})"
		),
		intent="fallback",
		context={
			"openai_available": openai_status["available"],
			"openai_reason": openai_status["reason"],
			"openai_model": openai_status["model"],
			"openai_last_error": openai_status.get("last_error", ""),
		},
	)


@router.get("/health")
def chatbot_health():
	"""Health info used during deployment checks."""
	return {
		"service": "chatbot",
		"status": "ok",
		"openai": openai_service.status(),
	}
