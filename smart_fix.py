import re

def smart_fix():
    with open('app.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # We need to identify which lines define functions that are ROUTES.
    # A route function is usually preceded by @app.route(...) or @login_required etc.
    # But essentially, if it crashes with "Function mapping overwriting", it's because it's a view function.
    
    # Let's find all function definitions and their line numbers.
    func_defs = []
    func_pattern = re.compile(r'^\s*def\s+([a-zA-Z0-9_]+)\s*\(')
    
    for i, line in enumerate(lines):
        match = func_pattern.match(line)
        if match:
            func_name = match.group(1)
            # Check for decorator in previous lines (heuristic)
            is_route = False
            for j in range(i-1, i-10, -1):
                if j < 0: break
                prev = lines[j].strip()
                if prev.startswith('@app.route') or prev.startswith('@role_required') or prev.startswith('@login_required'):
                    is_route = True
                    break
                if prev.startswith('def ') or prev == '': # Stop if we hit another func or empty space? 
                    # Actually empty space is fine.
                    continue
            
            if is_route:
                func_defs.append({'name': func_name, 'line': i})

    # Find duplicates among routes
    seen = {}
    duplicates = []
    
    for item in func_defs:
        name = item['name']
        if name in seen:
            duplicates.append(item)
        else:
            seen[name] = item
            
    print(f"Found {len(duplicates)} duplicate route functions.")
    
    # Rename duplicates
    modified_count = 0
    for item in duplicates:
        line_idx = item['line']
        original_line = lines[line_idx]
        func_name = item['name']
        
        # Verify again
        if f"def {func_name}" in original_line:
            new_line = original_line.replace(f"def {func_name}", f"def {func_name}_v2", 1)
            lines[line_idx] = new_line
            modified_count += 1
            print(f"Renamed {func_name} at line {line_idx+1} to {func_name}_v2")
            
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print(f"Modified {modified_count} lines.")

if __name__ == "__main__":
    smart_fix()
