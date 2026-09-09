import os

# Descobre exatamente onde este script (gerador.py) está salvo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_DADOS = os.path.join(BASE_DIR, "dados")

def garantir_pasta():
    os.makedirs(PASTA_DADOS, exist_ok=True)

def gerar_sample1():
    garantir_pasta()
    caminho = os.path.join(PASTA_DADOS, "teste_sample1.txt")
    with open(caminho, "w") as f:
        f.write("4\n1 4\n4 3\n4 10\n8 3\n")
    print(f"[OK] Arquivo gerado: {caminho}")

def gerar_pior_caso():
    garantir_pasta()
    caminho = os.path.join(PASTA_DADOS, "teste_gigante.txt")
    with open(caminho, "w") as f:
        f.write("200000\n")
        for i in range(1, 200001):
            f.write(f"{i} {i + 1}\n")
    print(f"[OK] Arquivo gerado: {caminho}")

def gerar_desconexo():
    garantir_pasta()
    caminho = os.path.join(PASTA_DADOS, "teste_desconexo.txt")
    with open(caminho, "w") as f:
        f.write("3\n1 5\n5 12\n50 100\n")
    print(f"[OK] Arquivo gerado: {caminho}")

def gerar_isolado():
    garantir_pasta()
    caminho = os.path.join(PASTA_DADOS, "teste_isolado.txt")
    with open(caminho, "w") as f:
        f.write("2\n10 20\n30 40\n")
    print(f"[OK] Arquivo gerado: {caminho}")

if __name__ == "__main__":
    print("Iniciando a geração de todos os casos de teste...")
    gerar_sample1()
    gerar_pior_caso()
    gerar_desconexo()
    gerar_isolado()
    print(f"Todos os arquivos foram gerados com sucesso dentro de: {PASTA_DADOS}")