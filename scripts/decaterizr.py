import argparse
import copy
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
YenToken = Token('@5C', '¥', 1, True)
EsperluetteToken = Token('@26', '&', 1, True)


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
    def __init__(self, header_lines, data, ctype='G65'):
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
        if self.ctype == 'G100':
            fout.write(f'%Header Record\n')
            fout.write(f'Format:MCS1\n')
            fout.write(f'Type Number:1\n')
            fout.write(f'File Name:{self.name}\n')
            fout.write(f'Option Name:\n')
            fout.write(f'Communication SW:0\n')
            fout.write(f'Capacity:{self.capacity}\n')
            fout.write(f'Data Type:PG\n')
        else:
            fout.write(f'%Header Record\n')
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
        fout.write(f'%Data Record\n')
        if '100' in self.ctype:
            fout.write(f'Password:\n')
            fout.write(f'BaseN:0\n')
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

    def simplify(self):
        subst = {
            Token('@7FD1','z',2,True): Token('z','z',1, False),
            Token('@7FD2','p',2,True): Token('p','p',1,False),
            Token('(-)','-',1,True): Token('-','-',1,False),
            Token('or','or',1,True): [Token('o','o',1,False), Token('r','r',1,False)],
            Token('Re','e',2,True): Token('e','e',1,False),
            Token('Ra','a',1,True): Token('a','a',1,False),
            Token('E','E',1,True): Token('E','E',1,False),
            Token('milli','m',1,True): Token('m','m',1,False),
            Token('Cnt','n',1,True): Token('n','n',1,False),
        }
        for i, token in enumerate(self.tokens):
            alt = subst.get(token)
            if alt is not None:
                if isinstance(alt, list):
                    del self.tokens[i]
                    self.tokens[i:i] = alt
                else:
                    self.tokens[i] = alt
    
    def make_mono(self):
        for i in range(len(self.tokens)-1, -1, -1):
            token = self.tokens[i]
            if token==YenToken:
                self.tokens[i] = EsperluetteToken
            if token==GreenToken or token==OrangeToken:
                del self.tokens[i]

    def find_used_vars(self):
        operators = ['+', '-', '→', '⇒', '=', '≠', '≥', '≤', '>', '<', 'Not ', ' Or ', ' And ']
        operands = list()
        for i, token in enumerate(self.tokens):
            if token.dst in operators:
                if i>0:
                    operands.append(self.tokens[i-1])
                if i<len(self.tokens)-1:
                    operands.append(self.tokens[i+1])
        vars = set()
        for operand in operands:
            if len(operand.dst)>1:
                continue
            if re.match('[A-Z]|r|θ', operand.dst):
                vars.add(operand.dst)
        vars = sorted(list(vars))
        return vars



class CatFile(object):
    def __init__(self, filepath, ctype=None):
        self.programs: List[Program] = []
        self.filepath: Path = Path(filepath)
        self.ctype = 'G65'
        if 'G100' in filepath:
            self.ctype = 'G100'
        if ctype is not None:
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
                if '100' in self.ctype:
                    i+= 3
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
        with open("used.txt", 'w', encoding='utf-8') as f:
            for token in language_tokens:
                if token in programs_tokens:
                    f.write(f'{token.src};{token.dst};{token.size}\n')
                    
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
        if '100' in self.ctype:
            outputpath += "/G100"
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

    def sort(self):
        self.sort_programs()
        def set_program_index(name, index):
            program = self.find(name)
            if program is not None:
                self.programs.remove(program)
                self.programs.insert(index, program)
        set_program_index('TPROJECT', 0)
        set_program_index('T0', len(self.programs))

    def find(self, progname: str):
        for program in self.programs:
            if program.name==progname:
                return program
        return None

    def simplify(self):
        for program in self.programs:
            program.simplify()
        self.useless_tokens()

    def make_mono(self, ctype):
        for program in self.programs:
            program.make_mono()
        # T0(65) = 300/s
        # T0(35+) = 833/s
        # T0(100+) = 190/s
        t0 = self.find('T0')
        if '35+' in ctype:
            t0.tokens[0] = Token('8','8',1,False)
            t0.tokens[1] = Token('3','3',1,False)
            t0.tokens[2] = Token('3','3',1,False)
        if '65' in ctype:
            t0.tokens[0] = Token('3','3',1,False)
            t0.tokens[1] = Token('0','0',1,False)
            t0.tokens[2] = Token('0','0',1,False)
        if '100+' in ctype:
            t0.tokens[0] = Token('1','1',1,False)
            t0.tokens[1] = Token('9','9',1,False)
            t0.tokens[2] = Token('0','0',1,False)

    @classmethod
    def DumpPrograms(cls, catfile, outputpath: PathLike, clean: bool):
        outputpath = Path(outputpath)
        if clean:
            shutil.rmtree(outputpath, ignore_errors=True)
        # dump programs
        os.makedirs(outputpath, exist_ok=True)
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

    catfile = CatFile(args.filepath)

    if args.simplify:
        catfile.simplify()

    if args.sort:
        catfile.sort()

    if args.dump:
        catfile.dump_programs('../src')

    if args.overwrite:
        catfile.write()

    if args.make_mono:
        cat35 = copy.deepcopy(catfile)
        cat35.make_mono('35+')
        cat35.Write(cat35, '../packages/TPROJECT35.cat')
        cat35.dump_programs('../src/mono35+')
        cat100 = copy.deepcopy(catfile)
        cat100.make_mono('100+')
        cat100.Write(cat100, '../packages/TPROJECT100.cat')
        cat100.dump_programs('../src/mono100+')

    if args.forge:
        dummy = CatFile('non-existing.cat')
        dummy.forge_token_programs()

    if args.analyze:
        catfile.analyze()


if __name__ == "__main__":
    main()
