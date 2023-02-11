import string

from Tokenizador import tokenizador

archivo= """
 ROBOT_r
 VARS nom , x , y , one ;
 PROCS
 putCB [|c,b| assignTo : 1 , one ;
 put : c , chips ; put : b , balloons ]
 goNorth [| |
 while : canMovetoThe : 1 , north do: [ moveInDir : 1 , north ]
     ]
     goWest [ | | if : canMoveInDir : 1 , west then: [ MoveInDir : 1 ,
west ] else : [ nop ] ]
     [
     goTo : 3 , 3
     putcb : 2 ,1
     ]
        """

tk = tokenizador()
vars, funtions = {}, {}

def formato(cadena:str):
    """
    Función para separar las palabras de la cadena
    :param cadena: str
    :return: pf: List
    """
    p, pf= cadena.replace('\n', ' ').replace('  ',' ').split(' '), []
    for w in p:
        if len(w)>0:
            pf+= tk.filterSymbol(w)
    return pf
def nextWord(instrucciones:list):
    for w in instrucciones[1:]:
        yield tk.getToken(w.lower())

def initParser(cadena:str):
    instrucciones= formato(cadena)

    try:
        if tk.getToken(instrucciones[0]).token!='STR': raise Exception
    except Exception:
        return False, 'El programa no empieza con ROBOT_R'

    #Recorriendo las palabras de modo controlado utilizando un generador
    generator = nextWord(instrucciones)
    actualWord = generator.__next__()

    try:

        while (actualWord):
            if actualWord.category == 'COMMAND':
                actualWord=checkCommand(actualWord=actualWord, generator= generator )

            elif actualWord.category == 'KW':
                checkKW(word= actualWord, generator= generator)

            elif actualWord.category == 'CONDITIONAL':
                checkConditional(generator= generator)

            elif actualWord.category == 'CONDITION':
                checkCondition(generator=generator)

            elif actualWord.category == 'LOOP':
                checkLoop(generator)
            elif actualWord.category == 'REPEAT':
                checkRepeat(generator=generator)

            actualWord=generator.__next__()

    except StopIteration:
        return True

    except Exception as e:
        return e


def checkCommand(actualWord:tuple, generator):
    checkSeparator(generator.__next__(), 'COLON')
    if len(actualWord.parameters)==0: return
    for i in range(len(actualWord.parameters) - 1):
        checkCategory( nxWord=generator.__next__(), actualWord=actualWord, index=i)
        checkSeparator(word= generator.__next__(), separator= 'COMMA')
    checkCategory(nxWord=generator.__next__(), actualWord=actualWord, index=len(actualWord.parameters)-1)
    checkSeparator(word=generator.__next__(), separator='STMFIN')


def checkCategory(nxWord:tuple, actualWord:tuple, index:int):
    if len(actualWord.types)>0 and nxWord.category not in actualWord.types[index]:
        return False, 'El tipo de dato no coincide con los tipos de datos permitidos'

def checkSeparator(word:tuple, separator:str ):
    if word.token != separator:
        return False, f'El separador es incorrecto. Se esperaba: "{separator}"'

def checkKW(word:tuple, generator):

    if word.token=='VDEF':
        checkVarDef(word=word, generator= generator)

    elif word.category == 'PDEF':
        checkProcDef(word=word, generator=generator)


def checkVarDef(word:tuple, generator):
    word = generator.__next__()
    while word.token != 'STMFIN':
        if word.token[0] not in string.ascii_letters: raise Exception(False, "Nombre de variable inválido!")
        tk.updateVar(name=word.token, type=(), category='VAR')

        word = generator.__next__()
        if word.token == 'COMMA':
            word = generator.__next__()
        elif word.token != 'STMFIN':
            raise Exception(False, f'Error en el separador en la definición de variables! "{word.token}"')

def checkProcDef(word:tuple, generator):
    word= generator.__next__()

    if word.category=='VAR':
        if word.token[0] not in string.ascii_letters: raise Exception(False, "Nombre de procedimiento inválido!")
        tk.updateVar(name=word.token, type=(), category='PROC')

        checkSeparator(word=generator.__next__(), separator='LSB')
        checkSeparator(word=generator.__next__(), separator='VBAR')

        word= generator.__next__()
        while word.token!='VBAR':
            checkVarName(word)

            word = generator.__next__()
            if word.token == 'COMMA':
                word = generator.__next__()
            elif word.token != 'VBAR':
                raise Exception(False, f'Error en el separador en la definición de variables! "{word.token}"')
            word= generator.__next__()

        checkBlock(generator=generator)

    else:
        raise Exception(False, "Falta el nombre del método!")

def checkConditional(generator):
    pass

def checkCondition( actualWord: tuple, generator):
    checkSeparator(generator.__next__(), 'COLON')

    for i in range(len(actualWord.parameters) - 1):
        if 'cond' in actualWord.parameters:
            checkCondition(generator=generator)
            actualWord= generator.__next__()
        else:
            checkCategory(nxWord=generator.__next__(), actualWord=actualWord, index=i)
            checkSeparator(word=generator.__next__(), separator='COMMA')
    checkCategory(nxWord=generator.__next__(), actualWord=actualWord, index=len(actualWord.parameters) - 1)
    if generator.__next__().token not in ('STMFIN', 'COMMA'): raise Exception(False,'Se esperaba un separador: ; o ,')

def checkLoop(generator):
    checkSeparator(word=generator.__next__(), separator='COLON')
    var= generator.__next__()
    if var.category != 'CONDITION': raise Exception (False,'Se esperaba una condición!')
    checkCondition(actualWord=var, generator= generator)
    if generator.__next__().token != 'DO': raise Exception(False, 'Se esperaba un "DO"')
    if generator.__next__().token != 'LSB': raise Exception(False, 'Se esperaba un bloque: "["')
    checkBlock(generator= generator)

def checkBlock(generator):
    word = generator.__next__()
    while word.token != 'RSB':
        if word.category == 'COMMAND':
            checkCommand(actualWord=word, generator=generator)
        elif word.category == 'CONDITIONAL':
            checkConditional(generator=generator)
        elif word.category == 'LOOP':
            checkLoop(generator=generator)
        elif word.category == 'REPEAT':
            checkRepeat(generator)
        elif word.category == 'LSB':
            checkBlock(generator)
        word = generator.__next__()

def checkRepeat(generator):
    checkSeparator(generator.__next__(), 'COLON')
    actualWord= generator.__next__()

    for i in range(len(actualWord.parameters) - 1):
        checkCategory(nxWord=generator.__next__(), actualWord=actualWord, index=i)
        checkSeparator(word=generator.__next__(), separator='COMMA')
    checkBlock(generator)

def checkVarName(word:tuple ):
    if word.token[0] not in string.ascii_letters: raise Exception(False, "Nombre de variable inválido!")
    tk.updateVar(name=word.token, type=(), category='PROC')





print(initParser(archivo))
#print(formato(archivo))