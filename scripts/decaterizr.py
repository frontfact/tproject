import argparse
import copy
import re
import shutil
import os
import sys
from pathlib import Path
from typing import List, TypeVar


PathLike = TypeVar("PathLike", str, Path, None)
GRAPH35 = 'G35'
GRAPH65 = 'G65'
GRAPH100 = 'G100'


class Token:
    def __init__(self, src: str, dst: str, size: int, listed: bool):
        self.src = src
        self.dst = dst
        self.size = size
        self.listed = listed

    def __str__(self):
        return self.dst

    def __eq__(self, other):
        return isinstance(other, Token) and self.src == other.src

    def __hash__(self):
        return hash(self.src)


SpaceToken = Token(' ', ' ', 1, False)
LineFeedToken = Token('\n', '\n', 1, False)
DispToken = Token('Disp', '◢', 1, True)
StepToken = Token('Step ', 'Step ', 1, True)
ToToken = Token('To ', 'To ', 1, True)
GreenToken = Token('Green ', 'Green ', 2, True)
OrangeToken = Token('Orange ', 'Orange ', 2, True)
BlueToken = Token('Blue ', 'Blue ', 2, True)
YenToken = Token('@5C', '¥', 1, True)
YToken = Token('Y', 'Y', 1, False)
TextToken = Token('Text ', 'Text ', 2, True)
nToken = Token('n', 'n', 1, False)
nRecrToken = Token('R n', 'n', 2, True)


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
        self.known_tokens = sorted(known_tokens,
                                   key=lambda t: len(t.src),
                                   reverse=True)

    def parse_line(self, line):
        tokens = []
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\':
                i += 1  # consume '\'
                for token in self.known_tokens:
                    if line.startswith(token.src, i):
                        tokens.append(token)
                        i += len(token.src)
                        break
                else:
                    raise ParserError(f"Unknown token : '{line[i:]}' @ line \"{line}\"")
            elif not c.isspace():
                tokens.append(Token(str(c), str(c), 1, False))
                i += 1
            else:
                tokens.append(SpaceToken)
                i += 1
        return tokens


class Program:
    def __init__(self, header_lines, data, ctype):
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
        self.ctype = ctype

    def print_header(self):
        for k, v in self.header.items():
            print(f'{k} = {v}')

    @property
    def name(self) -> str:
        return self.header['File Name']

    def parse_tokens(self) -> list:
        program_tokens = []
        parser = AsciiParser(language_tokens)
        for i, line in enumerate(self.data):
            line_tokens = parser.parse_line(line)
            if i < (len(self.data) - 1):
                line_tokens.append(LineFeedToken)
            program_tokens.extend(line_tokens)
        return program_tokens

    def write(self, fout):
        # write header
        fout.write('%Header Record\n')
        fout.write(f'Format:{self.header["Format"]}\n')
        fout.write(f'Communication SW:{self.header["Communication SW"]}\n')
        fout.write(f'Data Type:{self.header["Data Type"]}\n')
        fout.write(f'Capacity:{self.capacity}\n')
        fout.write(f'File Name:{self.name}\n')
        fout.write(f'Group Name:{self.header["Group Name"]}\n')
        fout.write(f'Password:{self.header["Password"]}\n')
        fout.write(f'Option1:{self.header["Option1"]}\n')
        fout.write(f'Option2:{self.header["Option2"]}\n')
        fout.write(f'Option3:{self.header["Option3"]}\n')
        fout.write(f'Option4:{self.header["Option4"]}\n')
        # write data
        fout.write('%Data Record\n')
        for token in self.tokens:
            # backslash in front of listed tokens
            if token.listed:
                fout.write('\\')
            fout.write(token.src)
        fout.write('\n')
        fout.write('%End\n')

    def pretty_print(self, indent='  ') -> str:
        output: str = ''
        inc = {'For ', 'Do', 'While ', 'Then '}
        dec = {'Next', 'IfEnd', 'WhileEnd', 'LpWhile '}
        level = 0
        first = True
        ntokens = len(self.tokens)
        for i, t in enumerate(self.tokens):
            if t == LineFeedToken:
                output += str(t)
                first = True
                continue
            if t == DispToken:
                output += f'{t}\n'
                first = True
                continue
            if t.dst == 'Else ':
                level -= 1
                output += (indent * level + str(t) + '\n')
                level += 1
                first = True
                continue
            if t.dst in dec:
                level -= 1
            line = (indent * level + str(t)) if first else str(t)
            output += line
            first = False
            if t.dst in inc:
                level += 1
                if t.dst == 'Then ':
                    output += '\n'
                    first = True
            else:
                if (t.dst == ']') and (i+1 < ntokens) and (self.tokens[i+1].dst == '['):
                    output += '\n'
                    first = True
        if level != 0:
            print(f'Indentation level error in {self.name}', file=sys.stderr)
        return output

    @property
    def capacity(self) -> int:
        cap = 0
        for token in self.tokens:
            cap += token.size
        return 3 + cap

    def simplify(self):
        subst = {
            Token('@7FD1', 'z', 2, True): Token('z', 'z', 1, False),
            Token('@7FD2', 'p', 2, True): Token('p', 'p', 1, False),
            Token('(-)', '-', 1, True): Token('-', '-', 1, False),
            Token('or', 'or', 1, True): [Token('o', 'o', 1, False),
                                         Token('r', 'r', 1, False)],
            Token('Re', 'e', 2, True): Token('e', 'e', 1, False),
            Token('Ra', 'a', 1, True): Token('a', 'a', 1, False),
            Token('E', 'E', 1, True): Token('E', 'E', 1, False),
            Token('milli', 'm', 1, True): Token('m', 'm', 1, False),
            Token('Cnt', 'n', 1, True): Token('n', 'n', 1, False),
        }
        for i, token in enumerate(self.tokens):
            alt = subst.get(token)
            if alt is not None:
                if isinstance(alt, list):
                    del self.tokens[i]
                    self.tokens[i:i] = alt
                else:
                    self.tokens[i] = alt

    def make_mono(self, ctype: str):
        self.ctype = ctype
        Text_seen_since_last_linefeed = False
        for i, token in enumerate(self.tokens):
            # '¥' not rendered with `Text` on G35/G100, replace by 'Y'
            if token == YenToken:
                self.tokens[i] = YToken
            if ctype == GRAPH100:
                if token == LineFeedToken:
                    Text_seen_since_last_linefeed = False
                if token == TextToken:
                    Text_seen_since_last_linefeed = True
                # regular 'n' is too wide on G100, use alternative 'n'
                if (token == nToken) and Text_seen_since_last_linefeed:
                    self.tokens[i] = nRecrToken

    def find_used_vars(self):
        operators = ['+', '-', '→', '⇒', '=', '≠', '≥', '≤', '>', '<', 'Not ',
                     ' Or ', ' And ']
        operands = list()
        for i, token in enumerate(self.tokens):
            if token.dst in operators:
                if i > 0:
                    operands.append(self.tokens[i-1])
                if i < len(self.tokens)-1:
                    operands.append(self.tokens[i+1])
        vars = set()
        for operand in operands:
            if len(operand.dst) > 1:
                continue
            if re.match('[A-Z]|r|θ', operand.dst):
                vars.add(operand.dst)
        vars = sorted(list(vars))
        return vars


class CatFile(object):
    def __init__(self, filepath, ctype):
        self.programs: List[Program] = []
        self.filepath: Path = Path(filepath)
        self.ctype = ctype
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
                if self.ctype == GRAPH100:
                    i += 3
                else:
                    i += 1
                while i < len(lines) and not lines[i].startswith('%End'):
                    data.append(lines[i])
                    i += 1
                # append program
                self.programs.append(Program(header, data, self.ctype))
            else:
                i += 1

    def write(self):
        CatFile.Write(self, self.filepath)

    def useless_tokens(self):
        programs_tokens = set()
        for program in self.programs:
            programs_tokens.update(program.tokens)
        with open("used.txt", 'w', encoding='utf-8', newline='\n') as f:
            for token in language_tokens:
                if token in programs_tokens:
                    f.write(f'{token.src};{token.dst};{token.size}\n')

    def dump_programs(self, outputpath: PathLike):
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
            if program.name == progname:
                return program
        return None

    def simplify(self):
        for program in self.programs:
            program.simplify()
        self.useless_tokens()

    def make_mono(self, ctype: str):
        self.ctype = ctype
        for program in self.programs:
            program.make_mono(ctype)
        # T0(65) = 300/s
        # T0(35+) = 833/s
        # T0(100+) = 190/s
        tnt2 = self.find('Z02')
        if ctype == GRAPH35:
            tnt2.tokens[0] = Token('8', '8', 1, False)
            tnt2.tokens[1] = Token('3', '3', 1, False)
            tnt2.tokens[2] = Token('3', '3', 1, False)
        if ctype == GRAPH65:
            tnt2.tokens[0] = Token('3', '3', 1, False)
            tnt2.tokens[1] = Token('0', '0', 1, False)
            tnt2.tokens[2] = Token('0', '0', 1, False)
        if ctype == GRAPH100:
            tnt2.tokens[0] = Token('2', '2', 1, False)
            tnt2.tokens[1] = Token('4', '4', 1, False)
            tnt2.tokens[2] = Token('0', '0', 1, False)

    @classmethod
    def DumpPrograms(cls, catfile, outputpath: PathLike, clean: bool):
        outputpath = Path(outputpath)
        if clean:
            shutil.rmtree(outputpath, ignore_errors=True)
        # dump programs
        os.makedirs(outputpath, exist_ok=True)
        for program in catfile.programs:
            filepath = outputpath / f'{program.name}.cbas'
            with open(str(filepath), mode='w', encoding='utf-8', newline='\n') as fout:
                contents = program.pretty_print()
                fout.write(contents)

    @classmethod
    def Write(cls, catfile, filepath: PathLike):
        with open(str(filepath), mode='w', encoding='utf-8') as fout:
            current_size = 0
            for program in catfile.programs:
                program.write(fout)
                current_size += program.capacity
            initial_size = 47498
            second_pict_price = 4096
            mat_y_savings = 720-240
            to_save = second_pict_price
            to_save -= mat_y_savings
            diff = initial_size - current_size
            progress = 100. * diff / to_save
            print(f'{Path(filepath).stem} : {current_size} (target: {progress:3.1f}%, {diff-to_save} extra bytes)')

    def forge_token_programs(self):
        header_lines = [
            'Format:TXT\n',
            'Communication SW:0\n',
            'Data Type:PG\n',
            'Capacity:foobar\n',
            'File Name:foobar\n',
            'Group Name:\n',
            'Password:\n',
            'Option1:NL\n',
            'Option2:\n',
            'Option3:\n',
            'Option4:\n'
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

    def analyze(self):
        for prog in self.programs:
            vars = prog.find_used_vars()
            print(f'{prog.name} : {vars}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('filepath')
    p.add_argument('--sort', '-s', action='store_true')
    p.add_argument('--forge', action='store_true')
    p.add_argument('--dump', '-d', action='store_true')
    p.add_argument('--overwrite', '-o', action='store_true')
    p.add_argument('--simplify', action='store_true')
    p.add_argument('--make_mono', action='store_true')
    p.add_argument('--analyze', action='store_true')
    args = p.parse_args()

    catfile = CatFile(args.filepath, GRAPH65)

    if args.simplify:
        catfile.simplify()

    if args.sort:
        catfile.sort_programs()

    if args.dump:
        catfile.dump_programs('../src')

    if args.overwrite:
        catfile.write()

    if args.make_mono:
        cat35 = copy.deepcopy(catfile)
        cat35.make_mono(GRAPH35)
        cat35.Write(cat35, '../packages/TPROJECT35.CAT')
        #  cat35.dump_programs('../src/mono35+')
        cat100 = copy.deepcopy(catfile)
        cat100.make_mono(GRAPH100)
        cat100.Write(cat100, '../packages/TPROJECT100.CAT')
        #  cat100.dump_programs('../src/mono100+')

    if args.forge:
        dummy = CatFile('non-existing.cat', GRAPH65)
        dummy.forge_token_programs()

    if args.analyze:
        catfile.analyze()


if __name__ == "__main__":
    main()
