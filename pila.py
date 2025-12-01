class Pila:
    def __init__(self, capacidad_maxima=None):
        self.items = []
        self.capacidad_maxima = capacidad_maxima
    
    def apilar(self, item):
        if self.capacidad_maxima and len(self.items) >= self.capacidad_maxima:
            self.items.pop(0)
        self.items.append(item)
        return True
    
    def desapilar(self):
        if self.esta_vacia():
            return None
        return self.items.pop()
    
    def ver_tope(self):
        if self.esta_vacia():
            return None
        return self.items[-1]
    
    def ver_todos(self):
        return list(reversed(self.items))
    
    def buscar(self, criterio):
        return [item for item in self.items if criterio(item)]
    
    def esta_vacia(self):
        return len(self.items) == 0
    
    def tamanio(self):
        return len(self.items)
    
    def limpiar(self):
        self.items.clear()
    
    def __len__(self):
        return len(self.items)
    
    def __str__(self):
        if self.esta_vacia():
            return "Pila(vacía)"
        preview = str(self.items[-1])[:30] if self.items else ""
        return f"Pila({len(self)} elementos, tope: {preview}...)"
    
    def __iter__(self):
        return reversed(self.items)