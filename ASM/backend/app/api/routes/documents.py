from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.document import Document
from app.models.user import User
from app.models.voucher import Voucher
from app.schemas.document_schema import (
    DocumentApprovalRequest,
    DocumentCreateRequest,
    DocumentLinkRequest,
    DocumentResponse,
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _build_document_ref(db: Session) -> str:
    year = datetime.utcnow().year
    total = db.query(func.count(Document.id)).scalar() or 0
    return f"RAB/TECH/{year}/{total + 1:03d}"


@router.post("/", response_model=DocumentResponse)
def create_document(payload: DocumentCreateRequest, db: Session = Depends(get_db)):
    submitted_by_id = None
    if payload.submitted_by_email:
        user = db.query(User).filter(User.email == payload.submitted_by_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Submitting user not found")
        submitted_by_id = user.id

    document = Document(
        document_ref=_build_document_ref(db),
        date=payload.date,
        name_of_staff=payload.name_of_staff,
        position=payload.position,
        division=payload.division,
        device_model=payload.device_model,
        device_serial_number=payload.device_serial_number,
        rab_asset_code=payload.rab_asset_code,
        nature_of_problem=payload.nature_of_problem,
        observation=payload.observation,
        key_recommendation=payload.key_recommendation,
        priority=payload.priority,
        approval_status="pending",
        submitted_by_id=submitted_by_id,
        voucher_id=payload.voucher_id,
        disposal_id=payload.disposal_id,
    )

    db.add(document)
    db.commit()
    db.refresh(document)
    return document


@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()


@router.patch("/{document_id}/link", response_model=DocumentResponse)
def link_document_to_voucher(document_id: int, payload: DocumentLinkRequest, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if payload.voucher_id is not None:
        voucher = db.query(Voucher).filter(Voucher.id == payload.voucher_id).first()
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")

    document.voucher_id = payload.voucher_id
    db.commit()
    db.refresh(document)
    return document


@router.patch("/{document_id}/approve", response_model=DocumentResponse)
def approve_document(document_id: int, payload: DocumentApprovalRequest, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    approver = None
    if payload.approved_by_email:
        approver = db.query(User).filter(User.email == payload.approved_by_email).first()
        if not approver:
            raise HTTPException(status_code=404, detail="Approving user not found")

        if (approver.role or "").upper() != "IT":
            raise HTTPException(status_code=403, detail="Only IT personnel can approve or reject documents")

    document.approval_status = payload.decision
    document.approved_by_id = approver.id if approver else None
    document.approved_at = datetime.utcnow()
    document.approval_note = payload.approval_note

    if payload.decision == "approved":
        document.status = "approved"
    elif payload.decision == "rejected":
        document.status = "rejected"
    else:
        document.status = "submitted"

    db.commit()
    db.refresh(document)
    return document
