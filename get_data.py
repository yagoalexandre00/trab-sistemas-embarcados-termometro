import serial
import csv

# Configurações da porta serial
PORTA = "COM4"  # Substitua pela porta onde o Arduino está conectado (ex.: "COM3" no Windows ou "/dev/ttyUSB0" no Linux)
BAUDRATE = 9600  # Deve ser o mesmo do Arduino
TIMEOUT = 2      # Timeout para a leitura serial

# Configuração inicial
NOME_ARQUIVO = "dados_dht11.csv"  # Nome do arquivo CSV a ser salvo

# Inicializa a comunicação serial
try:
    ser = serial.Serial(PORTA, BAUDRATE, timeout=TIMEOUT)
    print(f"Conectado à porta {PORTA} com baudrate {BAUDRATE}.")
except serial.SerialException as e:
    print(f"Erro ao conectar à porta {PORTA}: {e}")
    exit()

# Criação do arquivo CSV e adição do cabeçalho
with open(NOME_ARQUIVO, mode="w", newline="") as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerow(["Umidade (%)", "Temperatura (*C)"])  # Cabeçalho

print(f"Arquivo '{NOME_ARQUIVO}' criado com sucesso.")

# Loop para leitura dos dados e gravação no CSV
try:
    while True:
        # Lê uma linha da porta serial
        linha = ser.readline().decode("utf-8").strip()
        if linha:  # Verifica se recebeu algo válido
            print(f"Dado recebido: {linha}")

            # Verifica e extrai os valores de umidade e temperatura
            if "Umidade:" in linha and "Temperatura:" in linha:
                try:
                    partes = linha.split(" / ")
                    umidade = partes[0].split(":")[1].strip().replace("%", "")
                    temperatura = partes[1].split(":")[1].strip().replace("*C", "")

                    # Salva os dados no CSV
                    with open(NOME_ARQUIVO, mode="a", newline="") as arquivo_csv:
                        escritor = csv.writer(arquivo_csv)
                        escritor.writerow([umidade, temperatura])

                    print(f"Dados salvos: Umidade={umidade}%, Temperatura={temperatura}°C")
                except (IndexError, ValueError) as e:
                    print(f"Erro ao processar linha recebida: {e}")

except KeyboardInterrupt:
    print("\nInterrompido pelo usuário.")
    ser.close()
    print("Conexão serial encerrada.")
