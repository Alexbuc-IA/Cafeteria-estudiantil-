class ConjuntoPersonalizado:
    def __init__(self, elementos=None):
        self.elementos = set(elementos) if elementos else set()
    
    def agregar(self, elemento):
        self.elementos.add(elemento)
        return True
    
    def eliminar(self, elemento):
        if elemento in self.elementos:
            self.elementos.remove(elemento)
            return True
        return False
    
    def contiene(self, elemento):
        return elemento in self.elementos
    
    def union(self, otro_conjunto):
        if isinstance(otro_conjunto, ConjuntoPersonalizado):
            return ConjuntoPersonalizado(self.elementos | otro_conjunto.elementos)
        return ConjuntoPersonalizado(self.elementos | set(otro_conjunto))
    
    def interseccion(self, otro_conjunto):
        if isinstance(otro_conjunto, ConjuntoPersonalizado):
            return ConjuntoPersonalizado(self.elementos & otro_conjunto.elementos)
        return ConjuntoPersonalizado(self.elementos & set(otro_conjunto))
    
    def diferencia(self, otro_conjunto):
        if isinstance(otro_conjunto, ConjuntoPersonalizado):
            return ConjuntoPersonalizado(self.elementos - otro_conjunto.elementos)
        return ConjuntoPersonalizado(self.elementos - set(otro_conjunto))
    
    def obtener_lista(self):
        return list(self.elementos)
    
    def tamanio(self):
        return len(self.elementos)
    
    def esta_vacio(self):
        return len(self.elementos) == 0
    
    def limpiar(self):
        self.elementos.clear()
    
    def __len__(self):
        return len(self.elementos)
    
    def __str__(self):
        if self.esta_vacio():
            return "Conjunto(vacío)"
        elementos_str = ', '.join(str(e) for e in list(self.elementos)[:5])
        if len(self.elementos) > 5:
            elementos_str += f", ... (+{len(self.elementos) - 5} más)"
        return f"Conjunto({{{elementos_str}}})"
    
    def __iter__(self):
        return iter(self.elementos)