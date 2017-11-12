import datetime
from sqlalchemy import Column, Integer, DateTime, String, Float, Boolean
from app import Base


class Sorteio(Base):
    __tablename__ = 'sorteio'
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, nullable=False)
    acumulado = Column(Boolean, nullable=False)
    valor_acumulado = Column(Float)
    ganhadores_mega = Column(Integer)
    valor_mega = Column(Float)
    ganhadores_quina = Column(Integer)
    valor_quina = Column(Float)
    ganhadores_quadra = Column(Integer)
    valor_quadra = Column(Float)
    sequencia = Column(String, nullable=False)

    @property
    def lst_numeros(self):
        return self.sequencia.split(",")

    def str_bool(self, bool_str):
        return True if bool_str == "sim" else False

    def __init__(self, *args, **kwargs):
        self.id = int(kwargs.get("numero")) if kwargs.get("numero") else None
        self.data = datetime.datetime.strptime(kwargs.get("data"), "%Y-%m-%d").date() if kwargs.get('data') else None
        self.acumulado = self.str_bool(kwargs.get("acumulado")) if kwargs.get('acumulado') else False
        self.valor_acumulado = float(kwargs.get("valor_acumulado")) if kwargs.get("valor_acumulado") and float(kwargs.get("valor_acumulado")) > 0 else 0
        self.ganhadores_mega = int(kwargs.get("ganhadores")[0]) if kwargs.get("ganhadores") and kwargs.get("ganhadores")[0] else 0
        self.ganhadores_quina = int(kwargs.get("ganhadores")[1]) if kwargs.get("ganhadores") and kwargs.get("ganhadores")[1] else 0
        self.ganhadores_quadra = int(kwargs.get("ganhadores")[2]) if kwargs.get("ganhadores") and kwargs.get("ganhadores")[2] else 0
        self.valor_mega = int(kwargs.get("rateio")[0]) if kwargs.get("rateio") and kwargs.get("rateio")[0] else 0
        self.valor_quina = int(kwargs.get("rateio")[1]) if kwargs.get("rateio") and kwargs.get("rateio")[1] else 0
        self.valor_quadra = int(kwargs.get("rateio")[2]) if kwargs.get("rateio") and kwargs.get("rateio")[2] else 0
        self.sequencia = kwargs.get("sorteio").__str__().replace("[", "").replace("]", "")[0:-1] if kwargs.get('sorteio') else False



