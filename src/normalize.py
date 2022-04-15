"""
Normalize your label file (remove unicode character such as "dấu ngã ~", "dấu huyền `", ...)
"""

import sys
from unidecode import unidecode


with open(sys.argv[1], 'r') as fp:
    with open(sys.argv[2], 'w') as fp2:
        for line in fp:
            line = unidecode(line)
            fp2.write(line)