import string

from Tokenizador import tokenizador

archivo= """
 ROBOT_r
 VARS nom , 1x , y , one ;
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
    vars={}
    fncAdded={}

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
            #Falta añadir el resto. De lo contrario se queda en un blucle infinito


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


# TODO if nxWord.category=='VAR': checkear si la variable fue definida (Me encargo yo)

def checkCategory(nxWord:tuple, actualWord:tuple, index:int):
    if nxWord.category not in actualWord.types[index]:
        return False, 'El tipo de dato no coincide con los tipos de datos permitidos'

def checkSeparator(word:tuple, separator:str ):
    if word.token != separator:
        return False, f'El separador es incorrecto. Se esperaba: "{separator}"'

def checkKW(word:tuple, generator):

    if word.token=='VDEF':
        word= generator.__next__()
        while  word.token!= 'STMFIN':
            if word.token[0] not in string.ascii_letters: raise Exception(False, "Nombre de variable inválido!")
            tk.updateVar(name=word.token ,type= (), category='VAR')

            word= generator.__next__()
            if word.token== 'COMMA': word= generator.__next__()
            elif word.token != 'STMFIN': raise Exception( False, f'Error en el separador en la definición de variables! "{word.token}"')

    elif word.category == 'PDEF':
        return True






print(initParser(archivo))
#print(formato(archivo))