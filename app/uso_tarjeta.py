from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UsoTarjeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compra = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    cuotas = db.Column(db.Integer, nullable=False)
    pendientes = db.Column(db.Integer, nullable=False)
    saldo = db.Column(db.Float, nullable=False)
    
    def __init__(self, compra, total, cuotas):
        self.compra = compra
        self.total = total
        self.cuotas = cuotas
        self.pendientes = cuotas
        self.saldo = total
    
    def get_compra(self):
        return self.compra
    def get_total(self):
        return self.total
    def get_cuotas(self):
        return self.cuotas
    def get_pendientes(self):
        return self.pendientes
    def get_saldo(self):
        return self.saldo
    def get_valor_cuota(self):
        return self.total / self.cuotas
            
    def pago_cuota(self):
        if self.pendientes >= 1:
            self.pendientes -=1
            self.saldo -= self.get_valor_cuota()