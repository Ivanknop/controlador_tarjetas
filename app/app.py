from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarjetas.db"
db = SQLAlchemy(app)

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

    def get_valor_cuota(self):
        return round(self.total / self.cuotas,2)

    def pago_cuota(self):
        if self.pendientes > 0:
            self.pendientes -= 1
            self.saldo -= self.get_valor_cuota()

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()
    
@app.route('/')
def index():        
    compras = compras = UsoTarjeta.query.filter(UsoTarjeta.pendientes > 0).all()
    saldo_total = round(sum(compra.saldo for compra in compras), 2)
    return render_template('index.html', saldo_total=saldo_total,compras=compras, page_title='Inicio')

@app.route('/add', methods=['GET', 'POST'])
def add_compra():
    if request.method == 'POST':
        compra = request.form['compra']
        total = float(request.form['total'])
        cuotas = int(request.form['cuotas'])
        nueva_compra = UsoTarjeta(compra, total, cuotas)
        db.session.add(nueva_compra)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', page_title='Nueva Compra')

@app.route('/pagar_cuotas')
def pagar_cuotas():
    compras = UsoTarjeta.query.all()
    for compra in compras:
        compra.pago_cuota()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
