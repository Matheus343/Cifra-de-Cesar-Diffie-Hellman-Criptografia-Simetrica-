from socket import *
import random
import time

def primo_fast(N):
    start_time = time.time()
    resultado = ""
    i = 2
    while i < N:
        R = N % i
        if R == 0:
            resultado = f"{N} não é primo!"
            break
        i += 1
    else:
        resultado = f"{N} é primo!"
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"  [FAST] {resultado} | Tempo: {execution_time:.6f}s")
    return "não" not in resultado

def primo_slow(N):
    start_time = time.time()
    cont = 0
    i = 2
    while i < N:
        R = N % i
        if R == 0:
            cont += 1
        i += 1
    if cont == 0:
        resultado = f"{N} é primo!"
    else:
        resultado = f"{N} não é primo!"
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"  [SLOW] {resultado} | Tempo: {execution_time:.6f}s")
    return cont == 0

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

def potencia_modular(base, exp, mod):
    resultado = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            resultado = (resultado * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return resultado

DH_P = 23 
DH_G = 5

print("=" * 55)
print("  TCP Client — Alice")
print("=" * 55)
print(f"\n[DH] Validando parâmetros: p={DH_P}, g={DH_G}\n")

print(f"  Testando p={DH_P}:")
p_fast = primo_fast(DH_P)
p_slow = primo_slow(DH_P)

print(f"\n  Testando g={DH_G}:")
g_fast = primo_fast(DH_G)
g_slow = primo_slow(DH_G)

if not p_fast:
    print(f"\n[ERRO] p={DH_P} não é primo! Diffie-Hellman exige p primo. Encerrando.")
    exit(1)

print(f"\n[✓] Parâmetros válidos! Conectando ao servidor...\n")

serverName = "127.0.0.1"
serverPort = 1300

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print("[+] Conectado ao servidor!\n")

a_privado = random.randint(2, DH_P - 2)
A_publico = potencia_modular(DH_G, a_privado, DH_P) 
print(f"[DH] Chave privada de Alice (secreta) : a={a_privado}")
print(f"[DH] Chave pública de Alice (enviada) : A={A_publico}")

clientSocket.send(str(A_publico).encode("utf-8"))

B_publico = int(clientSocket.recv(1024).decode("utf-8"))
print(f"[DH] Chave pública de Bob  recebida  : B={B_publico}")

segredo = potencia_modular(B_publico, a_privado, DH_P)
print(f"[DH] Segredo compartilhado calculado : s={segredo}")
print(f"[DH] Chave da Cifra de César = {segredo}")
print("-" * 55)

sentence = input("\nInput lowercase sentence: ")

sentence_cifrada = criptografar(sentence, segredo)
print(f"\n[→] Enviando  (cifrado)   : {sentence_cifrada}")

clientSocket.send(bytes(sentence_cifrada, "utf-8"))

resposta_bytes = clientSocket.recv(65000)
resposta_cifrada = str(resposta_bytes, "utf-8")
print(f"[←] Recebido  (cifrado)   : {resposta_cifrada}")

resposta_final = decriptografar(resposta_cifrada, segredo)
print(f"[✓] Received from Make Upper Case Server: {resposta_final}")

clientSocket.close()
print("\n[✓] Conexão encerrada.")