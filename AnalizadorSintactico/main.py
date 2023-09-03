import string

from Tokenizador import tokenizador

archivo= """
        defVar nom 0
        defVar x 0
        defVar y 0
        defVar z 0
        a=2
        b = 3
        walk(2)
        """

tk = tokenizador()
vars, functions = {}, {}

def format(cadena:str):
    """
    Función para separar las palabras de la cadena
    """

    r=[]
    for i in cadena.replace('\n', ' ').replace('  ',' ').strip().split(' '):
        if len(i.strip())==0: continue
        if len(i)==1: r.append(i); continue

        li= 0
        for j, v in enumerate(i.lower()):
            if v in tk.lang:
                r.append(i[li:j]) 
                r.append(i[j])
                try: li= j+1
                except: li=0; break
        if li==0:
            r.append(i)
        elif li<= len(i)-1:
            r.append(i[li:])
    return r

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
                checkCondition(generator= generator)

            elif w.category == 'LOOP':
                checkLoop(w)

            elif w.category == 'REPEAT':
                checkRepeat(generator=generator)

            elif w.category == 'VAR':
                checkAssignment(w, generator= generator)

            else: return False, f"La palabra - {w} - no hace parte de ninguna fracción del lenguaje"

            try:
                w= next(generator)
            except:
                return True
    except Exception as e:
        raise
        if len(e.args)>0:
            return False, e.args
        return False

def checkProcedureCall(w, generator):
    word, index, params= next(generator), 0, w.types

    assert word.token == tk.lang['('].token, f"Falta '('"

    while word.token != tk.lang[')'].token:
        word= next(generator)
        params= [i for i in params if len(i)>index and i[index]==word.category and (tk.isVarDefined(word) or word.word.isdigit())]

        assert len(params)>0, f"Los parámetros no coinciden para la función {w}"

        word= next(generator)
        assert index < maxProcArgs(params), f"Hay más parámetros de los requeridos en {w}"        
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
    
    

def checkCategory(nxWord:tuple, w:tuple, index:int):
    if len(w.types)>0 and nxWord.category not in w.types[index]:
        return False, 'El tipo de dato no coincide con los tipos de datos permitidos'

def checkSeparator(word:tuple, separator:str ):
    if word.token != separator:
        return False, f'El separador es incorrecto. Se esperaba: "{separator}"'

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
    
    checkVarName(token=next(generator))

    pass

def checkConditional(generator):
    pass

def checkCondition( w: tuple, generator):
    checkSeparator(generator.__next__(), 'COLON')

    for i in range(len(w.parameters) - 1):
        if 'cond' in w.parameters:
            checkCondition(generator=generator)
            w= generator.__next__()
        else:
            checkCategory(nxWord=generator.__next__(), w=w, index=i)
            checkSeparator(word=generator.__next__(), separator='COMMA')
    checkCategory(nxWord=generator.__next__(), w=w, index=len(w.parameters) - 1)
    if generator.__next__().token not in ('STMFIN', 'COMMA'): raise Exception('Se esperaba un separador: ; o ,')

def checkLoop(generator):
    checkSeparator(word=generator.__next__(), separator='COLON')
    var= generator.__next__()
    if var.category != 'CONDITION': raise Exception ('Se esperaba una condición!')
    checkCondition(w=var, generator= generator)
    if generator.__next__().token != 'DO': raise Exception( 'Se esperaba un "DO"')
    if generator.__next__().token != 'LSB': raise Exception( 'Se esperaba un bloque: "["')
    checkBlock(generator= generator)

def checkBlock(generator):
    word = generator.__next__()
    while word.token != 'RSB':
        if word.category == 'COMMAND':
            checkProcedureCall(w=word, generator=generator)
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
    w= generator.__next__()

    for i in range(len(w.parameters) - 1):
        checkCategory(nxWord=generator.__next__(), w=w, index=i)
        checkSeparator(word=generator.__next__(), separator='COMMA')
    checkBlock(generator)

def checkVarName(word):
    if word.category != "VAR": raise Exception(  "Nombre de variable o procedimiento no válido!")
    return 




print(initParser(archivo))
# print(format(archivo))