tokens={"MOVE":1,
        "ROTATE":1,
        "RIGHT":1,
        "LEFT":1,
        "LOOK":2,
        "DROP":1,
        "FREE":1,
        "PICK":1,
        "CHECK":3,
        "BLOCKEDP":4,
        "NOP":5,
        "BLOCK":6,
        "REPEAT":7,
        "IF":8,
        "DEFINE":9,
        "TO":10,
        "(":11,
        ")":12,
        "[":13,
        "]":14,
}
tokens_list=[]
lista_variables=["B","C"]

   
def leerComandos(lineas,linea,index,linea_index):
    if len(linea)!=0:
        if index==(len(lineas)-1):
            leerComando(lineas,linea,index,linea_index)
        else:
            leerComando(lineas,linea,index,linea_index)
            linea=lineas[index+1]
            leerComandos(lineas,linea,index+1,linea_index)

def leerComando(lineas,linea,index,linea_index):
    category=0
    lista=remove(linea)
    print(lista)
    
    if lista[0] in tokens:
        category=tokens[lista[0]]
        if category==1:
            return verificarValor(lista[1],lista_variables)
        elif category==2:
            return verificarLook(lista[1])
        elif category==3:
            return verificarCheck(lista[1],lista[2])
    else:
        return False

def verificarLook(direccion):
    if direccion=="N" or direccion=="S" or direccion=="E" or direccion=="W":
        return True
def verificarCheck(elemento,variable):
    if elemento=="C" or elemento =="B":
        return verificarValor(variable)
    else:
        return False
    
def verificarValor(elemento): 
    if elemento.isnumeric():
        return True
    else:
        for i in lista_variables:
            if i==elemento:
                return True
        return False


def remove(chain):
    lista=chain.split(" ")
    i=0
    while(i<len(lista)):
        
        if lista[i]!='':
            if (('('  in lista[i]) or (")"  in lista[i]) or ("["  in lista[i]) or ("]"  in lista[i]) or "\n" in lista[i]) :
                if "\n" in lista[i]:
                    print("something")
                var=""
                x=0
                while x < len(lista[i]):
                    temp2=0
                    if (lista[i][x]=="(") or (lista[i][x]==")") or (lista[i][x]=="[") or lista[i][x]=="]" or lista[i][x]=="\n":
                        
                            
                        if var!="":
                            tokens_list.append(var)
                            var=""
                        tokens_list.append(lista[i][x])
    
                        

                        
                    else:
                        var+=lista[i][x]
                    
                    if x==len(lista[i])-1:
                        if var!="":
                            tokens_list.append(var)
                    x+=1
            else:
                tokens_list.append(lista[i])
        i+=1
    i=0
   

    

def tokenize(lineas):
    for linea in lineas:
        print(linea)
        remove(linea)



def cargar_datos():
    archivo= open("code.txt", "r", encoding= "UTF-8-sig")
    
    lineas=archivo.readlines()
    tokenize(lineas)
    print(tokens_list)
    """
    linea_index=0
    leerComandos(lineas,linea,i,linea_index)
    archivo.close()
    """
cargar_datos()