from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.document import Document
from app.models.notification import TicketNotification
from app.models.sla_config import SLAConfig
from app.models.voucher import Voucher
from app.schemas.chatbot_schema import ChatbotAskRequest, ChatbotAskResponse

router = APIRouter()


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
	normalized = question.lower()

	if any(word in normalized for word in ["hello", "hi", "hey"]):
		return ChatbotAskResponse(
			reply=(
				"Hello! I can help with ticket status, recent documents, and report summaries. "
				"Try: 'ticket summary', 'unread alerts', or 'recent documents'."
			),
			intent="greeting",
		)

	if any(word in normalized for word in ["ticket", "voucher", "summary", "report"]):
		total = db.query(func.count(Voucher.id)).scalar() or 0
		open_count = db.query(func.count(Voucher.id)).filter(Voucher.status == "open").scalar() or 0
		assigned_count = db.query(func.count(Voucher.id)).filter(Voucher.status == "assigned").scalar() or 0
		in_progress_count = db.query(func.count(Voucher.id)).filter(Voucher.status == "in_progress").scalar() or 0
		resolved_count = db.query(func.count(Voucher.id)).filter(Voucher.status == "resolved").scalar() or 0
		closed_count = db.query(func.count(Voucher.id)).filter(Voucher.status == "closed").scalar() or 0

		urgent_tickets = (
			db.query(Voucher)
			.filter(Voucher.status.in_(["open", "assigned", "in_progress"]))
			.order_by(Voucher.priority.desc(), Voucher.created_at.asc())
			.limit(5)
			.all()
		)

		urgent_text = ", ".join(format_ticket_line(item) for item in urgent_tickets) if urgent_tickets else "None"

		return ChatbotAskResponse(
			reply=(
				f"Ticket summary: total={total}, open={open_count}, assigned={assigned_count}, "
				f"in_progress={in_progress_count}, resolved={resolved_count}, closed={closed_count}. "
				f"Priority queue: {urgent_text}."
			),
			intent="ticket_summary",
			context={
				"total": total,
				"open": open_count,
				"assigned": assigned_count,
				"in_progress": in_progress_count,
				"resolved": resolved_count,
				"closed": closed_count,
			},
		)

	if any(word in normalized for word in ["document", "docs", "files"]):
		recent_documents = db.query(Document).order_by(Document.created_at.desc()).limit(5).all()
		if not recent_documents:
			return ChatbotAskResponse(
				reply="No documents found yet. You can submit documents from the Document page.",
				intent="documents",
				context={"count": 0},
			)

		items = [f"{doc.document_ref} ({doc.name_of_staff})" for doc in recent_documents]
		return ChatbotAskResponse(
			reply=f"Recent documents: {', '.join(items)}.",
			intent="documents",
			context={"count": len(recent_documents)},
		)

	if any(word in normalized for word in ["sla", "alert", "escalation", "notification"]):
		unread_alerts = (
			db.query(TicketNotification)
			.filter(TicketNotification.is_read.is_(False))
			.order_by(TicketNotification.created_at.desc())
			.limit(5)
			.all()
		)
		config = db.query(SLAConfig).first()

		if not unread_alerts:
			config_text = "SLA config not set" if not config else (
				f"low={config.low_hours}h, medium={config.medium_hours}h, high={config.high_hours}h, critical={config.critical_hours}h"
			)
			return ChatbotAskResponse(
				reply=f"No unread SLA alerts right now. Current thresholds: {config_text}.",
				intent="sla",
				context={"unread_alerts": 0},
			)

		alert_lines = [
			f"Ticket #{item.voucher_id}: {item.category} ({item.severity})"
			for item in unread_alerts
		]
		return ChatbotAskResponse(
			reply=f"Unread SLA alerts ({len(unread_alerts)}): {'; '.join(alert_lines)}.",
			intent="sla",
			context={"unread_alerts": len(unread_alerts)},
		)

	if any(word in normalized for word in ["help", "what can you do", "commands"]):
		return ChatbotAskResponse(
			reply=(
				"I can answer: ticket summary, unread alerts, recent documents, and reporting status. "
				"Examples: 'show ticket summary', 'any unread alerts?', 'recent documents'."
			),
			intent="help",
		)

	now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
	return ChatbotAskResponse(
		reply=(
			"I couldn't fully match that request yet. Try asking about 'ticket summary', 'unread alerts', "
			f"or 'recent documents'. (Checked at {now})"
		),
		intent="fallback",
	)
