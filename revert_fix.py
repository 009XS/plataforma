import re

def revert_changes():
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex to find 'def name_v2(' and replace with 'def name('
    # Be careful not to match things that naturally end in _v2, but assuming none did before.
    # The previous script did `def {func}_v2`.
    
    # I can iterate over duplicates.txt again to know exactly what was renamed.
    duplicates = {}
    current_func = None
    with open('duplicates.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Function:'):
                current_func = line.split(': ')[1]
            elif line.startswith('- Line'):
                # We just need the names
                duplicates[current_func] = True
                
    modified_count = 0
    pattern = re.compile(r'def ([a-zA-Z0-9_]+)_v2\s*\(')
    
    def replacer(match):
        nonlocal modified_count
        name = match.group(1)
        if name in duplicates:
            modified_count += 1
            return f"def {name}("
        return match.group(0)

    new_content = pattern.sub(replacer, content)
    
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print(f"Reverted {modified_count} functions.")

if __name__ == "__main__":
    revert_changes()
