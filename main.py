# Piedra, papel, tijera, lagarto o spock

import random
import json
import os
import time
from mensajes import msg

SAVEFILE = "puntuacion2.txt"
SAVE_ON_EXIT = True
SAVE_ON_CYCLE = True

moves = ["R", "P", "S", "L", "K"]
control = ["E", "RQ"]

contBuenas = 0
contTotal = 0


gameStatus = None


def jugador(gameStatus):
    plyr = input("Introduzca su nombre: ")
    if plyr not in gameStatus["punt"]:
        gameStatus["punt"][plyr] = newPun()
        print(msg["crear"])
    else:
        print(msg["cargar"])

    return plyr


def inicio(moves, control):
    tiempoInicio()
    usuario = introducir()
    while usuario not in moves + control:
        print(msg["error"])
        print(msg["exit"])
        usuario = introducir()
    contadorBuenas(gameStatus)
    return usuario


def introducir():
    elecc = input(msg["input"])
    contadorInput(gameStatus)
    return elecc


def juego(usuario, gameStatus, startTime, moves, control):
    maquina = random.choice(moves)

    win = [["R", "S"], ["R", "L"], ["P", "R"], ["P", "K"], ["S", "P"], ["S", "L"], ["L", "K"], ["L", "P"], ["K", "S"], ["K", "R"]]

    if usuario in control:
        tiempoEjecucion(startTime)
        if SAVE_ON_EXIT:
            guardar(gameStatus)
        print(msg["mensajeSalida"])
        imprimir(gameStatus)
        exit()

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

    print(msg["mensajeMaquina"].format(**{"eleccionMaquina": eleccionMaquina}))

    eleccion = {
        "eleccionUsuario": eleccionUsuario,
        "eleccionMaquina": eleccionMaquina
    }

    if usuario == maquina:
        print(msg["mensajeEmpate"].format(**eleccion))
        punto = 0
        return punto
    elif [usuario, maquina] in win:
        print(msg["mensajeVictoria"].format(**eleccion))
        punto = 2
        return punto
    else:
        print(msg["mensajeDerrota"].format(**eleccion))
        punto = 1
        return punto


def newPun():
    return {
        "Partidas": 0,
        "Victorias": 0,
        "Derrotas": 0,
        "Empates": 0,
    }


def diccionario():
    if os.path.isfile(SAVEFILE):
        with open(SAVEFILE) as json_file:
            gameStatus = json.load(json_file)
            return gameStatus
    else:
        gameStatus = {
            "punt": {

            },
            "stats": {
                "tiempo_ejec": 0,
                "total_imput": 0,
                "buenas_imput": 0,
            }
        }
        return gameStatus


def tiempoInicio():
    startTime = time.time()
    return startTime


def tiempoEjecucion(startTime):
    elapsedTime = time.time() - startTime
    gmTime = time.gmtime(elapsedTime)
    slapsedStr = time.strftime("%H:%M:%S", gmTime)
    gameStatus["stats"]["tiempo_ejec"] = gmTime
    return gmTime


def contadorInput(gameStatus):
    gameStatus["stats"]["total_imput"] = gameStatus["stats"]["total_imput"] + 1


def contadorBuenas(gameStatus):
    gameStatus["stats"]["buenas_imput"] = gameStatus["stats"]["buenas_imput"] + 1


def puntuacion(puntos, gameStatus, plyr):
    gameStatus["punt"][plyr]["Partidas"] = gameStatus["punt"][plyr]["Partidas"] + 1

    if puntos == 0:
        gameStatus["punt"][plyr]["Empates"] = gameStatus["punt"][plyr]["Empates"] + 1
    elif puntos == 1:
        gameStatus["punt"][plyr]["Derrotas"] = gameStatus["punt"][plyr]["Derrotas"] + 1
    else:
        gameStatus["punt"][plyr]["Victorias"] = gameStatus["punt"][plyr]["Victorias"] + 1

    # print(json.dumps(punt, indent=4))
    print(msg["jugador"].format(**{"plyr": plyr}))

    print(msg["contador"].format(**gameStatus["punt"][plyr]))

    print(msg["exit"])
    print(msg["linea"])


def guardar(gameStatus):
    with open(SAVEFILE, "w") as outfile:
        json.dump(gameStatus, outfile, indent=4)


def imprimir(gameStatus):

    print(msg["stats"].format(**gameStatus["stats"]))


def ranking(usuario, gameStatus):
    for n in punt:
        m = n + 1
        if gameStatus["punt"][n]["Victorias"] > gameStatus["punt"][m]["Victorias"]:
            print(gameStatus["punt"][n])
        else:
            n = n + 1


def main():
    print(msg["inicio"])
    startTime = tiempoInicio()
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
