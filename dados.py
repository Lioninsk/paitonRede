def ip_ja_guardado(ip):
    ip = ip + "\n"
    with open("dados.txt", "r") as file:
        linhas = file.readlines()
    for i in range(len(linhas)):
        try:
            string_ip = linhas[i*5].split(":")# ["IP","ip"]
            if(string_ip[1] == ip):
                return True
        except:
            return False
    

def salva_dados(ip, mac, fabricante, data):
    if not (ip_ja_guardado(ip)):
        with open("dados.txt", "a") as file:
            file.write(f"IP:{ip}\nMac:{mac}\nFabricante:{fabricante}\nData de descoberta:{data}\n\n")


def mostra_dados():
    with open("dados.txt", "r") as file:
        linhas = file.readlines()
    for linha in linhas:
        linha = linha.strip()
        print(linha)



#salva_dados("ip", "mac", "fab", "data")


