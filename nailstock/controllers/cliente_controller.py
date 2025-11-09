from models.cliente_model import ClienteModel

class ClienteController:
    @staticmethod
    def agregar_cliente(nombre, telefono, direccion, rfc):
        return ClienteModel.agregar_cliente(
            nombre.strip() if nombre else None,
            telefono.strip() if telefono else None,
            direccion.strip() if direccion else None,
            rfc.strip() if rfc else None
        )
    
    @staticmethod
    def actualizar_cliente(cliente_id, nombre, telefono, direccion, rfc):        
        return ClienteModel.actualizar_cliente(
            cliente_id,
            nombre.strip() if nombre else None,
            telefono.strip() if telefono else None,
            direccion.strip() if direccion else None,
            rfc.strip() if rfc else None
        )
    
    @staticmethod
    def buscar_clientes(termino):
        clientes = ClienteModel.obtener_clientes()
        if not termino:
            return clientes
        
        termino_lower = termino.lower()
        resultados = []
        for cliente in clientes:
            if ((cliente[1] and termino_lower in cliente[1].lower()) or  # nombre
                (cliente[2] and termino_lower in cliente[2].lower()) or  # telefonom
                (cliente[4] and termino_lower in cliente[4].lower())):   # rfc
                resultados.append(cliente)
        
        return resultados