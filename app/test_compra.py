import unittest
from uso_tarjeta import Uso_tarjeta

class TestJerta(unittest.TestCase):
    def test_getters(self):
        primera_compra = Uso_tarjeta ('Celular', 100000,10)
        self.assertEqual(primera_compra.get_compra(),'Celular')
        self.assertEqual(primera_compra.get_total(), 100000)
        self.assertEqual(primera_compra.get_cuotas(), 10)
        self.assertEqual(primera_compra.get_pendientes(), 10)
        self.assertEqual(primera_compra.get_saldo(), 100000)
        self.assertEqual(primera_compra.get_valor_cuota(), 10000)
    
    def test_pago_una_cuota(self):
        primera_compra = Uso_tarjeta ('Celular', 100000,10)
        primera_compra.pago_cuota()
        self.assertEqual(primera_compra.get_compra(),'Celular')
        self.assertEqual(primera_compra.get_total(), 100000)
        self.assertEqual(primera_compra.get_cuotas(), 10)
        self.assertEqual(primera_compra.get_pendientes(), 9)
        self.assertEqual(primera_compra.get_saldo(), 90000)
    def test_pago_seis_cuotas(self):
        primera_compra = Uso_tarjeta ('Celular', 100000,10)
        for i in range(0,6):
            primera_compra.pago_cuota()
        self.assertEqual(primera_compra.get_compra(),'Celular')
        self.assertEqual(primera_compra.get_total(), 100000)
        self.assertEqual(primera_compra.get_cuotas(), 10)
        self.assertEqual(primera_compra.get_pendientes(), 4)
        self.assertEqual(primera_compra.get_saldo(), 40000)
        
if __name__ == '__main__':
    unittest.main()