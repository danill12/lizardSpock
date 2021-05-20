# Piedra, papel, tijera, lagarto o spock


import random
import json
import os
import time
from mensajes import msg

SAVEFILE = "puntuacion2.txt"
SAVE_ON_EXIT = True
SAVE_ON_CYCLE = True

# definimos los movimientos del juego y los elementos de control para manejarnos por el mismo
moves = ["R", "P", "S", "L", "K"]
movesM = ["r", "p", "s", "l", "k"]
control = ["E", "RQ"]
controlM = ["e", "rq"]

gameStatus = None


def jugador(gameStatus):
    # Introducimos el nombre del usuario y verificamos si ya esta guardado, si no creamos una nueva "partida"
    plyr = input("Introduzca su nombre: ")
    if plyr not in gameStatus["punt"]:
        gameStatus["punt"][plyr] = newPun()
        print(msg["crear"])
    else:
        print(msg["cargar"])

    return plyr


def inicio(moves, control):
    # Inciamos el juego y pedimos los movimientos del jugador, tambien comprobamos si son correctos
    usuario = introducir()
    while usuario not in moves + control and usuario not in movesM + controlM:
        print(msg["error"])
        print(msg["exit"])
        usuario = introducir()
    contadorBuenas(gameStatus)
    return usuario


def introducir():
    # funcion input para pedir los movimientos del jugador
    elecc = input(msg["input"])
    contadorInput(gameStatus)
    return elecc


def juego(usuario, gameStatus, startTime, moves, control):
    # funcion juego es donde esta la logica del programa
    # la maquina elige un movimiento
    maquina = random.choice(moves)

    win = [["R", "S"], ["R", "L"], ["P", "R"], ["P", "K"], ["S", "P"], ["S", "L"], ["L", "K"], ["L", "P"], ["K", "S"], ["K", "R"]]
    winM = [["r", "s"], ["r", "l"], ["p", "r"], ["p", "k"], ["s", "p"], ["s", "l"], ["l", "k"], ["l", "p"], ["k", "s"], ["k", "r"]]

    # sistema de salida del juego con la tecla "E"
    if usuario in control:
        # llama a la funcion contadorTiempo para obtener el timpo de juego
        gameStatus = contadorTiempo(gameStatus, startTime)
        if SAVE_ON_EXIT:
            guardar(gameStatus)
        print(msg["mensajeSalida"])
        imprimir(gameStatus)
        exit()

    # mejora de interfaz al indicar la eleccion de la maquina y la jugada

    opcionesMovimientos: {
        "R": msg["moveR"],
        "P": msg["moveP"],
        "S": msg["moveS"],
        "L": msg["moveL"],
        "K": msg["moveK"]
    }

    eleccionUsuario = opcionesMovimientos[usuario]
    eleccionMaquina = opcionesMovimientos[maquina]

    print(msg["mensajeMaquina"].format(**{"eleccionMaquina": eleccionMaquina}))

    """
    if maquina == "R":
        eleccionMaquina = "Piedra"
    elif maquina == "P":
        eleccionMaquina = "Papel"
    elif maquina == "S":
        eleccionMaquina = "Tijeras"
    elif maquina == "L":
        eleccionMaquina = "Lagarto"
    elif maquina == "K":
        eleccionMaquina = "Spock"

    if usuario == "R":
        eleccionUsuario = "Piedra"
    elif usuario == "P":
        eleccionUsuario = "Papel"
    elif usuario == "S":
        eleccionUsuario = "Tijeras"
    elif usuario == "L":
        eleccionUsuario = "Lagarto"
    elif usuario == "K":
        eleccionUsuario = "Spock"

    eleccion = {
        "eleccionUsuario": usuario,
        "eleccionMaquina": maquina
    }

    """

    # logica del juego
    if usuario == maquina:
        print(msg["mensajeEmpate"].format(**eleccion))
        punto = 0
        return punto
    elif [usuario, maquina] in win or [usuario, maquina] in winM:
        print(msg["mensajeVictoria"].format(**eleccion))
        punto = 2
        return punto
    else:
        print(msg["mensajeDerrota"].format(**eleccion))
        punto = 1
        return punto


def newPun():
    # funcion utulizada para añadir una partida a los jugadores nuevos
    return {
        "Partidas": 0,
        "Victorias": 0,
        "Derrotas": 0,
        "Empates": 0,
    }


def diccionario():
    # comprobamos si existe un archivo de anteriores partidas o si no creamos uno nuevo
    if os.path.isfile(SAVEFILE):
        with open(SAVEFILE) as json_file:
            gameStatus = json.load(json_file)
            return gameStatus
    else:
        gameStatus = {
            "punt": {

            },
            "stats": {
                "tiempo_ejec": 0.0,
                "total_imput": 0,
                "buenas_imput": 0,
            }
        }
        return gameStatus


def tiempoInicio():
    # iniciamos la cuenta del tiempo
    startTime = time.time()
    return startTime


def tiempoEjecucion(startTime):
    # operacion para obtener el tempo de juego
    elapsedTime = time.time() - startTime
    return elapsedTime


def contadorTiempo(gameStatus, startTime):
    # sumamos el tiempo de la partida actual al tiempo total del programa
    gameStatus["stats"]["tiempo_ejec"] = gameStatus["stats"]["tiempo_ejec"] + tiempoEjecucion(startTime)
    return gameStatus


def convertidorTiempo(elapsedTime):
    # mejora visual para sacar el tiempo de juego
    gmTime = time.gmtime(elapsedTime)
    slapsedStr = time.strftime("%H:%M:%S", gmTime)
    return slapsedStr


def contadorInput(gameStatus):
    # contador de los input totales que entran por teclado
    gameStatus["stats"]["total_imput"] = gameStatus["stats"]["total_imput"] + 1


def contadorBuenas(gameStatus):
    # contador de los inputs que el programa acepta como buenos(los movimientos del juego o elementos de control)
    gameStatus["stats"]["buenas_imput"] = gameStatus["stats"]["buenas_imput"] + 1


def puntuacion(puntos, gameStatus, plyr):
    # suma del resultado de la ronda en el diccionario
    gameStatus["punt"][plyr]["Partidas"] = gameStatus["punt"][plyr]["Partidas"] + 1

    if puntos == 0:
        gameStatus["punt"][plyr]["Empates"] = gameStatus["punt"][plyr]["Empates"] + 1
    elif puntos == 1:
        gameStatus["punt"][plyr]["Derrotas"] = gameStatus["punt"][plyr]["Derrotas"] + 1
    else:
        gameStatus["punt"][plyr]["Victorias"] = gameStatus["punt"][plyr]["Victorias"] + 1

    # salida de texto con el resltado de la ronda (llamada al archivo mensajes.py)
    print(msg["jugador"].format(**{"plyr": plyr}))

    print(msg["contador"].format(**gameStatus["punt"][plyr]))

    print(msg["exit"])
    print(msg["linea"])


def guardar(gameStatus):
    # guarda la partida mediante json's
    with open(SAVEFILE, "w") as outfile:
        json.dump(gameStatus, outfile, indent=4)


def imprimir(gameStatus):
    # llama a la funcion tiempoConvertido e imprime el resultado, a su vez imprime el numeor de outputs(totales y aceptados) (mensajes.py)
    tiempoConvertido = convertidorTiempo(gameStatus["stats"]["tiempo_ejec"])
    print(msg["tiempo"].format(**{"tiempoConvertido": tiempoConvertido}))

    print(msg["stats"].format(**gameStatus["stats"]))


def ranking(usuario, gameStatus):
    # proyecto de ranking
    for n in punt:
        m = n + 1
        if gameStatus["punt"][n]["Victorias"] > gameStatus["punt"][m]["Victorias"]:
            print(gameStatus["punt"][n])
        else:
            n = n + 1


def main():
    startTime = tiempoInicio()
    print(msg["inicio"])
    global gameStatus
    gameStatus = diccionario()
    plyr = jugador(gameStatus)
    while True:
        usuario = inicio(moves, control)
        if usuario == "RQ":
            ranking(usuario, gameStatus)
        puntos = juego(usuario, gameStatus, startTime, moves, control)
        puntuacion(puntos, gameStatus, plyr)
        if SAVE_ON_CYCLE:
            guardar(gameStatus)


main()
