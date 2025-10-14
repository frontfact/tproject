import sys
import re
import shutil, os
from pathlib import Path
from typing import List, TypeVar

PathLike = TypeVar("PathLike", str, Path, None)


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
StepToken = Token('Step ', 'Step ', 1, True)
ToToken = Token('To ', 'To ', 1, True)


def load_tokens(path):
    tokens = []
    lines = Path(path).read_text(encoding='utf-8').split('\n')
    for line in lines:
        if line.startswith('#'):
            continue
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
            line = line.rstrip()
            if ':' in line:
                k, v = line.split(':', 1)
                self.header[k.strip()] = v.strip()
            elif line:
                self.header[line] = ''
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

    def write(self, fout):
        # write header
        fout.write(f'%Header Record\n')
        fout.write(f'Format:{self.header["Format"]}\n')
        fout.write(f'Communication SW:{self.header["Communication SW"]}\n')
        fout.write(f'Data Type:{self.header["Data Type"]}\n')
        fout.write(f'Capacity:{self.capacity}\n')
        fout.write(f'File Name:{self.header["File Name"]}\n')
        fout.write(f'Group Name:{self.header["Group Name"]}\n')
        fout.write(f'Password:{self.header["Password"]}\n')
        fout.write(f'Option1:{self.header["Option1"]}\n')
        fout.write(f'Option2:{self.header["Option2"]}\n')
        fout.write(f'Option3:{self.header["Option3"]}\n')
        fout.write(f'Option4:{self.header["Option4"]}\n')
        # write data
        fout.write(f'%Data Record\n')
        for token in self.tokens:
            # backslash in front of listed tokens
            if token.listed:
                fout.write('\\')
            fout.write(token.src)
        fout.write('\n')
        fout.write(f'%End\n')

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

    @property
    def capacity(self) -> int:
        cap = 0
        for token in self.tokens:
            cap += token.size
        return 3 + cap


class CatFile(object):
    def __init__(self, filepath):
        self.programs: List[Program] = []
        self.filepath: Path = Path(filepath)
        if Path(filepath).exists():
            self.parse(Path(filepath).read_text(encoding='utf-8'))

    def parse(self, text):
        lines = text.splitlines()
        self.programs = []
        i = 0
        while i < len(lines):
            header = []
            data = []
            # read header
            if lines[i].startswith('%Header Record'):
                i += 1
                while i < len(lines) and not lines[i].startswith('%Data Record'):
                    header.append(lines[i])
                    i += 1
            # read data
            if i < len(lines) and lines[i].startswith('%Data Record'):
                i += 1
                while i < len(lines) and not lines[i].startswith('%End'):
                    data.append(lines[i])
                    i += 1
                # append program
                self.programs.append(Program(header, data))
            else:
                i += 1

    def write(self):
        CatFile.Write(self, self.filepath)

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
            pcap = program.capacity
            hcap = int(program.header["Capacity"])
            print(f'{program.name:8} : {pcap} / {hcap} ({pcap-hcap})')
            continue
            if program.name == 'TNT17':
                print(program.pretty_print())
                cntrs = {}
                sizes = {}
                for t in program.tokens:
                    # if not t.listed:
                    #     continue
                    # if t.size <= 1:
                    #     continue
                    if t.src in cntrs.keys():
                        cntrs[t.src] += 1
                    else:
                        cntrs[t.src] = 1
                        sizes[t.src] = t.size
                for t, c in cntrs.items():
                    if c==1:
                        print(f'\t{t},{sizes[t]} : {c}')


    def dump_programs(self, outputpath: PathLike):
        # create output directory
        CatFile.DumpPrograms(self, outputpath, False)
    
    def sort_programs(self):
        # human couting
        def sort_key(program):
            match = re.match(r'(.*?)(\d+)$', program.name)
            if match:
                prefix, number = match.groups()
                return (prefix, int(number))
            else:
                return (program.name, 0)
        self.programs = sorted(self.programs, key=sort_key)

    def find(self, progname: str):
        for program in self.programs:
            if program.name==progname:
                return program
        return None

    @classmethod
    def DumpPrograms(cls, catfile, outputpath: PathLike, clean: bool):
        outputpath = Path(outputpath)
        if clean:
            shutil.rmtree(outputpath, ignore_errors=True)
            os.makedirs(outputpath)
        # dump programs
        for program in catfile.programs:
            filepath = outputpath / program.name
            with open(str(filepath), mode='w', encoding='utf-8') as fout:
                contents = program.pretty_print()
                fout.write(contents)

    @classmethod
    def Write(cls, catfile, filepath: PathLike):
        with open(str(filepath), mode='w', encoding='utf-8') as fout:
            for program in catfile.programs:
                program.write(fout)

    def forge_token_programs(self):
        header_lines = [
            f'Format:TXT\n',
            f'Communication SW:0\n',
            f'Data Type:PG\n',
            f'Capacity:foobar\n',
            f'File Name:foobar\n',
            f'Group Name:\n',
            f'Password:\n',
            f'Option1:NL\n',
            f'Option2:\n',
            f'Option3:\n',
            f'Option4:\n'
        ]
        for i, token in enumerate(language_tokens):
            h = list(header_lines)
            h[4] = f'File Name:TOKEN{i:03}\n'
            program = Program(h, [])
            # cat encoding error
            if (token == StepToken) or (token == ToToken):
                program.tokens = [SpaceToken, token]
            else:
                program.tokens = [token]
            self.programs.append(program)
        CatFile.Write(self, 'tokens.cat')


def main():
    if len(sys.argv) < 2:
        print("Usage: python decaterizr.py <file.cat>")
        sys.exit(1)
    filepath = sys.argv[1]
    if True:
        cat = CatFile(filepath)
        cat.check_capacity()
        cat.dump_programs('../src')
    else:
        cat = CatFile('nonexisting.cat')
        cat.forge_token_programs()
    if True:
        cat.sort_programs()
        tproject = cat.find('TPROJECT')
        if tproject is not None:
            cat.programs.remove(tproject)
            cat.programs.insert(0, tproject)
        cat.dump_programs('../src')
        cat.write()


if __name__ == "__main__":
    main()
