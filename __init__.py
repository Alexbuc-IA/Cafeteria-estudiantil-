"""
Paquete de estructuras de datos personalizadas

Estructuras implementadas:
- ColaPrioridad: Heap para gestionar pedidos con prioridad
- ListaEnlazada: Lista enlazada simple para historial
- ArbolBST: Árbol binario de búsqueda para organizar productos
- Pila: Stack LIFO para historial de navegación y deshacer
- ConjuntoPersonalizado: Wrapper de sets con operaciones adicionales
"""

from .cola_prioridad import ColaPrioridad
from .lista_enlazada import ListaEnlazada, Nodo
from .arbol_bst import ArbolBST, NodoBST
from .pila import Pila
from .conjunto import ConjuntoPersonalizado

__all__ = [
    'ColaPrioridad',
    'ListaEnlazada',
    'Nodo',
    'ArbolBST',
    'NodoBST',
    'Pila',
    'ConjuntoPersonalizado'
]

__version__ = '1.0.0'
__author__ = 'Tu Nombre'