# GLSL to ShaderToy fragment transpiler


### Description
This is a simple python utility for transpiling GLSL fragments into [ShaderToy](https://www.shadertoy.com/)-compatible ones. This includes resolving nested dependencies imported with the `#include` macro.

### Usage
In the terminal, run:
```zsh
python3 main.py -i <input_file> -o <output_file>
```