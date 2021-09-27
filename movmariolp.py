import re

'''
compilador
———————–
lista    : lista de strings
expr     : lista de objeto tipo match
imprimir : Booleano
......
————————
Abre el archivo errores, recorre la lista "lista", 
comparando con las expresiones regulares de la lista.
Comprueba los parentesis y el orden de interpretación.
Compara string por string hasta encontrar un un match = None.
Despues de guardar los errores en el archivo, retorna una lista 
con los string validos y una lista con las match ordenados.
'''
def compilador(lista,expr,imprimir):
    if imprimir:
        archivo_errores = open('errores.txt', 'w')
    valuefinal=True
    lista_nueva=[]
    lista_expr=[]
    #Recorremos linea por linea
    for linea in range(1,len(lista)):
        list_expr_temp=[[]]
        #Por defecto, la linea no tiene errores
        valuelinea=True
        i=0
        contador= 0
        #Recorremos la linea por expresión
        while (i<len(lista[linea])) and (valuelinea):
            valuesharp = False
            #Condiciones por si hay paréntesis
            if contador<0:
                valuelinea=False
            elif lista[linea][i] == "(":
                contador+=1
                while len(list_expr_temp)<=contador:
                    list_expr_temp.append([])
                i+=1
                valuesharp = True
            elif lista[linea][i] == ")":
                contador-=1
                i+=1
                valuesharp = True
            #Vemos si las expresiones hacen match
            else:
                for e in expr:
                    E = re.compile(r'^'+e)
                    value = E.search(lista[linea][i:])
                    if (value != None) and (valuesharp==False):
                        list_expr_temp[contador].append(value)
                        valuesharp = True
                        i+=value.span()[1]
                valuelinea = valuesharp
        #Vemos si la linea tiene al menos un error
        if (valuelinea==False) or (contador!=0) :
            valuefinal=False
            if imprimir:
                archivo_errores.write(str(linea)+" "+str(lista[linea])+'\n')
        else:
            list_expr_temp.reverse()
            for l_expr in list_expr_temp:
                for expr2 in l_expr:
                    lista_expr.append(expr2)
            lista_nueva.append(lista[linea])
    #Si no hay ningun error
    if valuefinal == True:
        if imprimir:
            archivo_errores.write('No hay errores!\n')
    if imprimir:
        archivo_errores.close()
    return(lista_nueva,lista_expr)


'''
archivo
———————–
......
————————
Abre el archivo con el codigo, lo recorre y 
lo guarda en una lista de string (por lineas).
Guarda el largo de la matriz en la primera posición e la lista
Retorna la lista de strings
'''
def archivo():
    archivo = open('codigo.txt')
    lista=[]
    for linea in archivo:
        linea = linea.strip()
        lista.append(linea)
    archivo.close()
    return lista


'''
crear_matriz
———————–
lista    : lista de strings
......
————————
Creamos una matriz con listas de listas de largo n
y la inicializa completamente en 0, 
también retorna la posición inicial (0,0)
'''
def crear_matriz(lista):
    pos=[0,0]
    n=(int(lista[0]))
    matriz = [0] * n
    for i in range(n):
        matriz[i] = [0] * n    
    return [matriz,pos]


'''
expr
———————–
......
————————
Define las Expresiones Regulares y 
las retorna en una lista con ellas
'''
def expr():
    expr=[
        r'(U)(0|[1-9][0-9]*)',
        r'(D)(0|[1-9][0-9]*)',
        r'(<)(0|[1-9][0-9]*)',
        r'(>)(0|[1-9][0-9]*)',
        r'(A)',
        r'(B)',
        r'(X)((<|>|U|D)(0|[1-9][0-9]*))+',
        r'(Y)((<|>|U|D)(0|[1-9][0-9]*))+',
        r'(L)(c|e)',
        r'(R)',
        r'(Z)',
        r'(S)(c|e)'
        ]

    quest="(\?)(([U|D|<|>](0|[1-9][0-9]*))+)(\?([U|D|<|>](0|[1-9][0-9]*))+)*((X)(([U|D|<|>](0|[1-9][0-9]*))+)|(Y)(([U|D|<|>](0|[1-9][0-9]*))+)|A|B|L(c|e)|R|Z|S(c|e))"
    expr.append(quest)
    return expr


'''
U
———————–
matriz   : lista de listas
pos      : lista de enteros
numero   : entero
......
————————
Cambia la posición hacia arriba 
considerando el largo de la matriz.
'''
def U(matriz,pos,numero):
    pos[1]-=numero
    pos[1] %= len(matriz)
    return None


'''
D
———————–
matriz   : lista de listas
pos      : lista de enteros
numero   : entero
......
————————
Cambia la posición hacia abajo
considerando el largo de la matriz.
'''
def D(matriz,pos,numero):
    pos[1]+=numero
    pos[1] %= len(matriz) 
    return None


'''
IZQ
———————–
matriz   : lista de listas
pos      : lista de enteros
numero   : entero
......
————————
Cambia la posición hacia izquierda
considerando el largo de la matriz.
'''
def IZQ(matriz,pos,numero):
    pos[0]-=numero
    pos[0] %= len(matriz) 
    return None


'''
DER
———————–
matriz   : lista de listas
pos      : lista de enteros
numero   : entero
......
————————
Cambia la posición hacia derecha
considerando el largo de la matriz.
'''
def DER(matriz,pos,numero):
    pos[0]+=numero
    pos[0] %= len(matriz) 
    return None


'''
A
———————–
matriz   : lista de listas
pos      : lista de enteros
......
————————
Aumenta en uno el número donde se encuentra la posición.
'''
def A(matriz,pos):
    matriz[pos[1]][pos[0]] += 1
    return


'''
B
———————–
matriz   : lista de listas
pos      : lista de enteros
......
————————
Disminuye en uno el número donde se encuentra la posición.
'''
def B(matriz,pos):
    matriz[pos[1]][pos[0]] = (matriz[pos[1]][pos[0]])-1
    return


'''
X
———————–
matriz   : lista de listas
pos      : lista de enteros
dir      : string
......
————————
Multiplica el valor en donde se encuentra la posición por el valor indicado por dir.
'''
def X(matriz,pos,dir):
    guarda_dir = ""
    i = len(dir)
    while i>0:
        value=re.match("^(U|D|<|>)([0-9]+)",dir)
        if value.group(1) == "U":
            U(matriz,pos,int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,int(value.group(2)))
        guarda_dir = value.group() + guarda_dir
        j=value.span()[1]
        dir=dir[j:]
        i = len(dir)

    casilla = matriz[pos[1]][pos[0]]

    i=len(guarda_dir)
    while i > 0:
        value = re.search("^(U|D|<|>)([0-9]+)",guarda_dir)
        if value.group(1) == "U":
            U(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,-1*int(value.group(2)))
        j=value.span()[1]
        guarda_dir=guarda_dir[j:]
        i = len(guarda_dir)
    matriz[pos[1]][pos[0]] *= casilla
    return 


'''
Y
———————–
matriz   : lista de listas
pos      : lista de enteros
dir      : string
......
————————
Divide el valor en donde se encuentra la posición por el valor indicado por dir.
'''
def Y(matriz,pos,dir):
    guarda_dir = ""
    i = len(dir)
    while i>0:
        value=re.match("^(U|D|<|>)([0-9]+)",dir)
        if value.group(1) == "U":
            U(matriz,pos,int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,int(value.group(2)))
        guarda_dir = value.group() + guarda_dir
        j=value.span()[1]
        dir=dir[j:]
        i = len(dir)

    casilla = matriz[pos[1]][pos[0]]

    i=len(guarda_dir)
    while i > 0:
        value = re.search("^(U|D|<|>)([0-9]+)",guarda_dir)
        if value.group(1) == "U":
            U(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,-1*int(value.group(2)))
        j=value.span()[1]
        guarda_dir=guarda_dir[j:]
        i = len(guarda_dir)

    if casilla==0:
        print("Error, división por 0")
    else:
        matriz[pos[1]][pos[0]] = int((matriz[pos[1]][pos[0]])/casilla)
    return


'''
L
———————–
matriz   : lista de listas
pos      : lista de enteros
ce       : string
......
————————
Imprime el valor en donde se encuentra la possición,
en tipo chr y entero.
'''
def L(matriz,pos,ce):
    if ce == "c":
        if (32 <= (matriz[pos[1]][pos[0]]) <= 127):
            print(chr(matriz[pos[1]][pos[0]]),end="")
    else:
        print(matriz[pos[1]][pos[0]],end="")
    return 


'''
R
———————–
matriz   : lista de listas
pos      : lista de enteros
......
————————
Reinicializa el valor en donde se encuentra la posición a 0.
'''
def R(matriz,pos):
    matriz[pos[1]][pos[0]] = 0
    return


'''
Z
———————–
matriz   : lista de listas
pos      : lista de enteros
lista    : lista de strings
......
————————
Reinicializa todos los valores de la matriz a 0.
'''
def Z(matriz,pos,lista):
    for i in range(int(lista[0])):
        matriz[i] = [0] * (int(lista[0]))
    return


'''
S
———————–
matriz   : lista de listas
pos      : lista de enteros
ce       : string
......
————————
Recorre e imprime todos los valores de la matriz.
'''
def S(matriz,pos,ce):
    final=""
    for y in matriz:
        for x in y:
            if ce == "e":
                final+=str(x)
            elif ce == "c":
                if (32 <= x <= 127):
                    final+=chr(x)
    print(final)
    return


'''
Quest
———————–
matriz   : lista de listas
pos      : lista de enteros
dir      : string
comando  : string
......
————————
Se mueve a la dirección indicada, guarda el valor de esa posición, 
vuelve a donde estaba y si el valor guardado es mayor a 0, realiza el comando
'''
def Quest(matriz,pos,dir,comando):
    guarda_dir = ""
    i = len(dir)
    while i>0:
        value=re.match("^(U|D|<|>)([0-9]+)",dir)
        if value.group(1) == "U":
            U(matriz,pos,int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,int(value.group(2)))
        guarda_dir = value.group() + guarda_dir
        j=value.span()[1]
        dir=dir[j:]
        i = len(dir)
    casilla = matriz[pos[1]][pos[0]]
    i=len(guarda_dir)
    while i > 0:
        value = re.search("^(U|D|<|>)([0-9]+)",guarda_dir)
        if value.group(1) == "U":
            U(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "D":
            D(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == "<":
            IZQ(matriz,pos,-1*int(value.group(2)))
        elif value.group(1) == ">":
            DER(matriz,pos,-1*int(value.group(2)))
        j=value.span()[1]
        guarda_dir=guarda_dir[j:]
        i = len(guarda_dir)
    linea_nueva=[]
    if int(casilla) > 0:
        linea_nueva.append(str(len(matriz)))
        linea_nueva.append(comando)
        lista_nueva,lista_expr=compilador(linea_nueva,expr(),False)
        for exprr in lista_expr:
            primera_letra = exprr.group(1)
            if primera_letra=="U":
                U(matriz,pos, int(exprr.group(2)))
            elif primera_letra=="D":
                D(matriz,pos, int(exprr.group(2)))
            elif primera_letra=="<":
                IZQ(matriz,pos, int(exprr.group(2)))
            elif primera_letra==">":
                DER(matriz,pos, int(exprr.group(2)))
            elif primera_letra=="A":
                A(matriz,pos)
            elif primera_letra=="B":
                B(matriz,pos)
            elif primera_letra=="X":
                X(matriz,pos,(exprr.group()[1:]))
            elif primera_letra=="Y":
                Y(matriz,pos,(exprr.group()[1:]))
            elif primera_letra=="L":
                L(matriz,pos,(exprr.group(2)))
            elif primera_letra=="R":
                R(matriz,pos)
            elif primera_letra=="Z":
                Z(matriz,pos,lista)
            elif primera_letra=="S":
                S(matriz,pos,(exprr.group(2)))            
    return


'''
comando
———————–
matriz   : lista de listas
pos      : lista de enteros
expr     : objeto tipo match
lista    : lista de strings
......
————————
Ve la primera letra de expr y busca hasta encontrar la expresión correspondiente,
luego de eso ejecuta la función asociada.
'''
def comando(matriz,pos,expr,lista):
    primera_letra = expr.group(1)
    if primera_letra=="U":
        U(matriz,pos, int(expr.group(2)))
    elif primera_letra=="D":
        D(matriz,pos, int(expr.group(2)))
    elif primera_letra=="<":
        IZQ(matriz,pos, int(expr.group(2)))
    elif primera_letra==">":
        DER(matriz,pos, int(expr.group(2)))
    elif primera_letra=="A":
        A(matriz,pos)
    elif primera_letra=="B":
        B(matriz,pos)
    elif primera_letra=="X":
        X(matriz,pos,(expr.group()[1:]))
    elif primera_letra=="Y":
        Y(matriz,pos,(expr.group()[1:]))
    elif primera_letra=="L":
        L(matriz,pos,(expr.group(2)))
    elif primera_letra=="R":
        R(matriz,pos)
    elif primera_letra=="Z":
        Z(matriz,pos,lista)
    elif primera_letra=="S":
        S(matriz,pos,(expr.group(2)))
    return


'''
interprete
———————–
matriz     : lista de listas
pos        : lista de enteros
lista_expr : lista de objeto tipo match
......
————————
Ve si la expresión parte con ? y dependiendo de eso ejecuta la función asociada a "?"
o al comando correspondiente.
'''
def interprete(matriz,pos,lista_expr):
    for expr in lista_expr:
        if expr.group(1) != "?":
            comando(matriz,pos,expr,lista)
        elif expr.group(1) == "?":
            Quest(matriz,pos,expr.group(2),expr.group(8))
    return


lista=archivo()
lista_nueva,lista_expr=compilador(archivo(),expr(),True)
matriz,pos = crear_matriz(archivo())

interprete(matriz,pos,lista_expr)