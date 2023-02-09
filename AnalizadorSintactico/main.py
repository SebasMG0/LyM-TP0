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
    p, pf= cadena.replace('\n', ' ').replace('  ',' ').split(' '), []
    for w in p:
        if len(w)>0:
            pf+= tk.filterSymbol(w)
    return pf

def initParser(cadena:str):
    vars={}
    fncAdded={}

    instrucciones= formato(cadena)

    try:
        if tk.getToken(instrucciones[0]).token!='STR': raise Exception
    except Exception:
        return False, 'El programa no empieza con ROBOT_R'

    for w in instrucciones[1:]:
        token= tk.getToken(w.lower())[1]

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