from typing import Optional, Any
from pydantic import BaseModel


class Problem(BaseModel):

    title: str
    status: int
    detail: Any
    type: Optional[str] = None
    instance: Optional[str] = None

    def dict(self, *args, **kwargs):
        kwargs.pop("exclude_unset")
        return super().dict(*args, exclude_unset=True, **kwargs)
