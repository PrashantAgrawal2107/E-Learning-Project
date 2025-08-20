from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class ModuleContent(Base, IDMixin, TimestampMixin):
    __tablename__ = "module_contents"

    file_name = Column(String(255), nullable=False)  # original filename
    file_url = Column(Text, nullable=False)          # stored file path
    file_type = Column(String(50), nullable=True)    # pdf, video, ppt, image, etc.

    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    module = relationship("Module", back_populates="contents")
    