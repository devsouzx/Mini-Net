import socket
import json
import time

from protocol import Segmento, Pacote, Quadro, enviar_pela_rede_ruidosa

# ==============================
# CONFIGURAÇÕES
# ==============================

VIP_ORIGEM = "HOST_A"
VIP_DESTINO = "SERVIDOR"

MAC_ORIGEM = "AA:BB:CC:DD:EE:01"
MAC_DESTINO = "AA:BB:CC:DD:EE:FF"
TTL_INICIAL = 5
TIMEOUT = 2

ROUTER_IP = "127.0.0.1"
ROUTER_PORT = 5000

CLIENT_PORT = 4000

# ==============================
# SOCKET UDP
# ==============================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", CLIENT_PORT))
sock.settimeout(TIMEOUT)

print("\033[96m=== CLIENTE INICIADO ===\033[0m")

seq_atual = 0

while True:
    mensagem = input("Digite a mensagem: ")

    # ==============================
    # CAMADA DE APLICAÇÃO (JSON)
    # ==============================
    json_aplicacao = {
        "type": "chat",
        "sender": VIP_ORIGEM,
        "message": mensagem,
        "timestamp": time.time()
    }

    # ==============================
    # CAMADA DE TRANSPORTE
    # ==============================
    segmento = Segmento(
        seq_num=seq_atual,
        is_ack=False,
        payload=json_aplicacao
    )

    # ==============================
    # CAMADA DE REDE
    # ==============================
    pacote = Pacote(
        src_vip=VIP_ORIGEM,
        dst_vip=VIP_DESTINO,
        ttl=TTL_INICIAL,
        segmento_dict=segmento.to_dict()
    )

    # ==============================
    # CAMADA DE ENLACE
    # ==============================
    quadro = Quadro(
        src_mac=MAC_ORIGEM,
        dst_mac=MAC_DESTINO,
        pacote_dict=pacote.to_dict()
    )

    bytes_quadro = quadro.serializar()

    # ==============================
    # STOP-AND-WAIT
    # ==============================

    while True:
        print(f"\033[93m[CLIENTE] Enviando mensagem com SEQ={seq_atual}\033[0m")

        enviar_pela_rede_ruidosa(
            sock,
            bytes_quadro,
            (ROUTER_IP, ROUTER_PORT)
        )

        try:
            bytes_recebidos, _ = sock.recvfrom(4096)

            quadro_recebido, valido = Quadro.deserializar(bytes_recebidos)

            if not valido:
                print("\033[91m[CLIENTE] ACK corrompido. Ignorando.\033[0m")
                continue

            pacote_recebido = quadro_recebido["data"]
            segmento_recebido = pacote_recebido["data"]

            if segmento_recebido["is_ack"] and segmento_recebido["seq_num"] == seq_atual:
                print(f"\033[92m[CLIENTE] ACK recebido para SEQ={seq_atual}\033[0m")
                seq_atual = 1 - seq_atual
                break

        except socket.timeout:
            print("\033[93m[CLIENTE] Timeout! Retransmitindo...\033[0m")