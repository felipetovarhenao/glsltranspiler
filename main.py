from transpiler import GLTranspiler
from argparse import ArgumentParser
import os
import sys


parser = ArgumentParser('GLSL to ShaderToy transpiler', f'{os.path.basename(
    sys.executable)} main.py -i <input_file> -o <output_file>')
parser.add_argument('-i', '--input', help='input path', type=str, required=True)
parser.add_argument('-o', '--output', help='output path', type=str, required=True)
args = parser.parse_args()

t = GLTranspiler()
t.to_shadertoy(input_file=args.input, output_file=args.output)
