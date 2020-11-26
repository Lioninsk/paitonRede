def leitura_arquivo(arquivo):
    with open(f"{arquivo}.txt", "rt") as fr:
        return fr.readlines()


def print_definido(indice, item):
    if(item == "\n"):
        return
    if(indice == 0):
        print(f"IP:{item}")
    elif(indice == 1):
        print(f"Mac:{item}")
    elif(indice == 2):
        print(f"Fabricante:{item}")
    else:
        print(f"Status:{item}")
    
    
def mostra_historico():
    linhas = leitura_arquivo("historico")
    matriz = []
    for linha in linhas:
        matriz.append(linha.split(":"))
    contador_dispositivos = 0
    contador_buscas = 0
    for linha in matriz:
        if(linha[0] != "\n"):
            contador_dispositivos += 1
            if(contador_dispositivos == 1):
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
        file.write("\n\n")#fim busca





