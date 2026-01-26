# Script para generar reporte detallado de duplicados
# Y crear un plan de eliminación manual más seguro

import re
from collections import defaultdict

print("Cargando app.py...")
with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total líneas: {len(lines)}")

# Encontrar todas las rutas
routes_info = []
for i, line in enumerate(lines):
    m = re.search(r"@app\.route\(['\"]([^'\"]+)['\"]", line)
    if m:
        # Buscar nombre de función
        func_name = None
        for j in range(i, min(i+5, len(lines))):
            fn = re.search(r"def\s+(\w+)\s*\(", lines[j])
            if fn:
                func_name = fn.group(1)
                break
        
        routes_info.append({
            'route': m.group(1),
            'line': i + 1,  # 1-indexed
            'func_name': func_name,
            'decorator_text': line.strip()
        })

# Agrupar por ruta
route_groups = defaultdict(list)
for r in routes_info:
    route_groups[r['route']].append(r)

# Identificar duplicados
duplicates = {k: v for k, v in route_groups.items() if len(v) > 1}

print(f"Total rutas: {len(routes_info)}")
print(f"Rutas únicas: {len(route_groups)}")
print(f"Rutas duplicadas: {len(duplicates)}")

# Generar reporte detallado
report = []
report.append("=" * 70)
report.append("REPORTE DE RUTAS DUPLICADAS EN app.py")
report.append("=" * 70)
report.append(f"\nTotal de rutas: {len(routes_info)}")
report.append(f"Rutas con duplicados: {len(duplicates)}")
report.append(f"Total de instancias duplicadas para eliminar: {sum(len(v)-1 for v in duplicates.values())}")
report.append("\n" + "=" * 70)
report.append("DUPLICADOS ORDENADOS POR CANTIDAD")
report.append("=" * 70)

# Ordenar por cantidad de duplicados
sorted_dupes = sorted(duplicates.items(), key=lambda x: -len(x[1]))

for route, instances in sorted_dupes:
    report.append(f"\n--- {route} ({len(instances)} definiciones) ---")
    for inst in instances:
        report.append(f"  L{inst['line']}: {inst['func_name']} -> {inst['decorator_text'][:60]}...")
    report.append(f"  [RECOMENDACIÓN: Conservar L{instances[-1]['line']} y eliminar las anteriores]")

# Generar script de líneas a eliminar
report.append("\n" + "=" * 70)
report.append("RANGOS DE LÍNEAS PARA ELIMINAR")
report.append("(Conservamos la última definición de cada ruta duplicada)")
report.append("=" * 70)

total_to_remove = 0
for route, instances in sorted_dupes:
    # Mantener la última, eliminar las anteriores
    to_remove = instances[:-1]  # Todas menos la última
    if to_remove:
        report.append(f"\n{route}:")
        for inst in to_remove:
            report.append(f"  ELIMINAR función '{inst['func_name']}' en línea {inst['line']}")
            total_to_remove += 1

report.append(f"\n\nTOTAL DE FUNCIONES DUPLICADAS A ELIMINAR: {total_to_remove}")

# Guardar reporte
report_text = '\n'.join(report)
with open('duplicates_detailed_report.txt', 'w', encoding='utf-8') as f:
    f.write(report_text)

print(report_text)
print("\n\n[OK] Reporte guardado en duplicates_detailed_report.txt")

# Generar un archivo Python con las líneas exactas de cada función duplicada
print("\nGenerando análisis de funciones...")

# Para cada ruta duplicada, mostrar dónde está cada función
with open('duplicates_functions.txt', 'w', encoding='utf-8') as f:
    f.write("FUNCIONES DUPLICADAS - LÍNEAS EXACTAS\n")
    f.write("=" * 70 + "\n\n")
    
    for route, instances in sorted_dupes:
        f.write(f"\n{'='*70}\n")
        f.write(f"RUTA: {route}\n")
        f.write(f"{'='*70}\n")
        
        for idx, inst in enumerate(instances):
            f.write(f"\n--- Instancia {idx+1}: {inst['func_name']} (Línea {inst['line']}) ---\n")
            # Mostrar las primeras 15 líneas de cada función
            start = inst['line'] - 1  # 0-indexed
            for j in range(start, min(start + 15, len(lines))):
                f.write(f"L{j+1}: {lines[j]}")
            f.write("...\n")

print("[OK] Análisis de funciones guardado en duplicates_functions.txt")
