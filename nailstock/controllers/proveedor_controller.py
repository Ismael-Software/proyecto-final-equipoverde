from models.proveedor_model import ProveedorModel

class ProveedorController:
    @staticmethod
    def agregar_proveedor(nombre, telefono, direccion, correo, rfc, observaciones):
        return ProveedorModel.agregar_proveedor(
            nombre.strip(),
            telefono.strip() if telefono else None,
            direccion.strip() if direccion else None,
            correo.strip() if correo else None,
            rfc.strip() if rfc else None,
            observaciones.strip() if observaciones else None
        )
    
    @staticmethod
    def actualizar_proveedor(proveedor_id, nombre, telefono, direccion, correo, rfc, observaciones):   
        return ProveedorModel.actualizar_proveedor(
            proveedor_id,
            nombre.strip(),
            telefono.strip() if telefono else None,
            direccion.strip() if direccion else None,
            correo.strip() if correo else None,
            rfc.strip() if rfc else None,
            observaciones.strip() if observaciones else None
        )
    
    @staticmethod
    def buscar_proveedores(termino):
        proveedores = ProveedorModel.obtener_proveedores()
        if not termino:
            return proveedores
        
        termino_lower = termino.lower()
        resultados = []
        for proveedor in proveedores:
            if (termino_lower in proveedor[1].lower() or  # nombre
                (proveedor[2] and termino_lower in proveedor[2].lower()) or  # telefono
                (proveedor[4] and termino_lower in proveedor[4].lower()) or  # correo
                (proveedor[5] and termino_lower in proveedor[5].lower())):   # rfc
                resultados.append(proveedor)
        
        return resultados