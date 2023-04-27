# Integrantes: Agustin Lizarraga, Valentino Gil, Sebastian Limardo de Casas
# Grupo: 9
# Martes Tarde

import random

def crear_manual(manual):
    #Manual que contiene las reglas del juego.
    try:
        archivo = open("Manual_De_Reglas_Reversi.txt","wt")
        archivo.write(manual)
        print("Creado el archivo: Manual_De_Reglas_Reversi.txt")
    except OSError as mensaje:
        print("No se pudo grabar correctamente el archivo", mensaje)
    finally:
        try:
            archivo.close()
        except NameError:
            pass

def elegir_ficha():
    conjunto = {"X","O"}
    print("\n_____________________________________\n")
    print("          Eleccion de ficha")
    print("_____________________________________\n")
    print("--------------------------------------------------------------------\n")
    ficha = input("Que ficha queres ser? (X, O, RANDOM): ")
    ficha = ficha.upper()
    while ficha != "X" and ficha != "O" and ficha != "RANDOM":
        ficha = input("Error, por favor escoja su ficha de las siguientes opciones: (X, O, RANDOM)")
        ficha = ficha.upper()
    print("\n--------------------------------------------------------------------\n")
    if ficha == "RANDOM":
        ficha = conjunto.pop()
        ficha2 = conjunto.pop()
    elif ficha == "X":
        ficha2 = "O"
    else:
        ficha2 = "X"
    return ficha, ficha2

def creartab():
    #Crea tablero
    filas = 8
    columnas = 8
    tab = [[" "]*columnas for i in range(filas)]
    tab[3][3] = "X"
    tab[4][4] = "X"
    tab[3][4] = "O"
    tab[4][3] = "O"
    return tab

def imprimirtab(tab):
    #Imprime tablero
    filas = len(tab)
    col = len(tab[0])

    print("\n  ---------------------------------")
    for f in range(filas):
        print(f+1,end=" | ")
        for c in range(col):
            print(tab[f][c],end=" | ")
        print("\n  ---------------------------------")
    print("    A   B   C   D   E   F   G   H")

def val_casillero1():
    #Validamos ambos casilleros
    lista = ["A","B","C","D","E","F","G","H"]
    while True:
        try:
            
            casillero = input("Ingresar casillero: ")
            assert len(casillero) == 2, "Son necesarios 2 digitos, ingresar (1A-8H)\n"
            fila = int(casillero[0])
            assert 1 <= fila <= 8, "El primer digito tiene que ser del 1 al 8, ingresar (1A-8H)\n"
            columna = casillero[1: ]
            assert columna.upper() in lista, "El segundo digito tiene que ser de la A a la H, ingresar (1A-8H)\n"
            break
        except ValueError:
            print("No hay un numero valido, ingresar (1A-8H)\n")
        except AssertionError as mensaje:
            print(mensaje)
    return fila-1,lista.index(columna.upper())

def val_jugada(c1,c2,tab,ficha):
    #Valida la jugada ingresada
    if tab[c1][c2] != " ":
        return False
    #recorremos fila hacia derecha
    for i in range(c2+1,8):
        if tab[c1][c2+1] == ficha or tab[c1][i] == " ":
            break
        elif tab[c1][i] == ficha:
            return True
            
    #recorremos fila hacia izquierda
    for i in range(c2-1,0,-1):
        if tab[c1][c2-1] == ficha or tab[c1][i] == " ":
            break
        elif tab[c1][i] == ficha:
            return True

    #recorremos la columna hacia abajo
    for i in range(c1+1,8):
        if tab[c1+1][c2] == ficha or tab[i][c2] == " ":
            break
        elif tab[i][c2] == ficha:
            return True
                
    #recorremos la columna hacia arriba 
    for i in range(c1-1,0,-1):
        if tab[c1-1][c2] == ficha or tab[i][c2] == " ":
            break
        elif tab[i][c2] == ficha:
            return True
                
    #recorremos diagonal abajo derecha
    f = c2
    for i in range(c1+1,8):
        f+=1
        try:
            if tab[c1+1][c2+1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha:
                return True
        except IndexError:
            break
                
    #recorremos diagonal abajo izquierda
    f = c2
    for i in range(c1+1,8):
        f-=1
        try:
            if tab[c1+1][c2-1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha:
                return True
        except IndexError:
            break
                
    #recorremos diagonal arriba derecha
    f=c2
    for i in range(c1-1,-1,-1):
        f+=1
        try:
            if tab[i][f] == " " or tab[c1-1][c2+1] == ficha:
                break
            elif tab[i][f] == ficha:
                return True
        except IndexError:
            break
                
    #recorremos diagonal arriba izquierda
    f=c2
    for i in range(c1-1,-1,-1):
        f-=1
        try:
            if tab[c1-1][c2-1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha:
                return True
        except IndexError:
            break

    return False

def VS(jugador,lista):
    letras = ["A","B","C","D","E","F","G","H"]
    cont_fichas = 60
    turnos = 0
    try:
        
        ficha1,ficha2 = elegir_ficha()
        print("          ___________________\n")
        print("                TABLERO")
        print("          ___________________\n")
        tableroPrincipal = creartab()
        imprimirtab(tableroPrincipal)
        print("\n________________________\n")
        if ficha1 == "X":
            print("El jugador 1 juega con X\nEl jugador 2 juega con O")
        else:
            print("El jugador 1 juega con O\nEl jugador 2 juega con X")
            turnos += 1
        print("________________________\n")
        while cont_fichas != 0:
            turnos += 1
            if turnos % 2 != 0:
                input("\nPresione enter para el siguiente turno (CTRL+C para finalizar programa): ")
                contador = 0
                jugadasPosibles, fichaNueva = jugadas_validas(tableroPrincipal,ficha1,contador)
                while jugadasPosibles == []:
                    print("Ningun jugador puede realizar movimientos, fin del juego.")
                    input("Presione CTRL+C y ENTER para finalizar.")
                if fichaNueva != ficha1 and jugador == 2:
                    print("\n-------------------------------------------------------\n")
                    print("Jugador 1 no puede realizar movimientos, pasa el turno.")
                    print("\n-------------------------------------------------------\n")
                    tableroPrincipal,lista = juega_Humano(tableroPrincipal,ficha2,letras,2,lista)
                elif fichaNueva != ficha1 and jugador == 1:
                    print("\n-------------------------------------------------------\n")
                    print("Jugador 1 no puede realizar movimientos, pasa el turno.")
                    print("\n-------------------------------------------------------\n")
                    tableroPrincipal,lista = juega_pc(tableroPrincipal,ficha1,letras,1,jugadasPosibles,lista)
                else:
                    tableroPrincipal,lista = juega_Humano(tableroPrincipal,ficha1,letras,1,lista)
                
            elif jugador == 1:
                #input("Presione intro para ver la jugada de la pc")
                contador = 0
                jugadasPosibles,fichaNueva = jugadas_validas(tableroPrincipal,ficha2,contador)
                while jugadasPosibles == []:
                    print("Ningun jugador puede realizar movimientos, fin del juego.")
                    input("Presione CTRL+C y ENTER para finalizar.")
                if fichaNueva != ficha2:
                    print("\n-------------------------------------------------------\n")
                    print("Jugador 2 no puede realizar movimientos, pasa el turno.")
                    print("\n-------------------------------------------------------\n")
                    tableroPrincipal,lista = juega_Humano(tableroPrincipal,ficha1,letras,1,lista)
                else:
                    tableroPrincipal,lista = juega_pc(tableroPrincipal,ficha2,letras,2,jugadasPosibles,lista)
                
            elif jugador == 2:
                input("\nPresione enter para el siguiente turno (CTRL+C para finalizar programa): ")
                contador = 0
                jugadasPosibles, fichaNueva = jugadas_validas(tableroPrincipal,ficha2,contador)
                while jugadasPosibles == []:
                    print("Ningun jugador puede realizar movimientos, fin del juego.")
                    input("Presione CTRL+C y ENTER para finalizar.")
                if fichaNueva != ficha2:
                    print("\n-------------------------------------------------------\n")
                    print("Jugador 1 no puede realizar movimientos, pasa el turno.")
                    print("\n-------------------------------------------------------\n")
                    tableroPrincipal,lista = juega_Humano(tableroPrincipal,ficha1,letras,1,lista)
                else:
                    tableroPrincipal,lista = juega_Humano(tableroPrincipal,ficha2,letras,2,lista)
            cont_fichas -= 1

    except KeyboardInterrupt:
        print("Finalizo el juego")        
    return tableroPrincipal, lista
        
            

def juega_Humano(tableroPrincipal,ficha,letras,jugador,lista):
    #Jugadas de los humanos
    try:
        print("\n--------------------\n")
        print("Turno del jugador", jugador)
        print("\n--------------------\n")
        fila,columna = val_casillero1()
        movimiento = val_jugada(fila,columna,tableroPrincipal,ficha)
        while movimiento == False:
            print("JUGADA INVALIDA\n")
            fila,columna = val_casillero1()
            movimiento = val_jugada(fila,columna,tableroPrincipal,ficha)
        poner_ficha(fila,columna,tableroPrincipal,ficha)
        imprimirtab(tableroPrincipal)
        letra = letras[columna]
        lista.append(str(fila+1) + letra)
    except KeyboardInterrupt:
        print("Presione CTRL+C de vuelta para terminar el juego")
    return tableroPrincipal,lista

def juega_pc(tab,ficha,letras,jugador,jugadasPosibles,lista):
    #Jugadas de la computadora
    try:
        random.shuffle(jugadasPosibles)
        mayorPuntos = -1
        for f,c in jugadasPosibles:
            copiadeTablero = copiaTablero(tab)
            poner_ficha(f,c,copiadeTablero,ficha)
            puntos = conteo_fichas(copiadeTablero,ficha)
            if puntos > mayorPuntos:
                mejor_jugada = [f,c]
                mayorPuntos = puntos
        fila,columna = mejor_jugada
        poner_ficha(fila,columna,tab,ficha)
        print("\n--------------------\n")
        print("Turno del jugador", jugador)
        print("\n--------------------\n")
        letra = letras[columna]
        print("Las", ficha, "Jugaron:", str(fila+1) + letra)
        lista.append(str(fila+1) + letra)
        imprimirtab(tab)
    except KeyboardInterrupt:
        pass
    return tab,lista

def jugadas_validas(tab,ficha,contador):
    #Revisa si hay jugadas validas en el tablero   
    jugadasPosibles = []
    for f in range(8):
        for c in range(8):
            if val_jugada(f,c,tab,ficha) != False:
                jugadasPosibles.append([f,c])
    if jugadasPosibles != [] or contador == 1:
        return jugadasPosibles,ficha
    else:
        if ficha == "X":
            jugadas_validas(tab,"O",contador+1)
        elif ficha == "O":
            jugadas_validas(tab,"X",contador+1)
            
            

def copiaTablero(tab):
    #Crea un duplicado del tablero
    tab_duplicado = [[" "]*8 for i in range(8)]         
    for f in range(8):
        for c in range(8):
            tab_duplicado[f][c] = tab[f][c]
    return tab_duplicado

def poner_ficha(c1,c2,tab,ficha):
    #Ubica la ficha en la posicion ingresada, si es posible
    tab[c1][c2] = ficha
    recorrer_tab(tab,ficha,c1,c2)

def conteo_fichas(tab,ficha):
    #Cuenta los puntos obtenidos
    filas = len(tab)
    columnas = len(tab[0])
    cont =  0
    
    for f in range(filas):
        for c in range(columnas):
            if tab[f][c] == ficha:
                cont += 1
                
    return cont

def recorrer_tab(tab,ficha,c1,c2):
    
    #recorremos fila hacia derecha
    for i in range(c2+1,8):
        if tab[c1][c2+1] == ficha or tab[c1][i] == " ":
            break
        elif tab[c1][i] == ficha:
            while i != c2:
                i -= 1
                tab[c1][i] = ficha 

    #recorremos fila hacia izquierda
    for i in range(c2-1,0,-1):
        if tab[c1][c2-1] == ficha or tab[c1][i] == " ":
            break
        elif tab[c1][i] == ficha and i!=c2:
            while i!=c2:
                i+=1
                tab[c1][i] = ficha

    #recorremos la columna hacia abajo
    for i in range(c1+1,8):
        if tab[c1+1][c2] == ficha or tab[i][c2] == " ":
            break
        elif tab[i][c2] == ficha:
            while i!=c1:
                i-=1
                tab[i][c2] = ficha
                
    #recorremos la columna hacia arriba 
    for i in range(c1-1,-1,-1):
        if tab[c1-1][c2] == ficha or tab[i][c2] == " ":
            break
        elif tab[i][c2] == ficha and i!=c1:
            while i!=c1:
                i+=1
                tab[i][c2] = ficha
                
    #recorremos diagonal abajo derecha
    f = c2
    for i in range(c1+1,8):
        f+=1
        if f == 8:
            break
        else:
            if tab[c1+1][c2+1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha and i!=c1 and f!=c2:
                while i!=c1 and f!=c2:
                    i-=1
                    f-=1
                    tab[i][f] = ficha
                    
    #recorremos diagonal abajo izquierda
    f = c2
    for i in range(c1+1,8):
        f-=1
        if f < 0 or i >= 8:
            break
        else:
            if tab[c1+1][c2-1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha and i!=c1 and f!=c2:
                while i!=c1 and f!=c2:
                    i-=1
                    f+=1
                    tab[i][f] = ficha
                
    #recorremos diagonal arriba derecha
    f=c2
    for i in range(c1-1,-1,-1):
        f+=1
        if f >= 8 or i < 0:
            break
        else:
            if tab[c1-1][c2+1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha:
                while i!=c1 and f!=c2:
                    i+=1
                    f-=1
                    tab[i][f] = ficha
                
    #recorremos diagonal arriba izquierda
    f=c2
    for i in range(c1-1,-1,-1):
        f-=1
        if f < 0 or i < 0:
            break
        else:
            if tab[c1-1][c2-1] == ficha or tab[i][f] == " ":
                break
            elif tab[i][f] == ficha and i!=c1 and f!=c2:
                while i!=c1 and f!=c2:
                    i+=1
                    f+=1
                    tab[i][f] = ficha
    
def imprimir_jugadas(lista,ficha):  
    if len(lista)>0:
        if ficha %2 == 0:
            signo = "X"
        else:
            signo = "O"
        print(lista[0], end=":"+ signo+"; ")
        imprimir_jugadas(lista[1: ], ficha+1)

#Programa Principal
jugadas = [] #Lista[str]
cont_fichas = 60
turnos = 0

ficha1 = "X"
ficha2 = "O"
try:
    print("____________________________________________________________________\n")
    mensaje_bienvenida = ("BIENVENIDOS AL REVERSI").center(67)
    print(mensaje_bienvenida)
    print("____________________________________________________________________\n")
    print("--------------------------------------------------------------------")
    reglas = input("Si quieres leer el manual de reglas, presiona 'R'.\nEn cambio, si quieres crear un archivo .txt del manual, presiona 'W'.\n")
    manual = "Reglas:\n1) Se emplea un tablero de 8x8 con 64 fichas, utilizando 32 'X' un jugador y 32 'O' el otro.\n2) El tablero comienza con dos fichas 'X' colocadas en 4D y 5E, y dos fichas 'O' colocadas en 4E y 5D.\n3) Comienzan jugando las 'X'.\n4) Durante su turno, el jugador debe colocar una ficha en una casilla libre que se encuentre alrededor de una ficha enemiga y que tambien se encuentre en linea con una ficha aliada por detras de la o las fichas enemigas (sin dejar espacio libre).\n5) Todas las fichas contrarias que se encuentren entre medio se convierten en sus piezas\n6) En caso de no poder mover, se pasa el turno al contrario.\n7) La partida termina si ninguno de los jugadores puede colocar mas fichas o presionando CTRL+C.\n8) Gana la partida el jugador con mas fichas en el tablero. (Empatando en el caso de tener la misma cantidad)"
    print("--------------------------------------------------------------------")
    if reglas.upper() == "R":
        print(manual)
        print("\n-------------------------------------------------------------------------------------------------------------\n")
    elif reglas.upper() == "W":
        crear_manual(manual)
        print("--------------------------------------------------------------------")
    while True:
        try:
            jugador = int(input("Ingresar 1 (para jugar contra la computadora) o 2 (para jugar contra otra persona): "))
            assert jugador == 1 or jugador == 2
            print("\n-------------------------------------------------------------------------------------------------------------\n")
            break
        except ValueError:
            print("Dato invalido.\nVuelva a poner el numero.\n")
        except AssertionError:
            print("Debe ingresar el numero 1 o 2\n")

    tableroPrincipal,jugadas = VS(jugador,jugadas)
    cant_x = conteo_fichas(tableroPrincipal,"X")
    cant_o = conteo_fichas(tableroPrincipal,"O")

    if cant_x > cant_o:
        print("\n_____________________________________________________\n")
        print("las",ficha1, "ganaron con",cant_x,"fichas contra",cant_o,"fichas de las", ficha2)
        print("_____________________________________________________\n")
    elif cant_o > cant_x:
        print("\n______________________________________________________________\n")
        print("El jugador 2 ganó con",cant_o,"fichas contra",cant_x,"fichas del jugador 1.")
        print("______________________________________________________________\n")
    else:
        print("\n_________________________________________________\n")
        print("Ambos jugadores empataron con",cant_x,"fichas cada uno.")
        print("_________________________________________________\n")

    pregunta = input("¿Quiere ver la lista de jugadas? (Y/N): ")
    if pregunta.upper() == "Y":
        imprimir_jugadas(jugadas,0)
except KeyboardInterrupt:
    print("Finalizo el juego")