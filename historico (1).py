import socket
import multiprocessing
import subprocess
import os

from getmac import get_mac_address
import requests
import datetime

def pinger(job_q, results_q):
    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list
#######################################################################################

def get_mac_details(mac_address):
    url = "https://api.macvendors.com/"

    response = requests.get(url + mac_address)
    if response.status_code != 200:
        raise Exception("IP MAC nao encontrado!")
    return response.content.decode()

########################################################################################################

def leitura_arquivo(arquivo):
    with open(f"{arquivo}.txt", "rt") as fr:
        return fr.readlines()


def print_definido(indice, item):
    if (item == "\n"):
        return
    if (indice == 0):
        print(f"Tipo:{item}")
    elif (indice == 1):
        print(f"IP:{item}")
    elif (indice == 2):
        print(f"Mac:{item}")
    elif (indice == 3):
        print(f"Fabricante:{item}")
    elif (indice == 4):
        print(f"Status:{item}")
    elif (indice == 5):
        print(f"Status:{item}")


def mostra_historico():
    linhas = leitura_arquivo("historico")
    matriz = []
    for linha in linhas:
        matriz.append(linha.split("#"))
    contador_dispositivos = 0
    contador_buscas = 0
    for linha in matriz:
        if (linha[0] != "\n"):
            contador_dispositivos += 1
            if (contador_dispositivos == 1):
                contador_buscas += 1
                print("========================")
                print(f"Busca numero: {contador_buscas}\n")
            print(f"Dispositivo {contador_dispositivos}")
        else:
            contador_dispositivos = 0
        for i in range(len(linha)):
            print_definido(i, linha[i])


def salva_estado_historico():
    linhas = leitura_arquivo("estado")
    with open("historico.txt", "a") as file:
        for linha in linhas:
            file.write(linha)
        file.write("\n\n")  # fim busca

##########################################################

def salva_estado(lst_dispositivo):
    f = open("estado.txt", "w")
    for dispositivo in lst_dispositivo:
        f.write(dispositivo[0] + "#" + dispositivo[1] + "#" + dispositivo[2] + "#" + dispositivo[3] + "#" + dispositivo[4] + "#" + dispositivo[5] + "\n")

if __name__ == "__main__":
    now = datetime.datetime.now()
    lst_ip = map_network()

    lst_dispositivo = []

    for ip in lst_ip:
        dispositivo = []
        tipo = "teste"
        try:
            mac = get_mac_address(ip=ip)
            fabricante = get_mac_details(mac)
        except:
            mac = "Nao Encontrado"
            fabricante = "Nao Encontrado"
        status = "Online"
        hora_inicial = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
        dispositivo.extend([tipo, ip, mac, fabricante, status, hora_inicial])
        print(dispositivo)
        lst_dispositivo.append(dispositivo)


    salva_estado(lst_dispositivo)

    salva_estado_historico()
    mostra_historico()

