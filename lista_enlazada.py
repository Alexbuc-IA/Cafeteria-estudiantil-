class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
    
    def esta_vacia(self):
        return self.cabeza is None
    
    def agregar_al_inicio(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        self.tamano += 1
        return True
    
    def agregar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamano += 1
        return True
    
    def eliminar_primero(self):
        if self.esta_vacia():
            return None
        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        self.tamano -= 1
        return dato
    
    def buscar(self, criterio):
        resultados = []
        actual = self.cabeza
        while actual:
            try:
                if criterio(actual.dato):
                    resultados.append(actual.dato)
            except:
                pass
            actual = actual.siguiente
        return resultados
    
    def obtener_en_posicion(self, indice):
        if indice < 0 or indice >= self.tamano:
            return None
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato
    
    def obtener_todos(self):
        elementos = []
        actual = self.cabeza
        while actual:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos
    
    def obtener_ultimos_n(self, n):
        todos = self.obtener_todos()
        return todos[:n] if len(todos) >= n else todos
    
    def limpiar(self):
        self.cabeza = None
        self.cola = None
        self.tamano = 0
    
    def __len__(self):
        return self.tamano
    
    def __iter__(self):
        actual = self.cabeza
        while actual:
            yield actual.dato
            actual = actual.siguiente