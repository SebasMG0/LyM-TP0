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
vars, funtions= {}, {}

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

            if actualWord == 'COMMAND':
                checkSeparator(generator.__next__(), 'COLON')
                actualWord=checkCommand()
            #Falta añadir el resto. De lo contrario se queda en un blucle infinito
            actualWord=generator.__next__()

    except StopIteration:
        return True


def checkCommand(actualWord:tuple,  word, generator):
    for i in range(len(actualWord.parameters) - 1):
        checkCategory( nxWord=word.__next__(), actualWord=actualWord, index=i)
        checkSeparator(generator= generator, separator= 'COMMA')

    checkCategory(nxWord=word.__next__(), actualWord=actualWord, index=len(actualWord.parameters)-1)
    checkSeparator(generator=generator, separator='STMFIN')
    return word.__next__()


# TODO if nxWord.category=='VAR': checkear si la variable fue definida (Me encargo yo)

def checkCategory(nxWord:tuple, actualWord:tuple, index:int):
    if nxWord.category not in actualWord.types()[index]:
        return False, 'El tipo de dato no coincide con los tipos de datos permitidos'

def checkSeparator(generator, separator:str ):
    if generator.__next__().token != separator:
        return False, f'El separador es incorrecto. Se esperaba: "{separator}"'




print(initParser(archivo))
#print(formato(archivo))