import heapq


class ColaPrioridad:
    def __init__(self):
        self.heap = []
        self.contador = 0
        self._id_map = {}
    
    def agregar(self, prioridad, pedido, pedido_id=None):
        if pedido_id is None:
            pedido_id = f"P{self.contador}"
        
        entrada = [prioridad, self.contador, pedido_id, pedido]
        heapq.heappush(self.heap, entrada)
        self._id_map[pedido_id] = entrada
        self.contador += 1
        
        return pedido_id
    
    def atender_siguiente(self):
        if self.esta_vacia():
            return None
        
        prioridad, _, pedido_id, pedido = heapq.heappop(self.heap)
        self._id_map.pop(pedido_id, None)
        
        return {
            'prioridad': prioridad,
            'id': pedido_id,
            'pedido': pedido
        }
    
    def ver_siguiente(self):
        if self.esta_vacia():
            return None
        
        prioridad, _, pedido_id, pedido = self.heap[0]
        return {
            'prioridad': prioridad,
            'id': pedido_id,
            'pedido': pedido
        }
    
    def buscar_por_id(self, pedido_id):
        entrada = self._id_map.get(pedido_id)
        if entrada:
            return {
                'prioridad': entrada[0],
                'id': entrada[2],
                'pedido': entrada[3]
            }
        return None
    
    def esta_vacia(self):
        return len(self.heap) == 0
    
    def tamanio(self):
        return len(self.heap)
    
    def ver_todos(self):
        return [
            {
                'prioridad': p,
                'id': pid,
                'pedido': pedido
            }
            for p, _, pid, pedido in sorted(self.heap)
        ]
    
    def limpiar(self):
        self.heap.clear()
        self._id_map.clear()
        self.contador = 0
    
    def __len__(self):
        return len(self.heap)
    
    def __str__(self):
        return f"ColaPrioridad({len(self.heap)} pedidos)"