from models.venta_model import VentaModel

class VentaController:    
    @staticmethod
    def registrar_venta(cliente_id, usuario_id, productos):
        return VentaModel.agregar_venta(cliente_id, usuario_id, productos)
    
    @staticmethod
    def calcular_total(productos):
        return sum(item['cantidad'] * item['precio_unitario'] for item in productos)