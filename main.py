# Piedra, papel, tijera, lagarto o spock

import random
import json
import os
import time
from mensajes import msg

SAVEFILE = "puntuacion2.txt"
SAVE_ON_EXIT = True
SAVE_ON_CYCLE = True

punt = None


def jugador():
    plyr = input("Introduzca su nombre: ")
    if plyr not in punt:
        punt[plyr] = newPun()
        print(msg["crear"])
    else:
        print(msg["cargar"])

    return plyr


def inicio():
    tiempoInicio()
    usuario = input("Escriba su elección: Piedra(R), Papel(P), Tijeras(S), Lagarto(L) o Spock(K): ")
    while usuario != "R" and usuario != "P" and usuario != "S" and \
            usuario != "E" and usuario != "L" and usuario != "K" and usuario != "RQ":
        print(msg["error"])
        print(msg["exit"])
        usuario = input("Escriba su elección: Piedra(R), Papel(P),\
 Tijeras(S), Lagarto(L) o Spock(K): ")
    return usuario


def juego(usuario, punt):
    maquina = random.choice(["R", "P", "S", "L", "K"])

    win = [["R", "S"], ["R", "L"], ["P", "R"], ["P", "K"], ["S", "P"], ["S", "L"], ["L", "K"], ["L", "P"], ["K", "S"], ["K", "R"]]

    if usuario == "E":
        tiempoEjecucion()
        if SAVE_ON_EXIT:
            guardar(punt)
        print(msg["mensajeSalida"])
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


def diccionario_puntos():
    if os.path.isfile(SAVEFILE):
        with open(SAVEFILE) as json_file:
            punt = json.load(json_file)
            return punt
    else:
        punt = {
        }
        return punt


def diccionario_stats():

    if os.path.isfile(SAVEFILE):
        with open(SAVEFILE) as json_file:
            punt = json.load(json_file)
            return stats
    else:
        stats = {
            "tiempo_ejec": elapsedTime,
            "total_imput": ,
            "buenas_imput": ,
        }
        return stats


def tiempoInicio():
    startTime = time.time()


def tiempoEjecucion():
    elapsedTime = time.time() - startTime()


def puntuacion(puntos, punt, plyr):
    punt[plyr]["Partidas"] = punt[plyr]["Partidas"] + 1

    if puntos == 0:
        punt[plyr]["Empates"] = punt[plyr]["Empates"] + 1
    elif puntos == 1:
        punt[plyr]["Derrotas"] = punt[plyr]["Derrotas"] + 1
    else:
        punt[plyr]["Victorias"] = punt[plyr]["Victorias"] + 1

    # print(json.dumps(punt, indent=4))
    print(msg["jugador"].format(**{"plyr": plyr}))

    print(msg["contador"]["Partidas"].format(**punt[plyr]))
    print(msg["contador"]["Victorias"].format(**punt[plyr]))
    print(msg["contador"]["Derrotas"].format(**punt[plyr]))
    print(msg["contador"]["Empates"].format(**punt[plyr]))
    print(msg["exit"])
    print(msg["linea"])


def guardar(punt, stats):
    with open(SAVEFILE, "w") as outfile:
        json.dump(punt, outfile, indent=4)
    with open(SAVEFILE, "w") as outfile:
        json.dump(stats, outfile, indent=4)


def ranking(usuario, punt):
    for n in punt:
        m = n + 1
        if punt[n]["Victorias"] > punt[m]["Victorias"]:
            print(punt[n])
        else:
            n = n + 1


def main():
    print(msg["inicio"])
    global punt
    punt = diccionario_puntos()
    stats = diccionario_stats()
    plyr = jugador()
    while True:
        usuario = inicio()
        if usuario == "RQ":
            ranking(usuario, punt)
        puntos = juego(usuario, punt)
        puntuacion(puntos, punt, plyr)
        if SAVE_ON_CYCLE:
            guardar(punt)


main()
