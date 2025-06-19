from sqlalchemy import Column, Integer, String, Text, BigInteger, Boolean, Float, Enum, DateTime
from sqlalchemy.sql import func
from config.config import Base

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    upload_path = Column(String(500), nullable=False)
    image_count = Column(Integer, default=0)
    file_size = Column(BigInteger, default=0)
    upload_type = Column(String(50), default='images')
    has_labels = Column(Boolean, default=False)
    labeling_method = Column(String(50), default='auto')
    labeling_accuracy = Column(Float, default=0.0)
    status = Column(String(50), default='uploaded')
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'upload_path': self.upload_path,
            'image_count': self.image_count,
            'file_size': self.file_size,
            'upload_type': self.upload_type,
            'has_labels': self.has_labels,
            'labeling_method': self.labeling_method,
            'labeling_accuracy': self.labeling_accuracy,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
