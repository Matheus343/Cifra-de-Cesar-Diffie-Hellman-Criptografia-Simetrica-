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
#alice
serverName = "127.0.0.1"
serverPort = 1300

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

sentence = input("Input lowercase sentence: ")

sentence_cifrada = criptografar(sentence, CHAVE)
print(f"[→] Enviando cifrado   : {sentence_cifrada}")

clientSocket.send(bytes(sentence_cifrada, "utf-8"))

modifiedSentence = clientSocket.recv(65000)
resposta_cifrada = str(modifiedSentence, "utf-8")
print(f"[←] Recebido cifrado   : {resposta_cifrada}")

resposta_final = decriptografar(resposta_cifrada, CHAVE)
print(f"[✓] Received from Make Upper Case Server: {resposta_final}")

clientSocket.close()