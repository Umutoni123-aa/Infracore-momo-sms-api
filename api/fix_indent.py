# Read original file
with open('routes.py', 'r') as f:
    content = f.read()

# Split into lines
lines = content.split('\n')

# Fixed lines
fixed = []
in_function = False

for line in lines:
    # Check if it's a function definition
    if line.strip().startswith('def '):
        fixed.append(line)
        in_function = True
    # Check if we've exited the function (global code)
    elif in_function and line and not line.startswith(' ') and not line.startswith('\t'):
        in_function = False
        fixed.append(line)
    # Inside function - add indentation
    elif in_function and line.strip():
        if not line.startswith('    '):
            fixed.append('    ' + line.strip())
        else:
            fixed.append(line)
    # Empty lines or outside function
    else:
        fixed.append(line)

# Write fixed file
with open('routes.py', 'w') as f:
    f.write('\n'.join(fixed))

print("✓ File fixed!")
