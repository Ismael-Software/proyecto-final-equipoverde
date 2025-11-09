from models.producto_model import ProductoModel

class ProductoController:
    @staticmethod
    def agregar_producto(nombre, descripcion, categoria, precio_compra, precio_venta, 
                        stock, stock_minimo, unidad, proveedor_id):
        return ProductoModel.agregar_producto(
            nombre, descripcion, categoria, precio_compra, precio_venta,
            stock, stock_minimo, unidad, proveedor_id
        )
    
    @staticmethod
    def actualizar_producto(producto_id, nombre, descripcion, categoria, precio_compra, 
                           precio_venta, stock, stock_minimo, unidad, proveedor_id):
        return ProductoModel.actualizar_producto(
            producto_id, nombre, descripcion, categoria, precio_compra, precio_venta,
            stock, stock_minimo, unidad, proveedor_id
        )