from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Indicamos al sistema (app) de dónde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tarjetas.db"
db = SQLAlchemy(app)

class Tarjeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, nombre):
        self.nombre = nombre

class UsoTarjeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarjeta = db.Column(db.String(100), nullable=False)
    compra = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Float, nullable=False)
    cuotas = db.Column(db.Integer, nullable=False)
    pendientes = db.Column(db.Integer, nullable=False)
    monto_cuota = db.Column(db.Float, nullable=False)
    saldo = db.Column(db.Float, nullable=False)

    def __init__(self, compra, total, cuotas,tarjeta):  
        self.tarjeta = tarjeta  
        self.compra = compra
        self.total = total
        self.cuotas = cuotas
        self.pendientes = cuotas
        self.saldo = total
        self.monto_cuota = self.get_valor_cuota()

    def get_valor_cuota(self):
        if self.pendientes == -1:
            return self.total
        return round(self.total / self.cuotas, 2)
    
    def pago_cuota(self):
        if self.pendientes == -1:
            self.saldo = self.total
        elif self.pendientes > 0:
            self.pendientes -= 1
            self.saldo -= self.get_valor_cuota()

# Crear las tablas en la base de datos si no existen
with app.app_context():
    db.create_all()

@app.before_first_request
def crear_tarjetas():
    tarjetas = ['Visa Galicia', 'Visa Provincia', 'Mastercard Galicia', 'Mastercard Provincia']
    for nombre in tarjetas:
        if not Tarjeta.query.filter_by(nombre=nombre).first():
            nueva_tarjeta = Tarjeta(nombre)
            db.session.add(nueva_tarjeta)
    db.session.commit()

@app.route('/')
def index():        
    tarjetas = Tarjeta.query.all()
    compras_por_tarjeta = {}
    
    for tarjeta in tarjetas:
        compras = UsoTarjeta.query.filter_by(tarjeta=tarjeta.nombre).filter(  (UsoTarjeta.pendientes > 0) | (UsoTarjeta.pendientes == -1)).all()
        if compras:
            compras_por_tarjeta[tarjeta.nombre] = compras
    
    subtotales_mensuales = {}
    for tarjeta, compras in compras_por_tarjeta.items():
        subtotal_mensual = 0
        for compra in compras:
            if compra.cuotas == -1:
                # Si no tiene cuotas, se cuenta el total como gasto mensual
                subtotal_mensual += compra.saldo
            else:
                # Si tiene cuotas, se cuenta el monto de cada cuota
                subtotal_mensual += compra.monto_cuota
        subtotales_mensuales[tarjeta] = round(subtotal_mensual, 2)
    
    total_pagar = round(sum(
        compra.monto_cuota * compra.pendientes 
        for compras in compras_por_tarjeta.values() 
        for compra in compras
    ), 2)
    
    mensual_pagar = round(sum(compra.monto_cuota for compras in compras_por_tarjeta.values() for compra in compras), 2)

    return render_template(
        'index.html',
        compras_por_tarjeta=compras_por_tarjeta,
        mensual_pagar=mensual_pagar,
        subtotales_mensuales=subtotales_mensuales,
        total_pagar=total_pagar
    )

@app.route('/add', methods=['GET', 'POST'])
def add_compra():
    if request.method == 'POST':
        tarjeta = request.form['tarjeta']
        compra = request.form['compra']
        total = float(request.form['total'])
        cuotas = int(request.form['cuotas'])
        nueva_compra = UsoTarjeta(compra, total, cuotas,tarjeta)
        db.session.add(nueva_compra)
        db.session.commit()
        return redirect('/')
    tarjetas = Tarjeta.query.all()
    return render_template('add.html', tarjetas=tarjetas)

@app.route('/filtrar_tarjeta', methods=['GET', 'POST'])
def filtrar_tarjeta():
    
    return render_template('filtrar_tarjeta.html')

@app.route('/pagar_cuotas')
def pagar_cuotas():
    compras = UsoTarjeta.query.all()
    for compra in compras:
        compra.pago_cuota()
    db.session.commit()
    return redirect('/')

@app.route('/clean_db', methods=['POST'])
def clean_db():
    try:
        # Borrar todos los registros de la tabla UsoTarjeta
        db.session.query(UsoTarjeta).delete()
        db.session.commit()
        return redirect('/')
    except Exception as e:
        db.session.rollback()  # Revertir los cambios en caso de error
        return f"Error al vaciar la base de datos: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
