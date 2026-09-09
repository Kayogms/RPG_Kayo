import os

def gerar_pior_caso():
    # Garante que a pasta 'dados' existe antes de tentar salvar
    os.makedirs("dados", exist_ok=True)
    
    N = 200000
    caminho = "dados/teste_gigante.txt"
    
    # O próprio Python cria e escreve no arquivo
    with open(caminho, "w") as f:
        f.write(f"{N}\n")
        for i in range(1, N + 1):
            f.write(f"{i} {i + 1}\n")
            
    print(f"[OK] Arquivo gerado: {caminho}")

def gerar_desconexo():
    os.makedirs("dados", exist_ok=True)
    caminho = "dados/teste_desconexo.txt"
    
    # Escreve o caso onde o andar 100 existe, mas não alcança o 1
    with open(caminho, "w") as f:
        f.write("3\n")
        f.write("1 5\n")
        f.write("5 12\n")
        f.write("50 100\n")
        
    print(f"[OK] Arquivo gerado: {caminho}")

def gerar_isolado():
    os.makedirs("dados", exist_ok=True)
    caminho = "dados/teste_isolado.txt"
    
    # Escreve o caso onde o andar 1 sequer possui escadas
    with open(caminho, "w") as f:
        f.write("2\n")
        f.write("10 20\n")
        f.write("30 40\n")
        
    print(f"[OK] Arquivo gerado: {caminho}")

if __name__ == "__main__":
    print("Iniciando a geração de todos os casos de teste...")
    gerar_pior_caso()
    gerar_desconexo()
    gerar_isolado()
    print("Todos os arquivos foram gerados com sucesso na pasta 'dados'!")