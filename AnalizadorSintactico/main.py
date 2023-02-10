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

            if actualWord == 'VDEF':
                checkSeparator(generator.__next__(), 'VAR')

            if actualWord == 'VAR':
                checkSeparator(generator.__next__(), 'COMMA')
                #Revisar si es la ultima variable y el separador es ";"
                actualWord=checkVar()

            if actualWord == 'PDEF':
                checkSeparator(generator.__next__(), 'VAR')
                #Aca en realidad no es una variable, es una funcion
                actualWord=checkFun()

            if actualWord == 'LSB':
                #Si es el corchete de apertura de una funcion, el siguiente deberia ser el separador
                checkSeparator(generator.__next__(), 'VBAR')
                #Validar si es el corchete de apertura de una condicion, ejemplo: "do", "then"
                #En ese caso el separador deberia ser un command
                checkSeparator(generator.__next__(), 'COMMAND')

            if actualWord == 'VBAR':
                #Puede tener o no tener parametros
                checkSeparator(generator.__next__(), 'VAR')
                #Aca en realidad no es una variable, es un parametro
                actualWord=checkParam()
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
def checkVar(nxWord:tuple, actualWord:tuple, index:int):
    # TODO
    return True

def checkFun(nxWord:tuple, actualWord:tuple, index:int):
    # TODO
    return True

def checkParam(nxWord:tuple, actualWord:tuple, index:int):
    # TODO
    return True

def checkCategory(nxWord:tuple, actualWord:tuple, index:int):
    if nxWord.category not in actualWord.types()[index]:
        return False, 'El tipo de dato no coincide con los tipos de datos permitidos'

def checkSeparator(generator, separator:str ):
    if generator.__next__().token != separator:
        return False, f'El separador es incorrecto. Se esperaba: "{separator}"'




print(initParser(archivo))
#print(formato(archivo))