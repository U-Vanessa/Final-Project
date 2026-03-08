from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.session import Base


class Document(Base):
	__tablename__ = "documents"

	id = Column(Integer, primary_key=True, index=True)
	document_ref = Column(String, unique=True, index=True, nullable=False)

	date = Column(String, nullable=False)
	name_of_staff = Column(String, nullable=False)
	position = Column(String, nullable=False)
	division = Column(String, nullable=False)

	device_model = Column(String, nullable=False)
	device_serial_number = Column(String, nullable=False)
	rab_asset_code = Column(String, nullable=True)

	nature_of_problem = Column(Text, nullable=False)
	observation = Column(Text, nullable=True)
	key_recommendation = Column(Text, nullable=True)

	priority = Column(String, default="medium", nullable=False)
	status = Column(String, default="submitted", nullable=False)
	approval_status = Column(String, default="pending", nullable=False, index=True)
	approved_by_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
	approved_at = Column(DateTime, nullable=True)
	approval_note = Column(Text, nullable=True)

	submitted_by_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
	voucher_id = Column(Integer, ForeignKey("vouchers.id"), nullable=True, index=True)
	disposal_id = Column(Integer, nullable=True, index=True)

	created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
