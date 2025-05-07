import serial
import json
import time
import serial.tools.list_ports
import sqlite3

def encontrar_microcontrolador():
    portas = serial.tools.list_ports.comports()
    for porta in portas:
        # print("passei aqui")
        # print(serial.tools.list_ports.ListPortInfo)
        if 'Arduino' in porta.description or 'ttyACM0' in porta.description:
            return porta.device
    return None

def conectar_serial(porta, baudrate=9600, timeout=2):
    try:
        ser = serial.Serial(porta, baudrate=baudrate, timeout=timeout)
        time.sleep(2)
        return ser
    except serial.SerialException:
        return None

def enviar_json(ser, dados):
    mensagem = json.dumps(dados)
    ser.write((mensagem + '\n').encode('utf-8'))

def receber_json(ser):
    try:
        linha = ser.readline().decode('utf-8').strip()
        if linha:
            return json.loads(linha)
    except json.JSONDecodeError:
        return None
    return None

def verificar_tag_no_banco(uid):
    conn = sqlite3.connect("tags.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM tags_autorizadas WHERE uid = ?", (uid,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

# --- EXECUÇÃO ---
porta = encontrar_microcontrolador()
# porta = "/dev/ttyACM0"
print(porta)

if porta:
    print(f"[INFO] Microcontrolador conectado na porta {porta}")
    ser = conectar_serial(porta)

    enviar_json(ser, {"cmd": "ler_nfc"})
    print("[INFO] Comando enviado: ler_nfc")

    while True:
        resposta = receber_json(ser)
        if resposta:
            if "tag" in resposta:
                uid = resposta["tag"]
                resultado = verificar_tag_no_banco(uid)
                if resultado:
                    print(f"[ACESSO LIBERADO] TAG reconhecida. Bem-vindo(a), {resultado[0]}!")
                    # Aqui você poderia acionar um relé, etc.
                else:
                    print(f"[ACESSO NEGADO] TAG não reconhecida.")
                    print(f"[SOLICITAÇÃO] UID {uid} precisa ser analisado e cadastrado manualmente.")
            elif "erro" in resposta:
                print(f"[ERRO NFC] {resposta['erro']}")
            break
else:
    print("[ERRO] Nenhum microcontrolador conectado via USB.")
