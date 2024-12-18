from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime

Base = declarative_base()
class ModelBTC(Base):
    __tablename__ = 'btc_precos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    criptomoeda = Column(String(50), nullable=False)
    moeda = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)