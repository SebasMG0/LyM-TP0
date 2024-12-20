import string
from collections import namedtuple


class tokenizador():

    def __init__(self):
        self.f = namedtuple("function", 'types category')
        self.dt = namedtuple("datatype", 'token category')
        self.cond = namedtuple("conditional", 'structure category')
        self.word = namedtuple('word', 'word category')

        self.userVars={'var' : set(),
                       'proc': set()}

        self.lang = {
            # separator= ';'
            'jump': self.f( 
                            types=(( 'VAR', 'VAR'),), 
                            category='COMMAND'),

            'walk': self.f(
                            types=( ('VAR', 'DIR'),
                                    ('VAR', 'ORI'),
                                    ('VAR',)),
                            category='COMMAND'),

            'leap': self.f(
                            types=( ('VAR'),
                                    ('VAR','DIR'),
                                    ('VAR', 'ORI')),
                            category='COMMAND'),

            'turn': self.f( types=(('ORI',), #SPECIAL
                                   ('DIR',)),
                            category='COMMAND'),

            'turnto': self.f( types=(('ORI',),),
                              category='COMMAND'),

            'drop': self.f(types=(('VAR',),), 
                           category='COMMAND'),

            'get': self.f(types=( ('VAR',),),
                          category='COMMAND'),

            'letgo': self.f(types=(('VAR',),), 
                            category='COMMAND'),

            'nop': self.f(types=(), category='COMMAND'),

            # Conditionals and loops: delimiter= ':', separator= ','
            'if': self.cond(structure=('CONDITION', 'IF', 'BLOCK', 'ELSE', 'BLOCK'), category='CONDITIONAL'),
            'while': self.cond(structure=('CONDITION', 'BLOCK'), category='LOOP'),
            'else': self.dt(token='else', category='KW'),

            # Caso especial
            'repeat': self.f(types=(('VAR', 'BLOCK')), category='REPEAT'), 
            'times': self.dt(token='TIMES', category='KW'),

            # Conditions: delimiter= ':', separator= ','
            'facing': self.f(types=('DIR'), category='CONDITION'),
            'can': self.f(types=('COMMAND'), category='CONDITION'), #SPECIAL CASE
            'not': self.f( types=('CONDITION'), category='CONDITION'),

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
            ';': self.dt(token='STMFIN', category='SYM'),
            '=': self.dt(token='ASI', category='SYM'),
            ':': self.dt(token='COLON', category='SYM'),
            ',': self.dt(token='COMMA', category='SYM'),
            'defvar': self.dt(token='VDEF', category='KW'),
            'defproc': self.dt(token='PDEF', category='KW'),
            '{': self.dt(token='LBR', category='SYM'),
            '}': self.dt(token='RBR', category='SYM'),
            '(': self.dt(token='LPAR', category='SYM'),
            ')': self.dt(token='RPAR', category='SYM')
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
                if str.isdigit(word): return self.word(word= word, category= "VAR")
                if str.isdigit(word[0]): raise Exception (False, f"El nombre de la variable es incorrecto: {word}")
                return self.word( word= word, category="VAR")
                
    def addVar(self, word):
        self.userVars['var'].add(word)

    def addProc(self, key:str, counter:int ):
        if counter== 0: self.lang[key]= self.f((), 'COMMAND')
        else: self.lang[key]= self.f( (('VAR',)*counter,)  , 'COMMAND')

    def isVarDefined(self, word):
        return word.word in self.userVars['var']
    
    def isProcDefined(self, word):
        return word.word in self.lang