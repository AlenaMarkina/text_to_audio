from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from db.sqlite import get_session

Session = Annotated[Session, Depends(get_session)]
