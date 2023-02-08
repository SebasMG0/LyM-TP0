import string
from collections import namedtuple

class tokenizador():

    def __init__(self):
        self.dataTypes = ['CHAR', 'NUM', 'VAR', 'FN', 'DIR', 'LOO', 'CON', 'ORI', 'FUN', 'DEL', 'KWO', 'BCK']
        self.f= namedtuple("function",'parameters types')
        self.dt= namedtuple("datatype", 'token type')

        letters = {x: self.dataTypes[0] for x in string.ascii_lowercase}
        numbers = {x: self.dataTypes[1] for x in range(0, 10)}
        #Como sugerencia para añadir en el dt: delimiter
        #TODO Hay que especificar cuando se hace un bloque
        self.alphabet={'north':self.dt('NOR', self.dataTypes[4]),
            'west': self.dt('WES', self.dataTypes[4]),
            'south': self.dt('SOU', self.dataTypes[4]),
            'east': self.dt('EAS', self.dataTypes[4]),
            'around': self.dt('ARD', self.dataTypes[7]),
            'left': self.dt('LFT', self.dataTypes[7]),
            'right': self.dt('RGT', self.dataTypes[7]),
            'front': self.dt('FRT', self.dataTypes[7]),
            'back': self.dt('BCK', self.dataTypes[7]),
            'while': self.dt('WLO', self.dataTypes[5]), #While loop,
            'do': self.dt('DO', self.dataTypes[5]),
            'then': self.dt('THEN', self.dataTypes[5]),
            'if': self.dt('IF', self.dataTypes[5]),
            'else': self.dt('ELSE', self.dataTypes[5]),
            'repeat': self.dt('REPEAT', self.dataTypes[5]),
            ';': self.dt('STMFIN', self.dataTypes[9]),  # Statement Fin
            ':': self.dt('COLON', self.dataTypes[9]),
            ',': self.dt('COMMA', self.dataTypes[9]),
            'vars': self.dt('VDEF', self.dataTypes[10]),
            'procs': self.dt('PDEF', self.dataTypes[10]),
            'robot_r': self.dt('STR', self.dataTypes[10]),
            '[': self.dt('LSB', self.dataTypes[9]),  # Left square bracket
            ']': self.dt('RSB', self.dataTypes[9]),  # Left square bracket
            '|': self.dt('VBAR', self.dataTypes[9])
            }

        self.functions={'assignto': self.f( parameters=('n', 'name'), types=(('NUM'),('VAR'))),
               'goto': self.f( parameters=('x','y'), types=(('NUM', 'VAR'), ('NUM', 'VAR'))),
               'move': self.f( parameters=('n'), types=(('NUM', 'VAR'))),
               'turn': self.f( parameters=('D'), types=(('LFT', 'RGT', 'ARD'))),
               'face': self.f( parameters=('O'), types=(('NOR', 'SOU', 'EAS', 'WES'))),
               'put': self.f( parameters=('n', 'X'), types=(('NUM', 'VAR'), ('BALL', 'CHIP'))),
               'pick': self.f( parameters=('n', 'X'), types=(('NUMBER', 'VAR'), ('BALL', 'CHIP'))),
               'movetothe': self.f( parameters=('n', 'D'), types=(('NUM', 'VAR'), ('FRT', 'LFT', 'RGT', 'BCK'))),
               'moveindir': self.f( parameters=('n', 'O'), types=(('NUM', 'VAR'), ('NOR', 'SOU', 'WES', 'EAS'))),
               'jumptothe': self.f( parameters=('n','D'), types=(('NUM', 'VAR'), ('FRT', 'RGT', 'LFT', 'BCK'))),
               'jumpindir': self.f( parameters=('n', 'O'), types=(('NUM', 'VAR'), ('NOR', 'SOU', 'WES', 'EAS'))),
               'nop': self.f( parameters=(), types=())
               }


    def filterSymbol(self, word:str):
        indices, chars= [], [x for x in word]
        for i in range(len(chars)):
            if (chars[i] in self.alphabet.keys()):
                indices.append(i)

        if len(indices)==0:
            return [word]
        else:
            resultado=[]
            cen= 0
            for i in indices:
                if len(word[cen:i])>0: resultado.append(word[cen:i])
                if len(word[i])>0: resultado.append(word[i])
                cen= i+1
            if len(word[cen:])>0: resultado.append(word[cen:])
            return resultado

    def getToken(self, char:str):
        try:
            token= self.alphabet[char], 'RW' #Reserved
        except KeyError:
            try:
                token= self.functions[char], 'FUNC' #Function
            except KeyError:
                token= 'VAR'
        return token