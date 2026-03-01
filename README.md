# 🔐 Comunicação TCP Segura — Cifra de César + Diffie-Hellman

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

Implementar uma comunicação TCP segura entre dois interlocutores — **Alice (cliente)** e **Bob (servidor)** — utilizando criptografia simétrica com **Cifra de César** e troca de chaves com o protocolo **Diffie-Hellman**, sem o uso de nenhuma biblioteca de criptografia pronta.

---

## 🗂️ Arquivos

| Arquivo | Descrição |
|---|---|
| `tcpServer_final.py` | Servidor TCP (Bob) — Diffie-Hellman + Cifra de César |
| `tcpClient_final.py` | Cliente TCP (Alice) — Diffie-Hellman + Cifra de César |
| `Simple_tcpServer_cesar.py` | Servidor TCP com Cifra de César e chave fixa (Etapa 2) |
| `Simple_tcpClient_cesar.py` | Cliente TCP com Cifra de César e chave fixa (Etapa 2) |
| `Simple_tcpServer.py` | Servidor TCP original sem criptografia (Etapa 1) |
| `Simple_tcpClient.py` | Cliente TCP original sem criptografia (Etapa 1) |
| `primo_fast.py` | Teste de primalidade com parada antecipada |
| `primo_slow.py` | Teste de primalidade sem parada antecipada |

---

## 🚀 Como executar

> Todos os arquivos devem estar na mesma pasta.

**Terminal 1 — inicie o servidor primeiro:**
```bash
python tcpServer_final.py
```

**Terminal 2 — inicie o cliente depois:**
```bash
python tcpClient_final.py
```

Para simular as duas máquinas no mesmo computador, o cliente já está configurado com `127.0.0.1` (localhost). Para rodar em máquinas distintas, altere a linha `serverName` no cliente para o IP real do servidor.

---

## 🔄 Etapas do Projeto

### Etapa 1 — Comunicação TCP simples
Implementação e teste da comunicação TCP básica entre cliente e servidor. O cliente envia uma frase em minúsculas e o servidor retorna em maiúsculas. O tráfego foi analisado com o **Wireshark**, onde o payload trafegava em texto claro.

### Etapa 2 — Cifra de César
Implementação da **Cifra de César** de forma autoral, sem bibliotecas externas. A cifra opera sobre os 95 caracteres ASCII imprimíveis (códigos 32–126):

```
novo_código = 32 + (código_original - 32 + chave) % 95
```

Com a criptografia ativa, o payload capturado pelo Wireshark passou a aparecer cifrado, tornando a mensagem ilegível para um interceptador.

### Etapa 3 — Diffie-Hellman
Implementação do protocolo **Diffie-Hellman** para troca de chaves simétricas, sem uso de bibliotecas de criptografia. A chave da Cifra de César passa a ser o segredo compartilhado negociado a cada conexão, sem jamais trafegar pela rede.

**Fluxo da troca de chaves:**
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
  |                                       |
  |──── mensagem cifrada (chave=segredo)─►|
  |◄─── resposta cifrada (chave=segredo)──|
```

Os parâmetros públicos `p` e `g` são validados com os algoritmos **primo fast** e **primo slow** antes de qualquer comunicação.

---

## ⏱️ Primo Fast vs Primo Slow

| | `primo_fast.py` | `primo_slow.py` |
|---|---|---|
| Estratégia | Para ao encontrar o 1º divisor | Conta **todos** os divisores |
| Velocidade | Muito mais rápido para não-primos | Sempre percorre até N |

Ambos os algoritmos estão integrados nos arquivos finais para validar os parâmetros do Diffie-Hellman na inicialização.

---

## 🦈 Análise com Wireshark

Para capturar o tráfego localmente:
1. Abra o Wireshark como administrador
2. Selecione a interface **"Adapter for loopback traffic capture"**
3. Aplique o filtro: `tcp.port == 1300`
4. Execute o servidor e o cliente

**Diferença observada no payload:**

| Etapa | Payload capturado no Wireshark |
|---|---|
| Etapa 1 (sem criptografia) | `hello world` — texto legível |
| Etapa 2 e 3 (com criptografia) | `olssv'~vysk` — texto cifrado |

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
