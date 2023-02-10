from Tokenizador import tokenizador
import re

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
    p, pf= cadena.replace('\n', ' ').replace('  ',' ').split(' '), []
    for w in p:
        if len(w)>0:
            pf+= tk.filterSymbol(w)
    return pf


def getValidationVars(variables:list):
    response = True
    if variables[0] != ',' and variables[-1] == ';':
        for v in range(0, len(variables), 2):
            if variables[v] == ',':
                response = False
            else:
                if re.search("^[a-zA-Z]", variables[v]) is None:
                    response = False
        
        for v in range(1, len(variables), 2):
            if variables[v] != ',' and variables[-1] != ';':
                response = False
    else:
        response = False
    
    return response


def getVars(variables:list):
    final_vars = []
    for v in range(0, len(variables), 2):
        final_vars.append(variables[v])

    return final_vars


def findIndices(ltc, itf):
    indices = []
    for idx, value in enumerate(ltc):
        if value == itf:
            indices.append(idx)
    return indices


def initParser(cadena:str):

    instrucciones = formato(cadena)

    try:
        if tk.getToken(instrucciones[0]).token!='STR': raise Exception
    except Exception:
        return False, 'El programa no empieza con ROBOT_R'
    
    try:
        if tk.getToken(instrucciones[1]).token!='VDEF': raise Exception
    except Exception:
        return False, 'El programa no tiene variables definidas'

    # VARS
    # Variables input
    variables_temp = []
    for w in instrucciones[2:]:
        if w == 'PROCS':
            break
        else:
            variables_temp.append(w)

    # Variables validation
    variablesLongitude = len(variables_temp)
    varsValidation = getValidationVars(variables_temp)
    if varsValidation == False:
        return False
    else:
        vars = getVars(variables_temp)


    # FUNC
    # finding the last occurrence of '['
    element = '['
    indexFinalFunction = max(index for index, item in enumerate(instrucciones) if item == element)

    # Functions dict
    functions = {}
    functions[instrucciones[(2+(variablesLongitude+1))]] = None

    functionsList = []
    for w in instrucciones[(2+(variablesLongitude+1)):indexFinalFunction]:
        functionsList.append(w)

    indicesOfEnds = findIndices(functionsList, ']')

    for i in indicesOfEnds:
        try:
            indexOfEnd = i
            nextVar = functionsList[indexOfEnd+1]
            nextStart = functionsList[indexOfEnd+2]

            if nextStart == '[':
                functions[nextVar] = None
        except:
            break

    
    # TODO INSTRUCTIONS
    for w in instrucciones[indexFinalFunction+1:]:
        try:
            parametersLength = len(tk.getToken(instrucciones[indexFinalFunction+1]).parameters)
            if parametersLength > 0:
                print(True)
        except Exception:
            return False, 'El programa no tiene variables definidas'     

    return True




def check(tipo:str):
    #['CHAR', 'NUM', 'VAR', 'FN', 'DIR', 'LOO', 'CON', 'ORI', 'FUN', 'DEL', 'KWO']
    if tipo== 'RW':
        pass
    elif tipo== 'FUNCTION':
        pass
    elif tipo== 'VAR':
        pass

print(initParser(archivo))
#print(formato(archivo))