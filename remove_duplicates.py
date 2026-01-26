# Script mejorado para eliminar rutas duplicadas de app.py
# Usa un enfoque más conservador para mantener la sintaxis válida

import re
from collections import defaultdict

def find_function_boundaries(lines, decorator_line_idx):
    """
    Encuentra los límites exactos de una función incluyendo todos sus decoradores.
    Retorna (primer_decorador, fin_funcion) como índices 0-based.
    """
    # Buscar hacia atrás para encontrar el primer decorador de este grupo
    start_idx = decorator_line_idx
    
    # Avanzar para encontrar la línea 'def'
    def_idx = decorator_line_idx
    while def_idx < len(lines) and not lines[def_idx].strip().startswith('def '):
        def_idx += 1
    
    if def_idx >= len(lines):
        return decorator_line_idx, decorator_line_idx + 1
    
    # Encontrar la indentación de la función
    def_line = lines[def_idx]
    base_indent = len(def_line) - len(def_line.lstrip())
    
    # Buscar el final de la función
    end_idx = def_idx + 1
    while end_idx < len(lines):
        line = lines[end_idx]
        stripped = line.strip()
        
        # Línea vacía o comentario - continuar
        if not stripped or stripped.startswith('#'):
            end_idx += 1
            continue
        
        current_indent = len(line) - len(line.lstrip())
        
        # Si la indentación es <= base (y no es línea vacía), terminó la función
        if current_indent <= base_indent:
            break
        
        end_idx += 1
    
    return start_idx, end_idx

print("Cargando app.py...")
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    original_count = len(lines)

print(f"Total líneas originales: {original_count}")

# Encontrar todas las rutas @app.route con su línea
routes_info = []
i = 0
while i < len(lines):
    m = re.search(r"@app\.route\(['\"]([^'\"]+)['\"]", lines[i])
    if m:
        route = m.group(1)
        routes_info.append({
            'route': route,
            'decorator_line': i,
            'line_text': lines[i].rstrip()
        })
    i += 1

print(f"Total rutas encontradas: {len(routes_info)}")

# Agrupar por ruta
route_groups = defaultdict(list)
for r in routes_info:
    route_groups[r['route']].append(r)

# Identificar duplicados
duplicates = {k: v for k, v in route_groups.items() if len(v) > 1}
print(f"Rutas duplicadas: {len(duplicates)}")

if not duplicates:
    print("No hay duplicados que eliminar")
    exit()

# Para cada grupo de duplicados, encontrar qué función conservar
# Conservamos la primera aparición por defecto (más arriba en el archivo)
# ya que Flask usa la última, pero podemos mantener la más completa

lines_to_delete = set()
routes_to_keep = []

for route, instances in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n=== {route} ({len(instances)} duplicados) ===")
    
    # Calcular límites para cada instancia
    function_info = []
    for inst in instances:
        start, end = find_function_boundaries(lines, inst['decorator_line'])
        length = end - start
        function_info.append({
            **inst,
            'start': start,
            'end': end, 
            'length': length
        })
    
    # Ordenar por longitud (mayor primero) para conservar la más completa
    function_info.sort(key=lambda x: -x['length'])
    
    best = function_info[0]
    routes_to_keep.append({
        'route': route,
        'line': best['decorator_line'] + 1,
        'length': best['length']
    })
    print(f"  CONSERVAR: L{best['start']+1}-L{best['end']} ({best['length']} líneas)")
    
    # Marcar las demás para eliminación
    for func in function_info[1:]:
        print(f"  ELIMINAR:  L{func['start']+1}-L{func['end']} ({func['length']} líneas)")
        for line_idx in range(func['start'], func['end']):
            lines_to_delete.add(line_idx)

print(f"\nTotal líneas a eliminar: {len(lines_to_delete)}")

# Crear el nuevo archivo sin las líneas duplicadas
new_lines = []
for i, line in enumerate(lines):
    if i not in lines_to_delete:
        new_lines.append(line)

print(f"Líneas finales: {len(new_lines)}")

# Verificar sintaxis antes de guardar
print("\nVerificando sintaxis...")
try:
    import ast
    content = ''.join(new_lines)
    ast.parse(content)
    print("[OK] Sintaxis válida")
    
    # Guardar
    with open('app.py', 'w', encoding='utf-8', newline='') as f:
        f.writelines(new_lines)
    print(f"[OK] app.py actualizado correctamente")
    print(f"    Líneas originales: {original_count}")
    print(f"    Líneas finales: {len(new_lines)}")
    print(f"    Líneas eliminadas: {original_count - len(new_lines)}")
    
    # Guardar reporte
    with open('duplicate_removal_report.txt', 'w', encoding='utf-8') as f:
        f.write("REPORTE DE ELIMINACIÓN DE DUPLICADOS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Líneas originales: {original_count}\n")
        f.write(f"Líneas finales: {len(new_lines)}\n")
        f.write(f"Líneas eliminadas: {original_count - len(new_lines)}\n")
        f.write(f"Rutas duplicadas procesadas: {len(duplicates)}\n\n")
        f.write("RUTAS CONSERVADAS:\n")
        for r in routes_to_keep:
            f.write(f"  {r['route']} -> L{r['line']} ({r['length']} líneas)\n")
    
except SyntaxError as e:
    print(f"[ERROR] Error de sintaxis: {e}")
    print("No se guardaron cambios. Revise el script.")
