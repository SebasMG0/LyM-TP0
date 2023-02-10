import string
from collections import namedtuple


class tokenizador():

    def __init__(self):
        self.f = namedtuple("function", 'parameters types category')
        self.dt = namedtuple("datatype", 'token category')
        self.cond = namedtuple("conditional", 'structure category')

        # TODO Hay que especificar cuando se hace un bloque y un llamado a un procedimiento
        # Esta en el "main.py"

        # Instructions: It can be a command, control structure or procedure call
        self.lang = {
            # Commands: delimiter= ':' , separator= ','
            'assignto': self.f(parameters=('n', 'name'), types=(('NUM'), ('VAR')), category='COMMAND'),
            'goto': self.f(parameters=('x', 'y'), types=(('NUM', 'VAR'), ('NUM', 'VAR')), category='COMMAND'),
            'move': self.f(parameters=('n'), types=(('NUM', 'VAR')), category='COMMAND'),
            'turn': self.f(parameters=('D'), types=(('LFT', 'RGT', 'ARD')), category='COMMAND'), # Hay que realizar un or en la comprobación
            'face': self.f(parameters=('O'), types=(('DIR')), category='COMMAND'),
            'put': self.f(parameters=('n', 'X'), types=(('NUM', 'VAR'), ('BALL', 'CHIP')), category='COMMAND'),
            'pick': self.f(parameters=('n', 'X'), types=(('NUMBER', 'VAR'), ('BALL', 'CHIP')), category='COMMAND'),
            'movetothe': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR'), ('ORI')), category='COMMAND'),
            'moveindir': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR'), ('DIR')), category='COMMAND'),
            'jumptothe': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR'), ('ORI')), category='COMMAND'),
            'jumpindir': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR'), ('DIR')), category='COMMAND'),
            'nop': self.f(parameters=(), types=(), category='COMMAND'),

            # Conditionals and loops: delimiter= ':', separator= ','
            'if': self.cond(structure=('CONDITION', 'THEN', 'BLOCK', 'ELSE', 'BLOCK'), category='CONDITIONAL'),
            'while': self.cond(structure=('CONDITION', 'DO', 'BLOCK'), category='LOOP'),
            'repeattimes': self.f(parameters=('n', 'block'), types=(('NUM', 'VAR'), ('BLOCK')), category='REPEAT'),
            # Caso especial

            # Conditions: delimiter= ':', separator= ','
            'facing': self.f(parameters=('O'), types=(('DIR')), category='CONDITION'),
            'canput': self.f(parameters=('n', 'X'), types=(('NUM', 'VAR'), ('BALL', 'CHIP')), category='CONDITION'),
            'canpick': self.f(parameters=('n', 'X'), types=(('NUM', 'VAR'), ('BALL', 'CHIP')), category='CONDITION'),
            'canmoveindir': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR'), ('DIR')), category='CONDITION'),
            'canjumpindir': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR'), ('DIR')), category='CONDITION'),
            'canmovetothe': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR'), ('ORI')), category='CONDITION'),
            'canjumptothe': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR'), ('ORI')), category='CONDITION'),
            'not': self.f(parameters=('cond'), types=(('CONDITION')), category='CONDITION'),

            # Extra types
            'north': self.dt(token='NOR', category='DIR'),
            'west': self.dt(token='WES', category='DIR'),
            'south': self.dt(token='SOU', category='DIR'),
            'east': self.dt(token='EAS', category='DIR'),
            'around': self.dt(token='ARD', category='ORI'),
            'left': self.dt(token='LFT', category='ORI'),
            'right': self.dt(token='RGT', category='ORI'),
            'front': self.dt(token='FRT', category='ORI'),
            'back': self.dt(token='BCK', category='ORI'),
            ';': self.dt(token='STMFIN', category='SYM'),  # Statement Fin
            ':': self.dt(token='COLON', category='SYM'),
            ',': self.dt(token='COMMA', category='SYM'),
            'vars': self.dt(token='VDEF', category='KW'),
            'procs': self.dt(token='PDEF', category='KW'),
            'robot_r': self.dt(token='STR', category='KW'),
            '[': self.dt(token='LSB', category='SYM'),  # Left square bracket
            ']': self.dt(token='RSB', category='SYM'),  # Left square bracket
            '|': self.dt(token='VBAR', category='SYM')
        }

    def filterSymbol(self, word: str):
        indices, chars = [], [x for x in word]
        for i in range(len(chars)):
            if (chars[i] in self.lang.keys()):
                indices.append(i)

        if len(indices) == 0:
            return [word]
        else:
            resultado = []
            cen = 0
            for i in indices:
                if len(word[cen:i]) > 0: resultado.append(word[cen:i])
                if len(word[i]) > 0: resultado.append(word[i])
                cen = i + 1
            if len(word[cen:]) > 0: resultado.append(word[cen:])
            return resultado

    def getToken(self, word: str):
        try:
            token = self.lang[word.lower()]
        except KeyError:
            token= 'VAR'
        return token
