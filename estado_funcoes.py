def leitura_estado():
    with open("estado.txt", "rt") as fr:
        return fr.readlines()

def todos_offline():
    linhas = leitura_estado()
    with open("estado.txt", "wt") as fw:
        for linha in linhas:
            fw.write(linha.replace("Online", "Offline"))


def definir_dispositivo_online(ip):
    linhas = leitura_estado()
    dispositivos = []
    for linha in linhas:
        vet = linha.strip()
        dispositivos.append(vet.split(":"))
    novas_linhas = ""
    for i in range(len(dispositivos)):
        if dispositivos[i][0] == ip:
            linhas[i] = linhas[i].replace("Offline", "Online")
        novas_linhas += linhas[i]
    with open("estado.txt", "wt") as fw:
                fw.write(novas_linhas)  
