import os
import sys


if len(sys.argv) != 4:
    print('Usage: python3 normalize.py <inp_sr> <out_sr> <data>')
    sys.exit(1)

# Get params
input_sr = sys.argv[1]
output_sr = sys.argv[2]
data = sys.argv[3]

if int(input_sr) < int(output_sr):
    print(f"{sys.argv[0]}: Warning: input_sr shouldn't be lower than output_sr as Nyquist theorem")
    input('Press Enter to continue or Ctrl+C to abort action...')

if os.path.isdir(data):
    for f in os.listdir(data):
        out_dir = 'out'
        os.makedirs(os.path.join(data, out_dir), exist_ok=True)
        if f.endswith('.wav'):
            os.system(f'sox -r {input_sr} {os.path.join(data, f)} -r {output_sr} {os.path.join(data, out_dir, f)}')
elif os.path.isfile(data):
    out_dir = 'out'
    os.system(f'sox -r {input_sr} {data} -r {output_sr} {os.path.join(out_dir, data)}')

print(f"{sys.argv[0]}: Done")
