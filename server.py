import socket
import time

from protocol import Segmento, Pacote, Quadro, enviar_pela_rede_ruidosa

# ==============================
# CONFIGURAÇÕES
# ==============================

VIP_SERVIDOR = "SERVIDOR"
VIP_CLIENTE = "HOST_A"

MAC_SERVIDOR = "AA:BB:CC:DD:EE:02"
MAC_ROUTER = "AA:BB:CC:DD:EE:FF"

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000

ROUTER_IP = "127.0.0.1"
ROUTER_PORT = 5000

TTL_INICIAL = 5

# ==============================
# SOCKET UDP
# ==============================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((SERVER_IP, SERVER_PORT))

print("\033[96m=== SERVIDOR INICIADO ===\033[0m")

seq_esperado = 0

while True:
    bytes_recebidos, endereco_origem = sock.recvfrom(4096)

    # ==============================
    # CAMADA DE ENLACE
    # ==============================

    quadro_recebido, valido = Quadro.deserializar(bytes_recebidos)

    if not valido:
        print("\033[91m[SERVIDOR] Quadro corrompido (CRC inválido). Descartando.\033[0m")
        continue

    pacote = quadro_recebido["data"]
    segmento = pacote["data"]

    # ==============================
    # CAMADA DE TRANSPORTE
    # ==============================

    if segmento["is_ack"]:
        continue

    seq_recebido = segmento["seq_num"]

    if seq_recebido == seq_esperado:
        print(f"\033[92m[SERVIDOR] Mensagem recebida (SEQ={seq_recebido})\033[0m")

        json_aplicacao = segmento["payload"]

        print(f'\033[92m{json_aplicacao["sender"]}: {json_aplicacao["message"]}\033[0m')

        seq_esperado = 1 - seq_esperado

    else:
        print(f"\033[93m[SERVIDOR] Duplicata detectada (SEQ={seq_recebido}). Reenviando ACK.\033[0m")

    # ==============================
    # ENVIO DE ACK
    # ==============================

    segmento_ack = Segmento(
        seq_num=seq_recebido,
        is_ack=True,
        payload=None
    )

    pacote_ack = Pacote(
        src_vip=VIP_SERVIDOR,
        dst_vip=VIP_CLIENTE,
        ttl=TTL_INICIAL,
        segmento_dict=segmento_ack.to_dict()
    )

    quadro_ack = Quadro(
        src_mac=MAC_SERVIDOR,
        dst_mac=MAC_ROUTER,
        pacote_dict=pacote_ack.to_dict()
    )

    bytes_ack = quadro_ack.serializar()

    print(f"\033[94m[SERVIDOR] Enviando ACK para SEQ={seq_recebido}\033[0m")

    enviar_pela_rede_ruidosa(
        sock,
        bytes_ack,
        (ROUTER_IP, ROUTER_PORT)
    )