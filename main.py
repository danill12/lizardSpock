# Piedra, papel, tijera, lagarto o spock

import random
import json
import os
import time
from mensajes import msg

SAVEFILE = "save.json"
SAVE_ON_EXIT = True
SAVE_ON_CYCLE = True
# definimos los movimientos del juego y los elementos de CONTROL para manejarnos por el mismo
MOVES = ["R", "P", "S", "L", "K"]
WINMOVES = [["R", "S"], ["R", "L"], ["P", "R"], ["P", "K"], ["S", "P"], ["S", "L"], ["L", "K"], ["L", "P"], ["K", "S"], ["K", "R"]]
CONTROL = ["E"]

gameStatus = None


def jugador(gameStatus):
    # Introducimos el nombre del usuario y verificamos si ya esta guardado, si no creamos una nueva "partida"
    plyr = input(msg["nameInput"])
    if plyr not in gameStatus["punt"]:
        gameStatus["punt"][plyr] = newPun()
        print(msg["crear"])
    else:
        print(msg["cargar"])

    return plyr


def getPlayerMove():
    # Inciamos el juego y pedimos los movimientos del jugador, tambien comprobamos si son correctos
    def getPlayerInput():
        # funcion input para pedir los movimientos del jugador
        elecc = input(msg["getPlayerMove"]).upper()
        increaseInputCounter(gameStatus)

        return elecc

    usuario = getPlayerInput()
    while usuario not in MOVES + CONTROL:
        print(msg["error"])
        print(msg["exit"])
        usuario = getPlayerInput()
    increaseGoodCounter(gameStatus)

    return usuario


def juego(usuario, gameStatus, startTime):
    # funcion juego es donde esta la logica del programa
    # la maquina elige un movimiento
    maquina = random.choice(MOVES)

    # sistema de salida del juego con la tecla "E" o "e"
    if usuario in CONTROL:
        # llama a la funcion contadorTiempo para obtener el timpo de juego


        if SAVE_ON_EXIT:
            guardar(gameStatus)

        print(msg["mensajeSalida"])
        printStats(startTime)
        exit()

    # mejora de interfaz al indicar la eleccion de la maquina y la jugada

    opcionesMovimientos = {
        "R": msg["moveR"],
        "P": msg["moveP"],
        "S": msg["moveS"],
        "L": msg["moveL"],
        "K": msg["moveK"],
    }

    eleccion = {
        "userChoice": opcionesMovimientos[usuario],
        "cpuChoice": opcionesMovimientos[maquina]
    }

    print(msg["mensajeMaquina"].format(**eleccion))

    # logica del juego
    if usuario == maquina:
        print(msg["mensajeEmpate"].format(**eleccion))
        punto = 0
        return punto
    elif [usuario, maquina] in WINMOVES:
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
        "partidas": 0,
        "victorias": 0,
        "derrotas": 0,
        "empates": 0,
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
                "total_input": 0,
                "buenas_input": 0,
            }
        }
        return gameStatus


def contadorTiempo(gameStatus, startTime):
    # sumamos el tiempo de la partida actual al tiempo total del programa
    sessionTime = time.time() - startTime
    gameStatus["stats"]["tiempo_ejec"] += sessionTime

    return sessionTime


def convertidorTiempo(elapsedTime):
    # mejora visual para sacar el tiempo de juego
    gmTime = time.gmtime(elapsedTime)
    slapsedStr = time.strftime("%H:%M:%S", gmTime)

    return slapsedStr


def increaseInputCounter(gameStatus):
    # contador de los input totales que entran por teclado
    gameStatus["stats"]["total_input"] += 1


def increaseGoodCounter(gameStatus):
    # contador de los inputs que el programa acepta como buenos(los movimientos del juego o elementos de CONTROL)
    gameStatus["stats"]["buenas_input"] += 1


def puntuacion(puntos, gameStatus, plyr):
    # suma del resultado de la ronda en el diccionario
    gameStatus["punt"][plyr]["partidas"] += 1

    if puntos == 0:
        gameStatus["punt"][plyr]["empates"] += 1
    elif puntos == 1:
        gameStatus["punt"][plyr]["derrotas"] += 1
    else:
        gameStatus["punt"][plyr]["victorias"] += 1

    # salida de texto con el resltado de la ronda (llamada al archivo mensajes.py)
    print(msg["jugador"].format(**{"plyr": plyr}))

    print(msg["contador"].format(**gameStatus["punt"][plyr]))

    print(msg["exit"])
    print(msg["linea"])


def guardar(gameStatus):
    # guarda la partida mediante json's
    with open(SAVEFILE, "w") as outfile:
        json.dump(gameStatus, outfile, indent=4)


def printStats(startTime):
    # llama a la funcion tiempoTotal e imprime el resultado, a su vez imprime el numeor de outputs(totales y aceptados) (mensajes.py)
    sessionTime = contadorTiempo(gameStatus, startTime)
    sessionText = convertidorTiempo(sessionTime)

    print(msg["sessionTime"].format(**{"sessionTime": sessionText}))

    timeText = convertidorTiempo(gameStatus["stats"]["tiempo_ejec"])
    print(msg["totalTime"].format(**{"tiempoTotal": timeText}))

    print(msg["stats"].format(**gameStatus["stats"]))


def main():
    global gameStatus

    startTime = time.time()
    print(msg["inicio"])
    gameStatus = diccionario()
    plyr = jugador(gameStatus)
    while True:
        usuario = getPlayerMove()
        puntos = juego(usuario, gameStatus, startTime)
        puntuacion(puntos, gameStatus, plyr)
        if SAVE_ON_CYCLE:
            guardar(gameStatus)


main()
