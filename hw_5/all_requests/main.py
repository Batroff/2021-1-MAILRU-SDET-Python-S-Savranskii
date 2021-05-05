from sys import argv
from json import dumps

with open('../access.log', 'r') as f:
    lines_quantity = sum(1 for line in f)

with open('./res.log', 'w+') as f:
    f.write(f'{lines_quantity}')
    
    f.write('\n')
    if '--json' in argv:
        f.write(f'JSON: {dumps({"lines_quantity": lines_quantity})}')

