import sys
import re
import shutil, os
from pathlib import Path


class Token:
    def __init__(self, src: str, dst: str, size: int, listed: bool):
        self.src = src
        self.dst = dst
        self.size = size
        self.listed = listed

    def __str__(self):
        return self.dst
    
    def __eq__(self, other):
        return self.src == other.src


SpaceToken = Token(' ', ' ', 1, False)
LineFeedToken = Token('\n', '\n', 1, False)
DispToken = Token('Disp', '◢', 1, True)


def load_tokens(path):
    tokens = []
    lines = Path(path).read_text(encoding='utf-8').split('\n')
    for line in lines:
        parts = line.split(';')
        if not parts[0]:
            continue
        src = parts[0]
        dst = parts[1] if len(parts) > 1 and parts[1] else src
        size = int(parts[2]) if len(parts) > 2 and parts[2] else 1
        tokens.append(Token(src, dst, size, True))
    return tokens


language_tokens = load_tokens("tokens.txt")


class ParserError(Exception):
    pass


class AsciiParser:
    def __init__(self, known_tokens):
        self.known_tokens = sorted(known_tokens, key=lambda t: len(t.src), reverse=True)

    def parse_line(self, line):
        tokens = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\':
                i += 1 # consume '\'
                for token in self.known_tokens:
                    if line.startswith(token.src, i):
                        tokens.append(token)
                        i += len(token.src)
                        break
                else:
                    raise ParserError(f"Unknown token : '{line[i:]}'")
            elif not c.isspace():
                tokens.append(Token(str(c), str(c), 1, False))
                i += 1
            else:
                tokens.append(SpaceToken)
                i += 1
        return tokens
        

class Program:
    def __init__(self, header_lines, data):
        self.header = {}
        for line in header_lines:
            if ':' in line:
                k, v = line.split(':', 1)
                self.header[k.strip()] = v.strip()
            elif line.strip():
                self.header[line.strip()] = ''
        self.data = data
        self.tokens = self.parse_tokens()
        
    def print_header(self):
        for k,v in self.header.items():
            print(f'{k} = {v}')
    
    @property
    def name(self) -> str:
        return self.header['File Name']

    def parse_tokens(self) -> list:
        program_tokens = []
        parser = AsciiParser(language_tokens)
        for i, line in enumerate(self.data):
            line_tokens = parser.parse_line(line)
            if i<(len(self.data)-1):
                line_tokens.append(LineFeedToken)
            program_tokens.extend(line_tokens)
        return program_tokens

    def pretty_print(self, indent='  ') -> str:
        output: str = ''
        inc = {'For ', 'Do', 'While ', 'Then '}
        dec = {'Next', 'IfEnd', 'WhileEnd', 'LpWhile '}
        level = 0
        first = True
        for t in self.tokens:
            if t == LineFeedToken:
                output += str(t)
                first = True
                continue
            if t == DispToken:
                output += f'{t}\n'
                first = True
                continue
            if t.dst == 'Else ':
                level = max(level - 1, 0)
                output += (indent * level + str(t) + '\n')
                level += 1
                first = True
                continue
            if t.dst in dec:
                level = max(level - 1, 0)
            line = (indent * level + str(t)) if first else str(t)
            output += line
            first = False
            if t.dst in inc:
                level += 1
                if t.dst=='Then ':
                    output += '\n'
                    first = True
        return output

    def capacity(self):
        cap = 0
        for token in self.tokens:
            cap += token.size
        return cap + 3


class CatFile:
    def __init__(self, path):
        self.programs = []
        self.path = path
        self._parse(Path(path).read_text(encoding='utf-8'))

    def _parse(self, text):
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            if lines[i].strip().startswith('%Header Record'):
                i += 1
                header = []
                while i < len(lines) and not lines[i].strip().startswith('%Data Record'):
                    header.append(lines[i]); i += 1
                if i < len(lines) and lines[i].strip().startswith('%Data Record'): i += 1
                data = []
                while i < len(lines) and not lines[i].strip().startswith('%End'):
                    data.append(lines[i]); i += 1
                self.programs.append(Program(header, data))
            else:
                i += 1

    def useless_tokens(self):
        programs_tokens = set()
        for program in self.programs:
            ptokens = program.raw_tokens()
            programs_tokens.update(ptokens)
        with open("used.txt", 'w') as f:
            for token, dest, size in language_tokens:
                if dest in programs_tokens:
                    f.write(f'{token};{dest};{size}\n')
                    
    def check_capacity(self):
        for program in self.programs:
            pcap = program.capacity()
            hcap = int(program.header["Capacity"])
            print(f'{program.name:8} : {pcap} / {hcap} ({pcap-hcap})')
            # if program.name=='TNT2':
            #     print(program.pretty_print())
            #     cntrs = {}
            #     sizes = {}
            #     for t in program.tokens:
            #         if not t.listed:
            #             continue
            #         if t.src in cntrs.keys():
            #             cntrs[t.src] += 1
            #         else:
            #             cntrs[t.src] = 1
            #             sizes[t.src] = t.size
            #     for t, c in cntrs.items():
            #         print(f'\t{t},{sizes[t]} : {c}')

    def dump(self):
        # create output directory
        catname = Path(self.path).stem
        path = Path(f'./tmp/{catname}')
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
        # dump programs
        for program in self.programs:
            filepath = path / program.name
            with open(str(filepath), mode='w', encoding='utf-8') as fout:
                contents = program.pretty_print()
                fout.write(contents)

def main():
    if len(sys.argv) < 2:
        print("Usage: python decaterizr.py <file.cat>")
        sys.exit(1)
    path = sys.argv[1]
    cat = CatFile(path)
    #cat.check_capacity()
    cat.dump()


if __name__ == "__main__":
    main()
