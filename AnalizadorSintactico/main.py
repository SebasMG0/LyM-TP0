import string

from Tokenizador import tokenizador

tk = tokenizador()
vars, functions = {}, {}

def format(cadena:str):
    """
    Función para separar las palabras de la cadena
    """
    p, pf= cadena.replace('\n', ' ').replace('  ',' ').split(' '), []
    for w in p:
        if len(w)>0:
            pf+= tk.filterSymbol(w)
    return pf

def nextWord(instructions:list):
    for w in instructions:
        yield tk.getToken(w.lower())

def initParser(cadena:str):
    instructions= format(cadena)

    #Recorriendo las palabras de modo controlado utilizando un generador   
    generator= nextWord(instructions)
    w = next(generator)
    try:
        while (w):
            if w.category == 'COMMAND':
                checkProcedureCall(w=w, generator= generator )

            elif w.category == 'KW':
                checkKW(word= w, generator= generator)

            elif w.category == 'CONDITIONAL':
                checkConditional(generator= generator)

            elif w.category == 'CONDITION':
                checkCondition(w, generator= generator)

            elif w.category == 'LOOP':
                checkLoop(w)

            elif w.category == 'REPEAT':
                checkRepeat(generator=generator)

            elif w.category == 'VAR':
                checkAssignment(w, generator= generator)
            
            elif w.token== tk.getToken("{").token:
                checkBlock(generator)

            else: return False, f"La palabra - {w} - no hace parte de ninguna fracción del lenguaje"

            try:
                w= next(generator)
            except:
                return True
    except Exception as e:
        if len(e.args)>0:
            return (False, e.args)
        return False

def checkProcedureCall(w, generator):
    if w== tk.getToken("nop"): lPar(generator=generator); rPar(generator=generator); return
    word, index, params= next(generator), 0, w.types

    assert word.token == tk.lang['('].token, f"Falta '('"

    while word.token != tk.lang[')'].token:
        word= next(generator)
        
        if word.category== 'VAR':
            assert tk.isVarDefined(word) or word.word.isdigit(), "Se está usando una variable no definida"

        params= [i for i in params if len(i)>index and i[index]==word.category]

        assert len(params)>0, f"Los parámetros no coinciden para la función {w}"
        assert index < maxProcArgs(params), f"Hay más parámetros de los requeridos en {w}"        

        word= next(generator)

        index+=1

def maxProcArgs(params:list):
    m=0
    for i in params:
        if len(i)>m:
            m= len(i)
    return m

def checkAssignment(w: tuple, generator):
    aw= next(generator)
    if aw.token== tk.lang['='].token:
        checkVarName(word= w)
        assert next(generator).category in ('VAR', 'NUM'), f"Definición de variable no válida {w}"
        tk.addVar(w.word)
    else: 
        assert tk.isProcDefined(w), f'Intenta llamar a un procedimiento no definido -- {w} --'
        checkProcedureCall(generator)

def checkKW(word:tuple, generator):

    if word.token== tk.lang['defvar'].token:
        checkVarDef(generator= generator)

    elif word.token == tk.lang['defproc'].token:
        checkProcDef(generator=generator)

def checkVarDef(generator):

    """
        Comprueba que las variables sean definidas correctamente
    """
    name= next(generator)
    checkVarName(name)

    w= next(generator)
    if w.category not in ('VAR', 'NUM'): 
        raise Exception( "False, El valor de una variable no es un número ni otra variable previamente definida")
    if tk.isProcDefined(w): 
        raise Exception((False, f"False, No se puede usar el nombre de un método en la definición de variables: {w}"))
    tk.addVar(name[0])

def checkProcDef(generator):

    """
        Comprueba que los procedimientos hayan sido declarados correctamente
    """
    name= next(generator)
    checkVarName(word=name)
    lPar(generator)

    word= next(generator)
    counter, localVars= 0, []
    while word != tk.getToken(")"):
        counter+=1
        if not tk.isVarDefined(word):
            localVars.append(word.word) 
            tk.addVar(word.word)

        word= next(generator) 
       
        if word== tk.getToken(","):
            word= next(generator)
            assert word!= tk.getToken(")")

    assert next(generator)== tk.getToken("{")

    tk.addProc(key=name.word, counter=counter)

    checkBlock(generator=generator)

    for w in localVars:
         tk.userVars['var'].discard(w)

def checkConditional(generator):
    word= next(generator)
    assert word.category == 'CONDITION', "Se esperaba una condición en un condicional"
    checkCondition(word, generator)

    word= next(generator)
    assert word.token == tk.getToken("{").token 
    checkBlock(generator)

    assert next(generator).token== tk.getToken("else").token, "Falta 'else' en un condicional"
    assert next(generator).token == tk.getToken("{").token, "Falta '{' en un condicional"
    checkBlock(generator)


def checkCondition(w: tuple, generator):
    if w== tk.getToken("not"):
        assert next(generator).token == tk.getToken(':').token
        checkCondition(next(generator), generator)
    elif w== tk.getToken("facing"):
        lPar(generator)
        assert next(generator).category==w.types, f"El tipo de dato no es el correcto para la condición 'facing'"
        rPar(generator)
    elif w== tk.getToken("can"):
        lPar(generator)
        word= next(generator)
        if word.category == 'COMMAND': checkProcedureCall(word, generator)
        else: checkAssignment(word, generator)
        rPar(generator)

    else:
        raise Exception(f"Condición no reconocida")
        
def lPar(generator):
    assert next(generator).token==tk.getToken("(").token

def rPar(generator):
    assert next(generator).token==tk.getToken(")").token

def checkLoop(generator):
    w= next(generator)
    assert w.category=='CONDITION', "Error en bucle while: se esperaba una condición"
    checkCondition(w, generator=generator)

    assert next(generator).token== tk.getToken("{").token
    checkBlock(generator=generator)


def checkBlock(generator):
    word = next(generator)

    while word != tk.getToken("}"):
        if word.category == 'COMMAND':
            checkProcedureCall(w=word, generator=generator)
        elif word.category == 'CONDITIONAL':
            checkConditional(generator=generator)
        elif word.category == 'CONDITION':
            checkCondition(generator=generator)
        elif word.category == 'LOOP':
            checkLoop(generator=generator)
        elif word.category == 'REPEAT':
            checkRepeat(generator)
        elif word.category == 'VAR':
            if not tk.isVarDefined(word) and not word.word.isdigit():
                checkAssignment(word, generator)
        
        word= next(generator)
        if word == tk.getToken(";"):
            word= next(generator)
            assert word!= tk.getToken("}")
            

def checkRepeat(generator):
    w= next(generator)
    assert w.word.isdigit() or tk.isVarDefined(w)
    assert next(generator) == tk.getToken('times') 
    assert next(generator) == tk.getToken('{')
    checkBlock(generator) 

def checkVarName(word):
    if word.category != "VAR": raise Exception(  "Nombre de variable o procedimiento no válido!")
    return 

def openFile(file:str="code.txt"):
    with open(file) as f:
        print(initParser(f.read().replace("\t",' ')))
    

if __name__ == '__main__':
    openFile(file="code.txt")