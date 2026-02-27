# Mini-NET - Projeto de Redes de Computadores
Desenvolvido por João Emanuel Marinho Sousa

## Descrição

Este projeto implementa um sistema de chat funcional sobre UDP, simulando todas as camadas da rede (Aplicação, Transporte, Rede, Enlace e Física) com mecanismos de confiabilidade, roteamento e detecção de erros. Desenvolvido para a disciplina de Redes de Computadores.

O sistema é resiliente a perdas e corrupções de pacotes, utilizando:
- **Stop-and-Wait** com ACKs e timeouts
- **Números de sequência** para evitar duplicatas
- **Roteamento** com endereços virtuais (VIPs) e TTL
- **CRC32** para detecção de corrupção
- **Simulação de falhas** (20% perda, 20% corrupção)

---

## Arquitetura do Sistema

O projeto segue o modelo de camadas com encapsulamento completo:

APLICAÇÃO (JSON) → TRANSPORTE (Segmento) → REDE (Pacote) → ENLACE (Quadro) → FÍSICA (UDP)


### Componentes:

| Arquivo | Função | Camadas Implementadas |
|---------|--------|----------------------|
| `client.py` | Cliente do chat | Aplicação, Transporte, Rede, Enlace |
| `server.py` | Servidor do chat | Aplicação, Transporte, Rede, Enlace |
| `router.py` | Roteador intermediário | Rede, Enlace |
| `protocolo.py` | Biblioteca base | Todas as camadas + Física simulada |

---

## Requisitos

- Python 3.8 ou superior

---

## Como Executar

### 1. Clone o repositório 

git clone https://github.com/devsouzx/Mini-Ne.git
cd mini-net

### 2. Inicie o Servidor 
python server.py

### 3. Inicie o Servidor

python router.py

### 4. Inicie o Cliente

python client.py

### 5. Comece a conversar
Digite mensagens no terminal do cliente e veja-as aparecerem no servidor.

## Configurações Ajustáveis

No arquivo `protocolo.py`, você pode modificar o comportamento da rede simulada:

```python
# Probabilidades de falha (valores entre 0.0 e 1.0)
PROBABILIDADE_PERDA = 0.2      # 20% de chance de perda
PROBABILIDADE_CORRUPCAO = 0.2  # 20% de chance de corrupção

# Latência simulada (segundos)
LATENCIA_MIN = 0.1              # Latência mínima
LATENCIA_MAX = 0.5              # Latência máxima
```
No `client.py`, você pode ajustar o timeout:
```python
TIMEOUT = 2  # Tempo em segundos para aguardar ACK
```

## Video
video rodando o projeto

https://drive.google.com/file/d/1RtXmQdQeYLsV8PEYX_MBlNCObnfJ7HZ3/view?usp=sharing
