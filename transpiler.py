import re
import os


class GLTranspiler:

    def to_shadertoy(self, input_file: str, output_file: str):
        lines = self.__resolve_include(os.path.abspath(input_file))
        code = self.__replace_multiple_line_breaks("".join(lines))
        code = self.__remove_precision_def(code)
        with open(output_file, 'w') as f:
            f.write(code)

    def __remove_precision_def(self, input_string: str):
        def condition_function(s: str):
            return "GL_ES" in s
        lines = input_string.split('\n')
        result_lines = []
        inside_ifdef = False

        for line in lines:
            if line.strip().startswith("#ifdef"):
                inside_ifdef = condition_function(line.strip()[7:])
                if inside_ifdef:
                    continue
            elif line.strip().startswith("#endif"):
                inside_ifdef = False
                continue

            if not inside_ifdef:
                result_lines.append(line)

        return '\n'.join(result_lines)

    def __get_include_path(self, include_statement):
        pattern = r'#include "(.*)"'
        match = re.match(pattern, include_statement)
        if match:
            return match.group(1)
        else:
            return None

    def __replace_multiple_line_breaks(self, input_string):
        return re.sub(r'\n(\n)+', '\n\n', input_string)

    def __replace_main(self, line: str):
        return line.replace("void main()", "void mainImage(out vec4 fragColor, in vec2 fragCoord)")

    def __declares_builtin_uniforms(self, line: str):
        if "uniform" not in line:
            return False
        lower = line.lower()
        for u in ["resolution", "time"]:
            if u in lower:
                return True

    def __replace_gl_prefix(self, line: str):
        def replace_match(match):
            s = match.group(0)[3:]
            return s[0].lower() + s[1:]

        return re.sub(r'\bgl_[a-zA-Z0-9_]+\b', replace_match, line)

    def __replace_uniforms(self, line: str):
        def replace_match(match):
            return 'i' + match.group(0)[2:].capitalize()

        return re.sub(r'\bu_[a-zA-Z0-9_]+\b', replace_match, line)

    def __resolve_include(self, file: str):
        with open(file, 'r') as f:
            lines = f.readlines()
        resolved_lines = []
        for line in lines:
            if self.__declares_builtin_uniforms(line):
                continue
            if not line.startswith("#include"):
                line = self.__replace_main(line)
                line = self.__replace_uniforms(line)
                line = self.__replace_gl_prefix(line)
                resolved_lines.append(line)
                continue
            rel_path = self.__get_include_path(line)
            if not rel_path:
                raise SyntaxError(f"Import seems to have syntax errors: {line}")
            base_dir = os.path.dirname(file)
            path = os.path.join(base_dir, rel_path)
            resolved_lines.extend([*self.__resolve_include(path), "\n\n"])
        return resolved_lines
