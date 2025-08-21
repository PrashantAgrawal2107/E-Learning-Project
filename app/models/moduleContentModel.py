from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base, IDMixin, TimestampMixin


class ModuleContent(Base, IDMixin, TimestampMixin):
    __tablename__ = "module_contents"

    file_name = Column(String(255), nullable=False)  
    file_url = Column(Text, nullable=False)          
    file_type = Column(String(50), nullable=True) 

    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    module = relationship("Module", back_populates="contents")
    