import string
from collections import namedtuple


class tokenizador():

    def __init__(self):
        self.f = namedtuple("function", 'types category')
        self.dt = namedtuple("datatype", 'token category')
        self.cond = namedtuple("conditional", 'structure category')
        self.vars= namedtuple('vars', 'token types category')
        # TODO Hay que especificar cuando se hace un bloque y un llamado a un procedimiento

        # Instructions: It can be a command, control structure or procedure call
        self.userVars={}

        self.lang = {
            # Commands: delimiter= ':' , separator= ','
            'jump': self.f( 
                            types=(( 'VAR', 'VAR')), 
                            category='COMMAND'),

            'walk': self.f(
                            types=( ('VAR', 'DIR'),
                                    ('VAR', 'ORI'),
                                    ('VAR')),
                            category='COMMAND'),

            'leap': self.f(
                            types=( ('VAR'),
                                    ('VAR','DIR'),
                                    ('VAR', 'ORI')),
                            category='COMMAND'),

            'turn': self.f( types=(('ORI') #SPECIAL
                                   ('DIR')),
                            category='COMMAND'),

            'turnto': self.f( types=(('ORI')),
                              category='COMMAND'),

            'drop': self.f(types=(('VAR')), 
                           category='COMMAND'),

            'get': self.f(types=( ('VAR')),
                          category='COMMAND'),

            'letgo': self.f(types=(('VAR')), 
                            category='COMMAND'),

            'nop': self.f(parameters=(), types=(), category='COMMAND'),

            # Conditionals and loops: delimiter= ':', separator= ','
            'if': self.cond(structure=('CONDITION', 'THEN', 'BLOCK', 'ELSE', 'BLOCK'), category='CONDITIONAL'),
            'while': self.cond(structure=('CONDITION', 'DO', 'BLOCK'), category='LOOP'),
            'repeattimes': self.f(parameters=('n', 'block'), types=(('NUM', 'VAR'), ('BLOCK')), category='REPEAT'),
            # Caso especial

            # Conditions: delimiter= ':', separator= ','
            'facing': self.f(parameters=('O'), types=(('DIR')), category='CONDITION'),
            'canput': self.f(parameters=('n', 'X'), types=(('NUM', 'VAR', 'NTD'), ('BALL', 'CHIP')), category='CONDITION'),
            'canpick': self.f(parameters=('n', 'X'), types=(('NUM', 'VAR', 'NTD'), ('BALL', 'CHIP')), category='CONDITION'),
            'canmoveindir': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR', 'NTD'), ('DIR')), category='CONDITION'),
            'canjumpindir': self.f(parameters=('n', 'D'), types=(('NUM', 'VAR', 'NTD'), ('DIR')), category='CONDITION'),
            'canmovetothe': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR', 'NTD'), ('ORI')), category='CONDITION'),
            'canjumptothe': self.f(parameters=('n', 'O'), types=(('NUM', 'VAR', 'NTD'), ('ORI')), category='CONDITION'),
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
            'defVar': self.dt(token='VDEF', category='KW'),
            'defProc': self.dt(token='PDEF', category='KW'),
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
            return self.lang[word.lower()]
        except KeyError:
            try:
                return self.userVars[word]
            except KeyError:
                self.userVars[word]=self.vars(token=word, types=(), category='NTD')
                return self.userVars[word]

    def updateVar(self, name:str, type:str, category:str):
        self.userVars

