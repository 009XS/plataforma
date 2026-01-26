import re

def fix_collisions():
    # Read duplicates list
    duplicates = {}
    current_func = None
    with open('duplicates.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Function:'):
                current_func = line.split(': ')[1]
            elif line.startswith('- Line'):
                line_num = int(line.split(' ')[2])
                if current_func:
                    if current_func not in duplicates:
                        duplicates[current_func] = []
                    duplicates[current_func].append(line_num)

    # We want to rename the LAST occurrence (or all except first).
    # Based on duplicates.txt, the lines are sorted? Let's assume so.
    
    lines_to_modify = {}
    for func, line_nums in duplicates.items():
        if len(line_nums) > 1:
            # Sort line numbers just in case
            line_nums.sort()
            # Rename all except the first one
            for ln in line_nums[1:]:
                lines_to_modify[ln] = func

    print(f"Plan to rename {len(lines_to_modify)} functions.")

    # Read app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_lines = f.readlines()

    # Apply changes
    modified_count = 0
    for ln, func in lines_to_modify.items():
        # line numbers are 1-based, list is 0-based
        idx = ln - 1
        original_line = app_lines[idx]
        
        # Verify
        # Regex to match 'def func(' or 'def func ('
        pattern = re.compile(rf'^\s*def\s+{func}\s*\(')
        if pattern.match(original_line):
            # Rename to func_v2
            new_line = original_line.replace(f'def {func}', f'def {func}_v2', 1)
            app_lines[idx] = new_line
            modified_count += 1
            print(f"Renamed {func} at line {ln} to {func}_v2")
        else:
            print(f"Warning: Line {ln} does not match expected function definition for {func}. Content: {original_line.strip()}")

    # Write back
    with open('app.py', 'w', encoding='utf-8') as f:
        f.writelines(app_lines)
    
    print(f"Successfully modified {modified_count} lines.")

if __name__ == "__main__":
    fix_collisions()
