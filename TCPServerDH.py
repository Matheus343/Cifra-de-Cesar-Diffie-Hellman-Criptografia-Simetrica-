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

DH_P = 15  
DH_G = 5    

print("=" * 55)
print("  TCP Server — Bob")
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

print(f"\n[✓] Parâmetros válidos! Iniciando servidor...\n")

serverPort = 1300
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(5)
print("[✓] Aguardando conexão...\n")

connectionSocket, addr = serverSocket.accept()
print(f"[+] Conexão recebida de {addr}")

A_publico = int(connectionSocket.recv(1024).decode("utf-8"))
print(f"\n[DH] Chave pública de Alice recebida : A={A_publico}")

b_privado = random.randint(2, DH_P - 2)
B_publico = potencia_modular(DH_G, b_privado, DH_P)  
print(f"[DH] Chave privada de Bob  (secreta) : b={b_privado}")
print(f"[DH] Chave pública de Bob  (enviada) : B={B_publico}")

connectionSocket.send(str(B_publico).encode("utf-8"))

segredo = potencia_modular(A_publico, b_privado, DH_P)
print(f"[DH] Segredo compartilhado calculado : s={segredo}")
print(f"[DH] Chave da Cifra de César = {segredo}")
print("-" * 55)

dados = connectionSocket.recv(65000)
mensagem_cifrada = str(dados, "utf-8")
print(f"\n[←] Recebido  (cifrado)   : {mensagem_cifrada}")

mensagem_original = decriptografar(mensagem_cifrada, segredo)
print(f"[✓] Decriptografado       : {mensagem_original}")

mensagem_upper = mensagem_original.upper()
print(f"[↑] Processado            : {mensagem_upper}")

resposta_cifrada = criptografar(mensagem_upper, segredo)
print(f"[→] Enviando  (cifrado)   : {resposta_cifrada}")

connectionSocket.send(bytes(resposta_cifrada, "utf-8"))
connectionSocket.close()
serverSocket.close()
print("\n[✓] Conexão encerrada.")