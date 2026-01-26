import re
from collections import Counter

def find_duplicate_functions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    func_pattern = re.compile(r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(')
    
    definitions = []
    for i, line in enumerate(lines):
        match = func_pattern.match(line)
        if match:
            func_name = match.group(1)
            definitions.append((func_name, i + 1))

    counts = Counter(name for name, _ in definitions)
    duplicates = [name for name, count in counts.items() if count > 1]

    if duplicates:
        print(f"Found {len(duplicates)} duplicate functions:")
        for name in duplicates:
            print(f"\nFunction: {name}")
            for func_name, line_num in definitions:
                if func_name == name:
                    print(f"  - Line {line_num}")
    else:
        print("No duplicate functions found.")

if __name__ == "__main__":
    find_duplicate_functions('d:\\learning_platform\\app.py')
