class NodoBST:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class ArbolBST:
    def __init__(self):
        self.raiz = None
        self.tamano = 0
    
    def insertar(self, clave, valor):
        if self.raiz is None:
            self.raiz = NodoBST(clave, valor)
            self.tamano += 1
        else:
            self._insertar_recursivo(self.raiz, clave, valor)
    
    def _insertar_recursivo(self, nodo, clave, valor):
        if clave < nodo.clave:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(clave, valor)
                self.tamano += 1
            else:
                self._insertar_recursivo(nodo.izquierdo, clave, valor)
        elif clave > nodo.clave:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(clave, valor)
                self.tamano += 1
            else:
                self._insertar_recursivo(nodo.derecho, clave, valor)
        else:
            nodo.valor = valor
    
    def buscar(self, clave):
        return self._buscar_recursivo(self.raiz, clave)
    
    def _buscar_recursivo(self, nodo, clave):
        if nodo is None:
            return None
        if clave == nodo.clave:
            return nodo.valor
        elif clave < nodo.clave:
            return self._buscar_recursivo(nodo.izquierdo, clave)
        else:
            return self._buscar_recursivo(nodo.derecho, clave)
    
    def buscar_rango(self, min_clave, max_clave):
        resultados = []
        self._buscar_rango_recursivo(self.raiz, min_clave, max_clave, resultados)
        return resultados
    
    def _buscar_rango_recursivo(self, nodo, min_clave, max_clave, resultados):
        if nodo is None:
            return
        if min_clave <= nodo.clave <= max_clave:
            resultados.append({'clave': nodo.clave, 'valor': nodo.valor})
        if nodo.clave > min_clave:
            self._buscar_rango_recursivo(nodo.izquierdo, min_clave, max_clave, resultados)
        if nodo.clave < max_clave:
            self._buscar_rango_recursivo(nodo.derecho, min_clave, max_clave, resultados)
    
    def obtener_minimo(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return {'clave': nodo.clave, 'valor': nodo.valor}
    
    def obtener_maximo(self):
        if self.raiz is None:
            return None
        nodo = self.raiz
        while nodo.derecho:
            nodo = nodo.derecho
        return {'clave': nodo.clave, 'valor': nodo.valor}
    
    def recorrido_inorden(self):
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append({'clave': nodo.clave, 'valor': nodo.valor})
            self._inorden_recursivo(nodo.derecho, resultado)
    
    def obtener_altura(self):
        return self._calcular_altura(self.raiz)
    
    def _calcular_altura(self, nodo):
        if nodo is None:
            return 0
        altura_izq = self._calcular_altura(nodo.izquierdo)
        altura_der = self._calcular_altura(nodo.derecho)
        return 1 + max(altura_izq, altura_der)
    
    def esta_vacio(self):
        return self.raiz is None
    
    def limpiar(self):
        self.raiz = None
        self.tamano = 0
    
    def __len__(self):
        return self.tamano