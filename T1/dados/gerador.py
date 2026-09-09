import os

def gerar_pior_caso():
    # Garante que a pasta 'dados' existe antes de tentar salvar
    os.makedirs("dados", exist_ok=True)
    
    N = 200000
    caminho_arquivo = "dados/teste_gigante.txt"
    
    # O próprio Python cria e escreve no arquivo
    with open(caminho_arquivo, "w") as f:
        f.write(f"{N}\n")
        for i in range(1, N + 1):
            f.write(f"{i} {i + 1}\n")
            
    print(f"Sucesso! Arquivo gerado em: {caminho_arquivo}")

if __name__ == "__main__":
    gerar_pior_caso()