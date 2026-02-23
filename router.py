import socket
from protocol import Quadro, enviar_pela_rede_ruidosa

# ==============================
# CONFIGURAÇÕES DO ROTEADOR
# ==============================

ROUTER_IP = "127.0.0.1"
ROUTER_PORT = 5000

MAC_ROUTER = "AA:BB:CC:DD:EE:FF"

# TABELA DE ROTEAMENTO ESTÁTICA
TABELA_ROTEAMENTO = {
    "SERVIDOR": ("127.0.0.1", 6000, "AA:BB:CC:DD:EE:02"),
    "HOST_A": ("127.0.0.1", 4000, "AA:BB:CC:DD:EE:01")
}

# ==============================
# SOCKET UDP
# ==============================

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ROUTER_IP, ROUTER_PORT))

print("\033[96m=== ROTEADOR INICIADO ===\033[0m")

while True:
    bytes_recebidos, endereco_origem = sock.recvfrom(4096)

    # ==============================
    # CAMADA DE ENLACE
    # ==============================

    quadro_recebido, valido = Quadro.deserializar(bytes_recebidos)

    if not valido:
        print("\033[91m[ROTEADOR] Quadro corrompido (CRC inválido). Descartando.\033[0m")
        continue

    pacote = quadro_recebido["data"]

    # ==============================
    # CAMADA DE REDE (TTL)
    # ==============================

    pacote["ttl"] -= 1

    if pacote["ttl"] <= 0:
        print("\033[91m[ROTEADOR] TTL expirado. Descartando pacote.\033[0m")
        continue

    destino_vip = pacote["dst_vip"]

    if destino_vip not in TABELA_ROTEAMENTO:
        print("\033[91m[ROTEADOR] Destino desconhecido. Descartando.\033[0m")
        continue

    ip_destino, porta_destino, mac_destino = TABELA_ROTEAMENTO[destino_vip]

    print(f"\033[94m[ROTEADOR] Encaminhando pacote para {destino_vip}\033[0m")

    # ==============================
    # REENCAPSULAMENTO (ENLACE)
    # ==============================

    novo_quadro = Quadro(
        src_mac=MAC_ROUTER,
        dst_mac=mac_destino,
        pacote_dict=pacote
    )

    bytes_envio = novo_quadro.serializar()

    enviar_pela_rede_ruidosa(
        sock,
        bytes_envio,
        (ip_destino, porta_destino)
    )