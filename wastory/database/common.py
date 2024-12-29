from typing import Annotated
from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

intpk = Annotated[int, mapped_column(BigInteger, primary_key=True)]