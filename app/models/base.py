from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, func

Base = declarative_base()

# Mixin for ID field
class IDMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    
# Mixin for timestamps
class TimestampMixin:
    created_on = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()  # Set only at creation
    )
    updated_on = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()  # Auto-update when row changes
    )