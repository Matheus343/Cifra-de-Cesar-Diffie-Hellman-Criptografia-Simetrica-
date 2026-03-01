from socket import *

def criptografar(texto, chave):
    chave = chave % 95
    resultado = ""
    for char in texto:
        codigo = ord(char)
        if 32 <= codigo <= 126:
            novo_codigo = 32 + (codigo - 32 + chave) % 95
            resultado += chr(novo_codigo)
        else:
            resultado += char
    return resultado

def decriptografar(texto, chave):
    return criptografar(texto, -chave)

CHAVE = 7

#bob
serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("TCP Server com Cifra de César\n")

connectionSocket, addr = serverSocket.accept()
print(f"[+] Conexão recebida de {addr}\n")

dados = connectionSocket.recv(65000)
mensagem_cifrada = str(dados, "utf-8")
print(f"[←] Recebido cifrado   : {mensagem_cifrada}")

mensagem_original = decriptografar(mensagem_cifrada, CHAVE)
print(f"[✓] Decriptografado    : {mensagem_original}")

mensagem_upper = mensagem_original.upper()
print(f"[↑] Processado         : {mensagem_upper}")

resposta_cifrada = criptografar(mensagem_upper, CHAVE)
print(f"[→] Enviando cifrado   : {resposta_cifrada}")

connectionSocket.send(bytes(resposta_cifrada, "utf-8"))

connectionSocket.close()
serverSocket.close()
print("\n[✓] Conexão encerrada.")