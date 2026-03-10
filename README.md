# 🔐 Comunicação TCP Segura — Cifra de César + Diffie-Hellman + RSA

Projeto acadêmico desenvolvido para a disciplina de **Segurança da Informação** do curso de Engenharia de Computação da **Faculdade Engenheiro Salvador Arena**, 10º semestre, 2026.

---

## 👥 Grupo

| Nome | RA |
|---|---|
| Adriana Monteiro Martani | 082210012 |
| Analuz Marin Ramos | 081210034 |
| Matheus Galdino Xavier | 082210042 |
| Yasmin Laisa Maciel | 082210040 |

---

## 📌 Objetivo

Implementar uma comunicação TCP segura entre dois interlocutores — **Alice (cliente)** e **Bob (servidor)** — utilizando criptografia simétrica com **Cifra de César**, troca de chaves com o protocolo **Diffie-Hellman** e proteção assimétrica das chaves públicas DH com **RSA 4096 bits**, sem o uso de nenhuma biblioteca de criptografia pronta.

---

## 🗂️ Arquivos

| Arquivo | Descrição |
|---|---|
| `TCPServerDH.py` | Servidor TCP (Bob) — RSA 4096 + Diffie-Hellman + Cifra de César + validação de primos |
| `TCPClientDH.py` | Cliente TCP (Alice) — RSA 4096 + Diffie-Hellman + Cifra de César + validação de primos |
| `TCPServerCesar.py` | Servidor TCP com Cifra de César e chave fixa (Etapa 2) |
| `TCPClientCesar.py` | Cliente TCP com Cifra de César e chave fixa (Etapa 2) |
| `Simple_tcpServer.py` | Servidor TCP original sem criptografia (Etapa 1) |
| `Simple_tcpClient.py` | Cliente TCP original sem criptografia (Etapa 1) |

---

## 🚀 Como executar

> Todos os arquivos devem estar na mesma pasta.

**Terminal 1 — inicie o servidor primeiro:**
```bash
python TCPServerDH.py
```

**Terminal 2 — inicie o cliente depois:**
```bash
python TCPClientDH.py
```

Para simular as duas máquinas no mesmo computador, o cliente já está configurado com `127.0.0.1` (localhost). Para rodar em máquinas distintas, altere a linha `serverName` no cliente para o IP real do servidor.

> ⚠️ A geração das chaves RSA 4096 bits leva aproximadamente 30–60 segundos em cada máquina. Isso é esperado e demonstra o custo computacional real da criptografia assimétrica.

---

## 🔄 Etapas do Projeto

### Etapa 1 — Comunicação TCP simples
Implementação e teste da comunicação TCP básica entre cliente e servidor. O cliente envia uma frase em minúsculas e o servidor retorna em maiúsculas. O tráfego foi analisado com o **Wireshark**, onde o payload trafegava em texto claro.

---

### Etapa 2 — Cifra de César
Implementação da **Cifra de César** de forma autoral, sem bibliotecas externas. A cifra opera sobre os 95 caracteres ASCII imprimíveis (códigos 32–126):

```
novo_código = 32 + (código_original - 32 + chave) % 95
```

Com a criptografia ativa, o payload capturado pelo Wireshark passou a aparecer cifrado, tornando a mensagem ilegível para um interceptador.

---

### Etapa 3 — Diffie-Hellman + RSA 4096 bits

#### Diffie-Hellman
Implementação do protocolo **Diffie-Hellman** para negociação de chaves simétricas. A chave da Cifra de César passa a ser o segredo compartilhado calculado independentemente por cada lado, sem jamais trafegar pela rede.

**Fluxo da troca de chaves DH:**
```
Alice                                    Bob
  |                                       |
  |  a_privado (secreto)                  |  b_privado (secreto)
  |  A = g^a mod p                        |  B = g^b mod p
  |                                       |
  |────────── envia A ───────────────────►|
  |◄─────────── envia B ──────────────────|
  |                                       |
  |  segredo = B^a mod p                  |  segredo = A^b mod p
  |            └──────── mesmo valor ─────┘
```

#### RSA 4096 bits
Para proteger os valores **A** e **B** trocados no Diffie-Hellman contra interceptação, eles são criptografados com **RSA assimétrico de 4096 bits** antes de trafegar pela rede.

**Fluxo completo com RSA + DH + César:**
```
Alice                                        Bob
  |                                           |
  |── chave pública RSA de Alice ────────────►|
  |◄─ chave pública RSA de Bob ──────────────|
  |                                           |
  |── A cifrado com RSA (chave pública Bob) ─►|  Bob decifra → A
  |◄─ B cifrado com RSA (chave pública Alice)─|  Alice decifra → B
  |                                           |
  |  segredo = B^a mod p                      |  segredo = A^b mod p
  |                                           |
  |── mensagem cifrada com César ────────────►|
  |◄─ resposta cifrada com César ────────────|
```

**Funções RSA implementadas (todas autorais):**

| Função | Descrição |
|---|---|
| `miller_rabin()` | Teste de primalidade probabilístico |
| `gerar_primo_grande()` | Gera primo aleatório de N bits |
| `mdc_estendido()` | Algoritmo de Euclides estendido |
| `inverso_modular()` | Calcula `d` a partir de `e` e `phi` |
| `gerar_chaves_rsa()` | Gera par de chaves de 4096 bits |
| `rsa_criptografar()` | `c = valor^e mod n` |
| `rsa_decriptografar()` | `m = cifrado^d mod n` |

---

## ⏱️ Primo Fast vs Primo Slow

| | Primo Fast | Primo Slow |
|---|---|---|
| Estratégia | Para ao encontrar o 1º divisor | Conta **todos** os divisores |
| Velocidade | Muito mais rápido para não-primos | Sempre percorre até N |

Ambos os algoritmos estão integrados no `TCPServerDH.py` e `TCPClientDH.py` para validar os parâmetros do Diffie-Hellman na inicialização. O RSA utiliza o algoritmo de **Miller-Rabin** para geração eficiente de primos grandes.

---

## 🦈 Análise com Wireshark

**Mesmo PC (localhost):**
1. Abra o Wireshark como administrador
2. Selecione a interface **"Adapter for loopback traffic capture"**
3. Aplique o filtro: `tcp.port == 1300`

**PCs distintos (rede local):**
1. Abra o Wireshark no PC do servidor
2. Selecione a interface **Wi-Fi** ou **Ethernet**
3. Aplique o filtro: `tcp.port == 1300`

**Evolução do payload observado no Wireshark:**

| Etapa | Arquivo | Payload capturado |
|---|---|---|
| Etapa 1 | `Simple_tcpServer.py` | `hello world` — texto legível |
| Etapa 2 | `TCPServerCesar.py` | texto cifrado com chave fixa |
| Etapa 3 | `TCPServerDH.py` | chaves RSA + valores DH cifrados + mensagem cifrada |

---

## 🛠️ Requisitos

- Python 3.x
- Wireshark (para análise de tráfego)
- Npcap (Windows) para captura na interface loopback
- Nenhuma biblioteca externa de criptografia

---

## 🏫 Informações Acadêmicas

- **Instituição:** Faculdade Engenheiro Salvador Arena
- **Curso:** Engenharia de Computação
- **Disciplina:** Segurança da Informação
- **Semestre:** 10º — 2026
