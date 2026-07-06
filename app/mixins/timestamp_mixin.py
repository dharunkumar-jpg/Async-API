from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    """
        Adds timestamp fields to models.

        Models inheriting from this mixin automatically get:
        - created_at
        - updated_at
        """
    created_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default= func.now(),
        nullable = False)
    updated_at:Mapped[DateTime] = mapped_column(
        DateTime(timezone = True),
        server_default=func.now(),
        onupdate= func.now(),
        nullable= False)
