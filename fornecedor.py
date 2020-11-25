import requests 


def get_mac_fornecedor(endereco_mac): 
	# API
	link = "https://api.macvendors.com/" 
	response = requests.get(link+endereco_mac) 
	if response.status_code != 200: 
		raise Exception("Invalid MAC!") 
	return response.content.decode() 


#exemplo: 
# endereco_mac = "00:A0:C9:14:C8:29"
endereco_mac = "3c:cf:5b:c6:7a:72"
nome_fornecedor = get_mac_fornecedor(endereco_mac) 
print(f"\nfornecedor:{nome_fornecedor}")

