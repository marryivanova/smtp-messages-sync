from sqlalchemy import MetaData, Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

metadata = MetaData()
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    metadata = metadata

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)


class Discounts(Base):
    __tablename__ = "discounts"
    metadata = metadata

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    promo_code = Column(String)
    sale_id = Column(Integer)



class Sela(Base):
    __tablename__ = "sela"
    metadata = metadata

    id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey("sale.id"))
    sale_description = Column(String)