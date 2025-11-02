import json

with open('main.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f'Total cells: {len(cells)}')

# Find cells with execution_count 41 and 42
for i, c in enumerate(cells):
    exec_count = c.get('execution_count', None)
    if exec_count in [39, 40, 41, 42, 43]:
        cell_type = c.get('cell_type', 'unknown')
        source_preview = ''.join(c.get('source', []))[:100].replace('\n', ' ')
        print(f'Cell index {i}: exec_count={exec_count}, type={cell_type}')
        print(f'  Preview: {source_preview}...')

