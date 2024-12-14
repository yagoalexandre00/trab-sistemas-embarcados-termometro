from flask import Flask, render_template
import csv

app = Flask(__name__)

# Caminho para o arquivo CSV
CSV_FILE = "dados_dht11.csv"

def ler_ultimo_dado():
    """Lê o último registro do arquivo CSV."""
    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            dados = list(reader)
            if dados:
                return dados[-1]  # Retorna o último registro
    except FileNotFoundError:
        return ["N/A", "N/A"]  # Retorna valores padrão se o arquivo não existir

@app.route("/")
def index():
    """Rota principal que exibe a página com os dados."""
    umidade, temperatura = ler_ultimo_dado()
    return render_template("index.html", umidade=umidade, temperatura=temperatura)

if __name__ == "__main__":
    app.run(debug=True)
