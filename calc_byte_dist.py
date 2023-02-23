
# Calculate byte distribution of input folder
# loop through all files under input foler recursively
# and then count how many times each bytes (0x00 ~ 0xff) appears
# 
# usage:
# python3 calc_byte_dist.py /path/to/folder/
# 
# dependencies:
# Python version >= 3.8
# numpy, pandas


from pathlib import Path
import numpy as np
import pandas as pd
from sys import argv


# prepare
root = None
if len(argv) == 2:
    root = Path(argv[1])
else:
    root = Path(input('Enter folder path below:\n'))

files = [f for f in root.rglob('*') if f.is_file()]
print(f'reading file: {root.resolve()}')
print(f'{len(files) = }')


def countBytes(file) -> int:
    with open(file, 'rb') as fd:
        data = fd.read()

    output = [0 for _ in range(256)]
    for d in data:
        output[d] += 1

    return output


result = pd.DataFrame({
    'sum':[0 for _ in range(256)],
    'percentage':[0 for _ in range(256)]
})

# counting
for i,f in enumerate(files):
    print(f'{i+1}/{len(files)}, filename={f.name}')
    cb = pd.Series(countBytes(f))
    result['sum'] += cb

# calculate percentage
colsum = result['sum'].sum()
result['percentage'] = np.round(result['sum'] / colsum * 100, 2)

# print result
print('\n\nresults:')
print(result.to_string())
print('\n\n3 largest:')
print(result.nlargest(3, 'sum'))
print('\n\n3 smallest:')
print(result.nsmallest(3, 'sum'))


