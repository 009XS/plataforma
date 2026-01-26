import re
import os

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.py'))

def analyze_app():
    if not os.path.exists(APP_PATH):
        print(f"File not found: {APP_PATH}")
        return

    with open(APP_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    lines = content.split('\n')
    
    # 1. Analyze Tables
    table_pattern = re.compile(r'CREATE TABLE IF NOT EXISTS\s+([a-zA-Z0-9_]+)', re.IGNORECASE)
    tables = table_pattern.findall(content)
    print(f"Found {len(tables)} tables:")
    print(", ".join(sorted(tables)))
    print("-" * 20)

    # 2. Analyze Routes
    routes = []
    route_pattern = re.compile(r'@app\.route\s*\(\s*[\'"]([^\'"]+)[\'"]')
    func_pattern = re.compile(r'def\s+([a-zA-Z0-9_]+)\s*\(')
    
    api_patterns = {
        'admin': [],
        'docente': [],
        'alumno': [],
        'tutor': [],
        'orientador': [],
        'auth': [],
        'api_general': [],
        'unknown': []
    }

    current_route = None
    
    for i, line in enumerate(lines):
        route_match = route_pattern.search(line)
        if route_match:
            current_route = route_match.group(1)
            # Find function
            for j in range(i+1, min(i+10, len(lines))):
                func_match = func_pattern.search(lines[j])
                if func_match:
                    func_name = func_match.group(1)
                    
                    # Analyze body size (rough heuristic)
                    body_start = j + 1
                    body_lines = 0
                    has_pass = False
                    is_json_empty = False
                    
                    for k in range(body_start, min(body_start + 50, len(lines))):
                        if lines[k].strip().startswith('def ') or lines[k].strip().startswith('@'):
                            break
                        body_lines += 1
                        if 'pass' == lines[k].strip():
                            has_pass = True
                        if 'return jsonify([])' in lines[k] or 'return jsonify({})' in lines[k]:
                            is_json_empty = True
                            
                    category = 'unknown'
                    if '/admin' in current_route: category = 'admin'
                    elif '/docente' in current_route: category = 'docente'
                    elif '/alumno' in current_route: category = 'alumno'
                    elif '/tutor' in current_route: category = 'tutor'
                    elif '/orientador' in current_route: category = 'orientador'
                    elif '/login' in current_route or '/register' in current_route: category = 'auth'
                    elif '/api' in current_route: category = 'api_general'
                    
                    api_patterns[category].append({
                        'route': current_route,
                        'func': func_name, 
                        'lines': body_lines,
                        'suspicious': has_pass or is_json_empty or body_lines < 3
                    })
                    break

    for cat, items in api_patterns.items():
        suspicious = [x for x in items if x['suspicious']]
        print(f"Category: {cat.upper()} - Total: {len(items)}, Suspicious/Stub: {len(suspicious)}")
        if len(suspicious) > 0:
            print(f"  Sample suspicious in {cat}:")
            for s in suspicious[:5]:
                print(f"    {s['route']} ({s['func']})")
                
    print("-" * 20)
    print("Sample 'Unknown' Routes (checking for missed features):")
    for r in api_patterns['unknown'][:10]:
        print(f"  {r['route']}")

if __name__ == "__main__":
    analyze_app()
