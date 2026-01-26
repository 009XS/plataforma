# Script de análisis del backend
import re
from collections import Counter, defaultdict

# Cargar archivo
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontrar todas las rutas con sus líneas
routes = []
for i, line in enumerate(lines, 1):
    m = re.search(r"@app\.route\(['\"]([^'\"]+)", line)
    if m:
        routes.append((m.group(1), i, line.strip()))

# Encontrar rutas duplicadas
route_counter = Counter([r[0] for r in routes])
duplicates = [(r, c) for r, c in route_counter.items() if c > 1]

print("=" * 60)
print("ANÁLISIS COMPLETO DEL BACKEND - LEARNING PLATFORM")
print("=" * 60)
print(f"\nTotal de líneas en app.py: {len(lines)}")
print(f"Total de rutas @app.route: {len(routes)}")
print(f"Rutas duplicadas: {len(duplicates)}")

if duplicates:
    print("\n=== RUTAS DUPLICADAS ===")
    for route, count in sorted(duplicates, key=lambda x: -x[1]):
        print(f"  {count}x: {route}")
        # Encontrar líneas
        for r, line_num, line_text in routes:
            if r == route:
                print(f"      L{line_num}")

# Agrupar rutas por prefijo de rol
roles = {'admin': [], 'alumno': [], 'docente': [], 'tutor': [], 'orientador': []}
general = []

for route, line_num, line in routes:
    route_lower = route.lower()
    found = False
    for role in roles:
        if role in route_lower:
            roles[role].append((route, line_num))
            found = True
            break
    if not found:
        general.append((route, line_num))

# Imprimir resumen
print("\n" + "=" * 60)
print("RESUMEN DE RUTAS POR ROL")
print("=" * 60)
for role, role_routes in roles.items():
    print(f"{role.upper()}: {len(role_routes)} rutas")
print(f"GENERAL/API: {len(general)} rutas")

# Mostrar rutas por rol
for role, role_routes in roles.items():
    if role_routes:
        print(f"\n=== RUTAS {role.upper()} ({len(role_routes)}) ===")
        for route, line in role_routes:
            print(f"  L{line}: {route}")

# Analizar CRUD por rol
print("\n" + "=" * 60)
print("ANÁLISIS CRUD POR ROL")
print("=" * 60)

# Buscar patrones CRUD en las rutas
crud_patterns = {
    'CREATE': ['crear', 'create', 'add', 'agregar', 'nuevo', 'new', 'registrar'],
    'READ': ['get', 'list', 'listar', 'obtener', 'ver', 'view', 'detalle', 'consultar'],
    'UPDATE': ['edit', 'editar', 'update', 'actualizar', 'modificar'],
    'DELETE': ['delete', 'eliminar', 'borrar', 'remove', 'cancelar']
}

for role, role_routes in roles.items():
    if role_routes:
        print(f"\n--- {role.upper()} ---")
        crud_count = {'CREATE': 0, 'READ': 0, 'UPDATE': 0, 'DELETE': 0, 'OTHER': 0}
        for route, line in role_routes:
            route_lower = route.lower()
            categorized = False
            for crud_type, patterns in crud_patterns.items():
                if any(p in route_lower for p in patterns):
                    crud_count[crud_type] += 1
                    categorized = True
                    break
            if not categorized:
                crud_count['OTHER'] += 1
        
        for crud_type, count in crud_count.items():
            print(f"  {crud_type}: {count}")

# Buscar funciones con decorador específico de rol
print("\n" + "=" * 60)
print("FUNCIONES CON @role_required")
print("=" * 60)

role_required = defaultdict(list)
for i, line in enumerate(lines, 1):
    m = re.search(r"@role_required\(\s*['\"](\w+)['\"]", line)
    if m:
        role_required[m.group(1)].append(i)

for role, line_nums in sorted(role_required.items()):
    print(f"  {role}: {len(line_nums)} funciones")

# Guardar análisis detallado a archivo
with open('backend_analysis.txt', 'w', encoding='utf-8') as f:
    f.write("ANÁLISIS COMPLETO DEL BACKEND\n")
    f.write("=" * 60 + "\n\n")
    
    f.write(f"Total rutas: {len(routes)}\n")
    f.write(f"Rutas duplicadas: {len(duplicates)}\n\n")
    
    if duplicates:
        f.write("RUTAS DUPLICADAS:\n")
        for route, count in sorted(duplicates, key=lambda x: -x[1]):
            f.write(f"  {count}x: {route}\n")
            for r, line_num, line_text in routes:
                if r == route:
                    f.write(f"      L{line_num}\n")
        f.write("\n")
    
    for role, role_routes in roles.items():
        if role_routes:
            f.write(f"\n=== RUTAS {role.upper()} ({len(role_routes)}) ===\n")
            for route, line in role_routes:
                f.write(f"  L{line}: {route}\n")
    
    f.write(f"\n=== RUTAS GENERALES ({len(general)}) ===\n")
    for route, line in general[:100]:
        f.write(f"  L{line}: {route}\n")
    if len(general) > 100:
        f.write(f"  ... y {len(general) - 100} más\n")

print("\n[OK] Análisis guardado en backend_analysis.txt")
