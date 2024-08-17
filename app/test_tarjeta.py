import unittest
from uso_tarjeta import Uso_tarjeta

class TestJerta(unittest.TestCase):
    def test_getters(self):
        tarjeta = []
        primera_compra = Uso_tarjeta ('Celular', 100000,10)
        segunda_compra = Uso_tarjeta ('Juguete', 36000,6)
        tercera_compra = Uso_tarjeta ('Televisor', 1000000,20)
        tarjeta.append(primera_compra)
        tarjeta.append(segunda_compra)
        tarjeta.append(tercera_compra)
        for i in tarjeta:
            i.pago_cuota()        
        self.assertEqual(primera_compra.get_pendientes(), 9)
        self.assertEqual(primera_compra.get_saldo(), 90000)
        self.assertEqual(segunda_compra.get_pendientes(), 5)
        self.assertEqual(segunda_compra.get_saldo(), 30000)
        self.assertEqual(tercera_compra.get_pendientes(), 19)
        self.assertEqual(tercera_compra.get_saldo(), 950000)
        for i in range(0,5):
            for i in tarjeta:
                i.pago_cuota()
        self.assertEqual(primera_compra.get_pendientes(), 4)
        self.assertEqual(primera_compra.get_saldo(), 40000)
        self.assertEqual(segunda_compra.get_pendientes(), 0)
        self.assertEqual(segunda_compra.get_saldo(), 0)
        self.assertEqual(tercera_compra.get_pendientes(), 14)
        self.assertEqual(tercera_compra.get_saldo(), 700000)
        for i in tarjeta:
            i.pago_cuota()   
        self.assertEqual(primera_compra.get_pendientes(), 3)
        self.assertEqual(primera_compra.get_saldo(), 30000)
        self.assertEqual(segunda_compra.get_pendientes(), 0)
        self.assertEqual(segunda_compra.get_saldo(), 0)
        self.assertEqual(tercera_compra.get_pendientes(), 13)
        self.assertEqual(tercera_compra.get_saldo(), 650000)
        
if __name__ == '__main__':
    unittest.main()