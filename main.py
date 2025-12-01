"""
Sistema de Gestión de Cafetería Universitaria
Autor: [Tu Nombre]
Fecha: Noviembre 2024

Estructuras de Datos Implementadas:
- Cola de Prioridad (Heap)
- Lista Enlazada
- Árbol BST
- Pila (Stack)
- Conjuntos (Sets)
- Mapas (Diccionarios)
- Algoritmos de Cadenas
"""

import sys
import os
from datetime import datetime



# Agregar paths
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar estructuras de datos
from estructuras.cola_prioridad import ColaPrioridad
from estructuras.lista_enlazada import ListaEnlazada
from estructuras.arbol_bst import ArbolBST
from estructuras.pila import Pila
from estructuras.conjunto import ConjuntoPersonalizado

# Importar modelos
from modelos.usuario import Usuario, GestorUsuarios
from modelos.producto import Producto, GestorProductos
from modelos.pedido import Pedido

# Importar utilidades
from utils.carga_datos import CargadorDatos


class SistemaCafeteria:
    """Sistema principal de gestión de la cafetería"""
    
    def __init__(self):
        # === MAPAS (Diccionarios) ===
        self.gestor_usuarios = GestorUsuarios()
        self.gestor_productos = GestorProductos()
        
        # === COLA DE PRIORIDAD ===
        self.cola_pedidos = ColaPrioridad()
        
        # === ÁRBOL BST ===
        self.arbol_precios = ArbolBST()
        self.arbol_popularidad = ArbolBST()
        
        # === PILA ===
        self.historial_navegacion = Pila(capacidad_maxima=10)
        self.operaciones_deshacer = Pila(capacidad_maxima=20)
        
        # === CONJUNTOS ===
        self.categorias_disponibles = ConjuntoPersonalizado()
        
        # Contadores y estadísticas
        self.total_pedidos_procesados = 0
        self.ventas_totales = 0.0
        
        # Cargar datos iniciales
        self.cargar_datos_iniciales()
    
    def cargar_datos_iniciales(self):
        """Carga datos desde archivos .txt"""
        print("=" * 70)
        print("  INICIALIZANDO SISTEMA DE CAFETERÍA UNIVERSITARIA")
        print("=" * 70)
        print("\nCargando datos iniciales...\n")
        
        cargador = CargadorDatos()
        
        # Cargar usuarios
        datos_usuarios = cargador.cargar_usuarios()
        for dato in datos_usuarios:
            self.gestor_usuarios.registrar_usuario(
                nombre=dato['nombre'],
                tipo=dato['tipo'],
                email=dato.get('email', '')
            )
        
        # Cargar productos
        datos_productos = cargador.cargar_productos()
        for dato in datos_productos:
            producto = self.gestor_productos.registrar_producto(
                nombre=dato['nombre'],
                precio=dato['precio'],
                categoria=dato['categoria']
            )
            
            # Agregar ingredientes
            for ingrediente in dato['ingredientes']:
                producto.agregar_ingrediente(ingrediente)
            
            producto.disponible = dato['disponible']
            
            # Agregar al árbol BST por precio
            self.arbol_precios.insertar(dato['precio'], producto)
            
            # Agregar categoría al conjunto
            self.categorias_disponibles.agregar(dato['categoria'])
        
        # Cargar pedidos históricos
        datos_pedidos = cargador.cargar_pedidos_historicos()
        for dato in datos_pedidos:
            usuario = self.gestor_usuarios.buscar_por_id(dato['usuario_id'])
            if usuario:
                productos_nombres = []
                for pid in dato['producto_ids']:
                    prod = self.gestor_productos.buscar_por_id(pid)
                    if prod:
                        productos_nombres.append(prod.nombre)
                
                pedido_info = {
                    'id': dato['id'],
                    'productos': productos_nombres,
                    'total': dato['total'],
                    'fecha': dato['fecha'],
                    'estado': dato['estado']
                }
                
                usuario.agregar_pedido_al_historial(pedido_info)
                self.total_pedidos_procesados += 1
                self.ventas_totales += dato['total']
        
        print("\n" + "=" * 70)
        print("  ✓ SISTEMA LISTO")
        print("=" * 70)
        print(f"\n  Usuarios registrados: {len(self.gestor_usuarios)}")
        print(f"  Productos disponibles: {len(self.gestor_productos)}")
        print(f"  Categorías: {self.categorias_disponibles.tamanio()}")
        print(f"  Pedidos históricos: {self.total_pedidos_procesados}")
        print(f"  Ventas acumuladas: ${self.ventas_totales:.2f}")
        print("\n" + "=" * 70 + "\n")
    
    def menu_principal(self):
        """Menú principal del sistema"""
        while True:
            self.historial_navegacion.apilar("Menu Principal")
            
            print("\n" + "=" * 70)
            print("  SISTEMA DE CAFETERÍA UNIVERSITARIA - MENÚ PRINCIPAL")
            print("=" * 70)
            print("\n  1. Gestión de Usuarios")
            print("  2. Gestión de Productos/Menú")
            print("  3. Realizar Pedido")
            print("  4. Ver Cola de Pedidos (Prioridad)")
            print("  5. Procesar Siguiente Pedido")
            print("  6. Historial y Estadísticas")
            print("  7. Búsqueda de Productos")
            print("  8. Operaciones con Conjuntos")
            print("  9. Deshacer Última Operación")
            print("  0. Salir")
            print("\n" + "=" * 70)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.menu_usuarios()
            elif opcion == "2":
                self.menu_productos()
            elif opcion == "3":
                self.realizar_pedido()
            elif opcion == "4":
                self.ver_cola_pedidos()
            elif opcion == "5":
                self.procesar_siguiente_pedido()
            elif opcion == "6":
                self.menu_historial_estadisticas()
            elif opcion == "7":
                self.menu_busqueda()
            elif opcion == "8":
                self.menu_conjuntos()
            elif opcion == "9":
                self.deshacer_operacion()
            elif opcion == "0":
                print("\n¡Gracias por usar el sistema!")
                print("Desarrollado para demostrar estructuras de datos\n")
                break
            else:
                print("\n❌ Opción inválida")
            
            input("\nPresione Enter para continuar...")
    
    def menu_usuarios(self):
        """Menú de gestión de usuarios"""
        self.historial_navegacion.apilar("Gestion de Usuarios")
        
        while True:
            print("\n" + "=" * 70)
            print("  GESTIÓN DE USUARIOS")
            print("=" * 70)
            print("\n  1. Registrar nuevo usuario")
            print("  2. Buscar usuario")
            print("  3. Listar todos los usuarios")
            print("  4. Listar por tipo (profesores/estudiantes/staff)")
            print("  5. Ver historial de un usuario (Lista Enlazada)")
            print("  6. Gestionar preferencias/alergias (Conjuntos)")
            print("  0. Volver")
            print("\n" + "=" * 70)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.buscar_usuario()
            elif opcion == "3":
                self.listar_usuarios()
            elif opcion == "4":
                self.listar_usuarios_por_tipo()
            elif opcion == "5":
                self.ver_historial_usuario()
            elif opcion == "6":
                self.gestionar_preferencias_usuario()
            elif opcion == "0":
                break
            else:
                print("\n❌ Opción inválida")
    
    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        print("\n--- REGISTRAR NUEVO USUARIO ---")
        
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("❌ Nombre no puede estar vacío")
            return
        
        print("\nTipo de usuario:")
        print("  1. Profesor")
        print("  2. Estudiante")
        print("  3. Staff")
        tipo_opcion = input("Seleccione (1-3): ").strip()
        
        tipos = {"1": "profesor", "2": "estudiante", "3": "staff"}
        tipo = tipos.get(tipo_opcion, "estudiante")
        
        email = input("Email (opcional): ").strip()
        
        usuario = self.gestor_usuarios.registrar_usuario(nombre, tipo, email)
        
        self.operaciones_deshacer.apilar({
            'tipo': 'registrar_usuario',
            'usuario_id': usuario.obtener_id(),
            'timestamp': datetime.now()
        })
        
        print(f"\n✓ Usuario registrado exitosamente:")
        print(f"  {usuario}")
        print(f"  Prioridad en cola: {usuario.obtener_prioridad()}")
    
    def buscar_usuario(self):
        """Busca un usuario"""
        print("\n--- BUSCAR USUARIO ---")
        print("1. Por ID")
        print("2. Por nombre")
        print("3. Por email")
        
        opcion = input("\nMétodo de búsqueda: ").strip()
        
        usuario = None
        if opcion == "1":
            user_id = input("ID del usuario: ").strip()
            usuario = self.gestor_usuarios.buscar_por_id(user_id)
        elif opcion == "2":
            nombre = input("Nombre: ").strip()
            usuario = self.gestor_usuarios.buscar_por_nombre(nombre)
        elif opcion == "3":
            email = input("Email: ").strip()
            usuario = self.gestor_usuarios.buscar_por_email(email)
        
        if usuario:
            print(f"\n✓ Usuario encontrado:")
            print(f"  {usuario}")
            info = usuario.obtener_info_completa()
            print(f"  Email: {info['email']}")
            print(f"  Total gastado: ${info['total_gastado']:.2f}")
            print(f"  Total pedidos: {info['total_pedidos']}")
            print(f"  Promedio por pedido: ${usuario.calcular_promedio_gasto():.2f}")
            
            if usuario.preferencias:
                print(f"  Preferencias: {', '.join(usuario.obtener_preferencias())}")
            if usuario.alergias:
                print(f"  Alergias: {', '.join(usuario.obtener_alergias())}")
        else:
            print("\n❌ Usuario no encontrado")
    
    def listar_usuarios(self):
        """Lista todos los usuarios"""
        print("\n--- TODOS LOS USUARIOS ---")
        usuarios = self.gestor_usuarios.listar_todos()
        
        if not usuarios:
            print("No hay usuarios registrados")
            return
        
        for usuario in usuarios:
            print(f"  {usuario} - Pedidos: {usuario.info['total_pedidos']}")
    
    def listar_usuarios_por_tipo(self):
        """Lista usuarios por tipo"""
        print("\n--- LISTAR POR TIPO ---")
        print("1. Profesores")
        print("2. Estudiantes")
        print("3. Staff")
        
        opcion = input("\nSeleccione tipo: ").strip()
        tipos = {"1": "profesor", "2": "estudiante", "3": "staff"}
        tipo = tipos.get(opcion)
        
        if not tipo:
            print("❌ Tipo inválido")
            return
        
        usuarios = self.gestor_usuarios.listar_por_tipo(tipo)
        print(f"\n{tipo.upper()}S ({len(usuarios)}):")
        for usuario in usuarios:
            print(f"  {usuario}")
    
    def ver_historial_usuario(self):
        """Ver historial de pedidos de un usuario"""
        print("\n--- HISTORIAL DE USUARIO (Lista Enlazada) ---")
        
        nombre = input("Nombre del usuario: ").strip()
        usuario = self.gestor_usuarios.buscar_por_nombre(nombre)
        
        if not usuario:
            print("❌ Usuario no encontrado")
            return
        
        print(f"\nHistorial de {usuario.obtener_nombre()}:")
        print(f"Estructura: Lista Enlazada con {len(usuario.historial)} nodos\n")
        
        historial = usuario.obtener_historial_completo()
        
        if not historial:
            print("  Sin pedidos previos")
            return
        
        for i, pedido in enumerate(historial, 1):
            print(f"  {i}. [{pedido['id']}] ${pedido['total']:.2f}")
            print(f"     Productos: {', '.join(pedido['productos'])}")
            print(f"     Fecha: {pedido['fecha']}")
            print()
        
        print(f"Total gastado: ${usuario.info['total_gastado']:.2f}")
        print(f"Promedio: ${usuario.calcular_promedio_gasto():.2f}")
    
    def gestionar_preferencias_usuario(self):
        """Gestiona preferencias y alergias"""
        print("\n--- PREFERENCIAS Y ALERGIAS (Conjuntos) ---")
        
        nombre = input("Nombre del usuario: ").strip()
        usuario = self.gestor_usuarios.buscar_por_nombre(nombre)
        
        if not usuario:
            print("❌ Usuario no encontrado")
            return
        
        while True:
            print(f"\nUsuario: {usuario.obtener_nombre()}")
            print(f"Preferencias actuales: {usuario.obtener_preferencias()}")
            print(f"Alergias actuales: {usuario.obtener_alergias()}")
            
            print("\n1. Agregar preferencia")
            print("2. Eliminar preferencia")
            print("3. Agregar alergia")
            print("4. Eliminar alergia")
            print("0. Volver")
            
            opcion = input("\nOpción: ").strip()
            
            if opcion == "1":
                pref = input("Producto favorito: ").strip()
                usuario.agregar_preferencia(pref)
                print(f"✓ Agregado a preferencias")
            elif opcion == "2":
                pref = input("Producto a eliminar: ").strip()
                if usuario.eliminar_preferencia(pref):
                    print(f"✓ Eliminado de preferencias")
                else:
                    print("❌ No estaba en preferencias")
            elif opcion == "3":
                alergia = input("Ingrediente alérgico: ").strip()
                usuario.agregar_alergia(alergia)
                print(f"✓ Agregado a alergias")
            elif opcion == "4":
                alergia = input("Alergia a eliminar: ").strip()
                if usuario.eliminar_alergia(alergia):
                    print(f"✓ Eliminado de alergias")
                else:
                    print("❌ No estaba en alergias")
            elif opcion == "0":
                break
    
    def menu_productos(self):
        """Menú de gestión de productos"""
        self.historial_navegacion.apilar("Gestion de Productos")
        
        while True:
            print("\n" + "=" * 70)
            print("  GESTIÓN DE PRODUCTOS/MENÚ")
            print("=" * 70)
            print("\n  1. Registrar nuevo producto")
            print("  2. Buscar producto")
            print("  3. Listar todos los productos")
            print("  4. Listar por categoría")
            print("  5. Ver productos por rango de precios (Árbol BST)")
            print("  6. Producto más barato/caro (Árbol BST)")
            print("  7. Modificar disponibilidad")
            print("  0. Volver")
            print("\n" + "=" * 70)
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_producto()
            elif opcion == "2":
                self.buscar_producto()
            elif opcion == "3":
                self.listar_productos()
            elif opcion == "4":
                self.listar_productos_por_categoria()
            elif opcion == "5":
                self.productos_por_rango_precios()
            elif opcion == "6":
                self.productos_extremos()
            elif opcion == "7":
                self.modificar_disponibilidad()
            elif opcion == "0":
                break
            else:
                print("\n❌ Opción inválida")
    
    def registrar_producto(self):
        """Registra un nuevo producto"""
        print("\n--- REGISTRAR NUEVO PRODUCTO ---")
        
        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("❌ Nombre no puede estar vacío")
            return
        
        try:
            precio = float(input("Precio: $").strip())
        except ValueError:
            print("❌ Precio inválido")
            return
        
        categoria = input("Categoría: ").strip()
        
        producto = self.gestor_productos.registrar_producto(nombre, precio, categoria)
        
        print("\nIngredientes (separados por coma, o Enter para omitir):")
        ingredientes_str = input().strip()
        if ingredientes_str:
            for ing in ingredientes_str.split(','):
                producto.agregar_ingrediente(ing.strip())
        
        self.arbol_precios.insertar(precio, producto)
        self.categorias_disponibles.agregar(categoria)
        
        self.operaciones_deshacer.apilar({
            'tipo': 'registrar_producto',
            'producto_id': producto.id,
            'timestamp': datetime.now()
        })
        
        print(f"\n✓ Producto registrado: {producto}")
    
    def buscar_producto(self):
        """Busca un producto"""
        print("\n--- BUSCAR PRODUCTO ---")
        termino = input("Nombre o parte del nombre: ").strip()
        
        resultados = self.gestor_productos.buscar_por_nombre(termino)
        
        if resultados:
            print(f"\n✓ Encontrados {len(resultados)} productos:")
            for prod in resultados:
                estado = "✓ Disponible" if prod.disponible else "✗ No disponible"
                print(f"  {prod} - {estado}")
                if prod.ingredientes:
                    print(f"    Ingredientes: {', '.join(prod.ingredientes)}")
        else:
            print("\n❌ No se encontraron productos")
    
    def listar_productos(self):
        """Lista todos los productos"""
        print("\n--- TODOS LOS PRODUCTOS ---")
        productos = self.gestor_productos.listar_todos()
        
        for prod in productos:
            estado = "✓" if prod.disponible else "✗"
            print(f"  {estado} {prod}")
    
    def listar_productos_por_categoria(self):
        """Lista productos por categoría"""
        print("\n--- CATEGORÍAS DISPONIBLES ---")
        categorias = self.categorias_disponibles.obtener_lista()
        
        for i, cat in enumerate(categorias, 1):
            print(f"  {i}. {cat}")
        
        categoria = input("\nCategoria: ").strip()
        
        productos = self.gestor_productos.listar_por_categoria(categoria)
        print(f"\n{categoria} ({len(productos)} productos):")
        for prod in productos:
            print(f"  {prod}")
    
    def productos_por_rango_precios(self):
        """Busca productos en un rango de precios"""
        print("\n--- BÚSQUEDA POR RANGO DE PRECIOS (Árbol BST) ---")
        
        try:
            min_precio = float(input("Precio mínimo: $").strip())
            max_precio = float(input("Precio máximo: $").strip())
        except ValueError:
            print("❌ Precios inválidos")
            return
        
        resultados = self.arbol_precios.buscar_rango(min_precio, max_precio)
        
        print(f"\nProductos entre ${min_precio:.2f} y ${max_precio:.2f}:")
        print(f"(Búsqueda eficiente con Árbol BST)\n")
        
        for item in resultados:
            producto = item['valor']
            print(f"  ${item['clave']:.2f} - {producto.nombre}")
    
    def productos_extremos(self):
        """Muestra productos más baratos y más caros"""
        print("\n--- PRODUCTOS EXTREMOS (Árbol BST) ---")
        
        minimo = self.arbol_precios.obtener_minimo()
        maximo = self.arbol_precios.obtener_maximo()
        
        if minimo:
            print(f"\nMás barato: ${minimo['clave']:.2f} - {minimo['valor'].nombre}")
        
        if maximo:
            print(f"Más caro: ${maximo['clave']:.2f} - {maximo['valor'].nombre}")
    
    def modificar_disponibilidad(self):
        """Modifica disponibilidad de un producto"""
        nombre = input("\nNombre del producto: ").strip()
        resultados = self.gestor_productos.buscar_por_nombre(nombre)
        
        if not resultados:
            print("❌ Producto no encontrado")
            return
        
        if len(resultados) > 1:
            print("\nVarios productos encontrados:")
            for i, prod in enumerate(resultados, 1):
                print(f"  {i}. {prod}")
            try:
                idx = int(input("Seleccione número: ")) - 1
                producto = resultados[idx]
            except:
                print("❌ Selección inválida")
                return
        else:
            producto = resultados[0]
        
        producto.disponible = not producto.disponible
        estado = "disponible" if producto.disponible else "no disponible"
        print(f"\n✓ Producto ahora está: {estado}")
    
    def realizar_pedido(self):
        """Crea un nuevo pedido"""
        print("\n" + "=" * 70)
        print("  REALIZAR NUEVO PEDIDO")
        print("=" * 70)
        
        nombre_usuario = input("\nNombre del usuario: ").strip()
        usuario = self.gestor_usuarios.buscar_por_nombre(nombre_usuario)
        
        if not usuario:
            print("❌ Usuario no encontrado")
            return
        
        print(f"\nUsuario: {usuario}")
        print(f"Prioridad: {usuario.obtener_prioridad()} ", end="")
        if usuario.obtener_prioridad() == 1:
            print("(ALTA - Profesor)")
        elif usuario.obtener_prioridad() == 2:
            print("(MEDIA - Staff)")
        else:
            print("(NORMAL - Estudiante)")
        
        productos_pedido = []
        total = 0.0
        
        print("\n--- Agregar productos al pedido ---")
        print("(Escriba 'fin' para terminar)")
        
        while True:
            nombre_prod = input("\nProducto: ").strip()
            
            if nombre_prod.lower() == 'fin':
                break
            
            resultados = self.gestor_productos.buscar_por_nombre(nombre_prod)
            
            if not resultados:
                print("❌ Producto no encontrado")
                continue
            
            if len(resultados) > 1:
                print("\nVarios productos encontrados:")
                for i, prod in enumerate(resultados, 1):
                    print(f"  {i}. {prod}")
                try:
                    idx = int(input("Seleccione número: ")) - 1
                    producto = resultados[idx]
                except:
                    print("❌ Selección inválida")
                    continue
            else:
                producto = resultados[0]
            
            if not producto.disponible:
                print(f"❌ {producto.nombre} no está disponible")
                continue
            
            puede_consumir, alergenos = usuario.puede_consumir_producto(producto)
            if not puede_consumir:
                print(f"⚠️  ADVERTENCIA: Este producto contiene: {', '.join(alergenos)}")
                confirmar = input("¿Continuar de todos modos? (s/n): ")
                if confirmar.lower() != 's':
                    continue
            
            productos_pedido.append(producto)
            total += producto.precio
            print(f"✓ Agregado: {producto.nombre} - ${producto.precio:.2f}")
            print(f"  Total actual: ${total:.2f}")
        
        if not productos_pedido:
            print("\n❌ No se agregaron productos")
            return
        
        pedido = Pedido(usuario, productos_pedido)
        
        pedido_id = self.cola_pedidos.agregar(
            pedido.prioridad,
            pedido,
            pedido.id
        )
        
        self.operaciones_deshacer.apilar({
            'tipo': 'realizar_pedido',
            'pedido_id': pedido_id,
            'timestamp': datetime.now()
        })
        
        print("\n" + "=" * 70)
        print("  ✓ PEDIDO CREADO EXITOSAMENTE")
        print("=" * 70)
        print(f"\nID del pedido: {pedido.id}")
        print(f"Usuario: {usuario.obtener_nombre()}")
        print(f"Prioridad en cola: {pedido.prioridad}")
        print(f"Total: ${pedido.calcular_total():.2f}")
        print(f"\nProductos:")
        for prod in productos_pedido:
            print(f"  - {prod.nombre} ${prod.precio:.2f}")
        print(f"\nPosición en cola: Será atendido según prioridad")
        print("=" * 70)
    
    def ver_cola_pedidos(self):
        """Muestra la cola de pedidos"""
        print("\n" + "=" * 70)
        print("  COLA DE PEDIDOS (Cola de Prioridad - Heap)")
        print("=" * 70)
        
        if self.cola_pedidos.esta_vacia():
            print("\n  No hay pedidos en cola")
            return
        
        pedidos = self.cola_pedidos.ver_todos()
        
        print(f"\nTotal de pedidos en cola: {len(pedidos)}\n")
        print("Orden de atención (por prioridad):\n")
        
        for i, item in enumerate(pedidos, 1):
            pedido = item['pedido']
            prioridad = item['prioridad']
            
            tipo_emoji = {1: "🎓 PROFESOR", 2: "👔 STAFF", 3: "👤 ESTUDIANTE"}
            tipo = tipo_emoji.get(prioridad, "👤 CLIENTE")
            
            print(f"{i}. [{tipo}] {pedido.id}")
            print(f"   Usuario: {pedido.usuario.obtener_nombre()}")
            print(f"   Total: ${pedido.calcular_total():.2f}")
            print(f"   Productos: {len(pedido.productos)}")
            print()
        
        print("=" * 70)
        
        siguiente = self.cola_pedidos.ver_siguiente()
        if siguiente:
            pedido_sig = siguiente['pedido']
            print(f"\n→ SIGUIENTE A ATENDER: {pedido_sig.id} - {pedido_sig.usuario.obtener_nombre()}")
    
    def procesar_siguiente_pedido(self):
        """Procesa el siguiente pedido"""
        print("\n--- PROCESAR SIGUIENTE PEDIDO ---")
        
        if self.cola_pedidos.esta_vacia():
            print("❌ No hay pedidos en cola")
            return
        
        item = self.cola_pedidos.atender_siguiente()
        pedido = item['pedido']
        
        print(f"\n→ Atendiendo pedido: {pedido.id}")
        print(f"  Usuario: {pedido.usuario.obtener_nombre()}")
        print(f"  Prioridad: {item['prioridad']}")
        print(f"  Total: ${pedido.calcular_total():.2f}")
        
        pedido.cambiar_estado("preparando")
        
        input("\nPresione Enter para marcar como listo...")
        pedido.cambiar_estado("listo")
        
        input("Presione Enter para entregar...")
        pedido.cambiar_estado("entregado")
        
        pedido_info = {
            'id': pedido.id,
            'productos': [p.nombre for p in pedido.productos],
            'total': pedido.calcular_total(),
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'estado': 'entregado'
        }
        pedido.usuario.agregar_pedido_al_historial(pedido_info)
        self.total_pedidos_procesados += 1
        self.ventas_totales += pedido.calcular_total()
        
        print(f"\n✓ Pedido {pedido.id} completado")
        print(f"\nPedidos restantes en cola: {self.cola_pedidos.tamanio()}")
    
        def menu_historial_estadisticas(self):  
            """Menú de historial y estadísticas"""
    self.historial_navegacion.apilar("Historial y Estadisticas")
    
    while True:
        print("\n" + "=" * 70)
        print("  HISTORIAL Y ESTADÍSTICAS")
        print("=" * 70)
        print("\n  1. Estadísticas generales del sistema")
        print("  2. Ver historial de navegación (Pila)")
        print("  3. Top usuarios por gasto")
        print("  4. Productos más vendidos")
        print("  5. Estadísticas por tipo de usuario")
        print("  0. Volver")
        print("\n" + "=" * 70)
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            self.estadisticas_generales()
        elif opcion == "2":
            self.ver_historial_navegacion()
        elif opcion == "3":
            self.top_usuarios()
        elif opcion == "4":
            self.productos_mas_vendidos()
        elif opcion == "5":
            self.estadisticas_por_tipo()
        elif opcion == "0":
            break
        else:
            print("\n❌ Opción inválida")

def estadisticas_generales(self):
    """Estadísticas generales"""
    print("\n" + "=" * 70)
    print("  ESTADÍSTICAS GENERALES DEL SISTEMA")
    print("=" * 70)
    
    stats_usuarios = self.gestor_usuarios.obtener_estadisticas()
    
    print(f"\n📊 USUARIOS:")
    print(f"  Total registrados: {stats_usuarios['total_usuarios']}")
    print(f"  Por tipo:")
    for tipo, cantidad in stats_usuarios['por_tipo'].items():
        print(f"    - {tipo.capitalize()}: {cantidad}")
    
    print(f"\n💰 VENTAS:")
    print(f"  Total de pedidos procesados: {self.total_pedidos_procesados}")
    print(f"  Ventas totales: ${self.ventas_totales:.2f}")
    if self.total_pedidos_procesados > 0:
        promedio = self.ventas_totales / self.total_pedidos_procesados
        print(f"  Ticket promedio: ${promedio:.2f}")
    
    print(f"\n📦 PRODUCTOS:")
    print(f"  Total en catálogo: {len(self.gestor_productos)}")
    print(f"  Categorías: {self.categorias_disponibles.tamanio()}")
    
    print(f"\n⏳ COLA ACTUAL:")
    print(f"  Pedidos en espera: {self.cola_pedidos.tamanio()}")
    
    print("\n" + "=" * 70)

def ver_historial_navegacion(self):
    """Historial de navegación"""
    print("\n--- HISTORIAL DE NAVEGACIÓN (Pila - LIFO) ---")
    
    if self.historial_navegacion.esta_vacia():
        print("Sin historial")
        return
    
    print(f"\nÚltimas {len(self.historial_navegacion)} pantallas visitadas:\n")
    
    for i, pantalla in enumerate(self.historial_navegacion.ver_todos(), 1):
        print(f"  {i}. {pantalla}")
    
    print(f"\nPantalla actual (tope de la pila): {self.historial_navegacion.ver_tope()}")

def top_usuarios(self):
    """Top usuarios"""
    print("\n--- TOP USUARIOS POR GASTO ---")
    
    usuarios = self.gestor_usuarios.listar_todos()
    usuarios_ordenados = sorted(
        usuarios,
        key=lambda u: u.info['total_gastado'],
        reverse=True
    )
    
    print("\nTop 10 usuarios:\n")
    for i, usuario in enumerate(usuarios_ordenados[:10], 1):
        print(f"{i}. {usuario.obtener_nombre()}")
        print(f"   Total gastado: ${usuario.info['total_gastado']:.2f}")
        print(f"   Pedidos: {usuario.info['total_pedidos']}")
        print(f"   Promedio: ${usuario.calcular_promedio_gasto():.2f}")
        print()

def productos_mas_vendidos(self):
    """Productos más vendidos"""
    print("\n--- PRODUCTOS MÁS POPULARES ---")
    print("(Basado en historial de pedidos)\n")
    
    conteo = {}
    
    for usuario in self.gestor_usuarios.listar_todos():
        for pedido in usuario.obtener_historial_completo():
            for prod_nombre in pedido['productos']:
                conteo[prod_nombre] = conteo.get(prod_nombre, 0) + 1
    
    ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    
    for i, (producto, cantidad) in enumerate(ordenados[:10], 1):
        print(f"{i}. {producto}: {cantidad} veces")

def estadisticas_por_tipo(self):
    """Estadísticas por tipo"""
    print("\n--- ESTADÍSTICAS POR TIPO DE USUARIO ---")
    
    for tipo in ['profesor', 'estudiante', 'staff']:
        usuarios = self.gestor_usuarios.listar_por_tipo(tipo)
        
        if not usuarios:
            continue
        
        total_gastado = sum(u.info['total_gastado'] for u in usuarios)
        total_pedidos = sum(u.info['total_pedidos'] for u in usuarios)
        
        print(f"\n{tipo.upper()}S:")
        print(f"  Cantidad: {len(usuarios)}")
        print(f"  Total gastado: ${total_gastado:.2f}")
        print(f"  Total pedidos: {total_pedidos}")
        if usuarios:
            promedio = total_gastado / len(usuarios)
            print(f"  Promedio por persona: ${promedio:.2f}")

def menu_busqueda(self):
    """Menú de búsqueda"""
    print("\n--- BÚSQUEDA (Algoritmos de Cadenas) ---")
    print("1. Buscar productos")
    print("2. Buscar usuarios")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == "1":
        termino = input("Término de búsqueda: ").strip().lower()
        resultados = self.gestor_productos.buscar_por_nombre(termino)
        
        print(f"\nEncontrados {len(resultados)} productos:")
        for prod in resultados:
            print(f"  {prod}")
    
    elif opcion == "2":
        termino = input("Nombre: ").strip()
        usuario = self.gestor_usuarios.buscar_por_nombre(termino)
        
        if usuario:
            print(f"\n✓ {usuario}")
        else:
            print("\n❌ No encontrado")

def menu_conjuntos(self):
    """Operaciones con conjuntos"""
    print("\n--- OPERACIONES CON CONJUNTOS ---")
    print("\nCategorías disponibles:")
    print(self.categorias_disponibles)
    
    print("\n1. Ver todas las categorías")
    print("2. Buscar productos de múltiples categorías")
    
    opcion = input("\nOpción: ").strip()
    
    if opcion == "1":
        print("\nCategorías:")
        for cat in self.categorias_disponibles:
            print(f"  - {cat}")
    
    elif opcion == "2":
        print("\nIngrese categorías separadas por coma:")
        cats_str = input().strip()
        categorias = [c.strip() for c in cats_str.split(',')]
        
        productos_totales = []
        for cat in categorias:
            productos_totales.extend(
                self.gestor_productos.listar_por_categoria(cat)
            )
        
        productos_unicos = list(set(productos_totales))
        
        print(f"\nProductos en {' o '.join(categorias)}:")
        for prod in productos_unicos:
            print(f"  {prod}")

def deshacer_operacion(self):
    """Deshace operación"""
    print("\n--- DESHACER ÚLTIMA OPERACIÓN (Pila) ---")
    
    if self.operaciones_deshacer.esta_vacia():
        print("❌ No hay operaciones para deshacer")
        return
    
    operacion = self.operaciones_deshacer.desapilar()
    
    print(f"\nDeshaciendo: {operacion['tipo']}")
    print(f"Timestamp: {operacion['timestamp']}")
    
    print(f"\n✓ Operación deshecha")
    print(f"Operaciones restantes en pila: {self.operaciones_deshacer.tamanio()}")

def main():  # Sin indentación (función global)
     """Función principal"""
try:
        sistema = SistemaCafeteria()
        sistema.menu_principal()
except KeyboardInterrupt:
        print("\n\nSistema interrumpido por el usuario")
except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":  # Sin indentación
    main()