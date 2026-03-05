import hashlib
import itertools
import string
import multiprocessing
import time


HASH_ALVO = "ca6ae33116b93e57b87810a27296fc36"


CARACTERES = string.digits

def obter_numero_nucleos():
    """
    Função para o usuário definir quantas threads de processamento deseja usar.
    """
    max_nucleos = multiprocessing.cpu_count()
    print(f" Seu processador possui {max_nucleos} núcleos disponíveis.")
    
    escolha = input(f"Quantos núcleos deseja usar para a quebra da hash? (Pressione ENTER para usar todos os {max_nucleos}): ")
    
    if escolha.strip() == "":
        return max_nucleos
    
    try:
        n = int(escolha)
        if 1 <= n <= max_nucleos:
            return n
        elif n > max_nucleos:
            print(f" Aviso: Você escolheu mais núcleos do que o disponível. Usando o limite máximo ({max_nucleos}).")
            return max_nucleos
        else:
            print(f" Aviso: Número inválido. Usando 1 núcleo.")
            return 1
    except ValueError:
        print(f" Aviso: Entrada não reconhecida. Usando o limite máximo ({max_nucleos}).")
        return max_nucleos

def testar_prefixo(args):
    """
    Função trabalhadora: Recebe um prefixo inicial e o tamanho total da senha.
    Ex: Se receber ('05', 4), vai testar de '0500' até '0599'.
    """
    prefixo, tamanho_total = args
    tamanho_restante = tamanho_total - len(prefixo)
    
    for combinacao in itertools.product(CARACTERES, repeat=tamanho_restante):

        tentativa = prefixo + "".join(combinacao)
        
        if hashlib.md5(tentativa.encode('utf-8')).hexdigest() == HASH_ALVO:
            return tentativa 
            
    return None 

if __name__ == '__main__':
    print("--- INICIANDO SISTEMA DE FORÇA BRUTA PARALELA ---")
    nucleos_escolhidos = obter_numero_nucleos()
    
    print(f"\n🔥 Iniciando ataque usando {nucleos_escolhidos} núcleos...")
    inicio = time.time()
    encontrada = False

    for tamanho_atual in range(1, 10):
        print(f"  -> Testando combinações com {tamanho_atual} dígitos...")
        
        if tamanho_atual <= 2:
            tarefas = [("", tamanho_atual)] 
        else:
            prefixos_duplos = ["".join(p) for p in itertools.product(CARACTERES, repeat=2)]
            tarefas = [(prefixo, tamanho_atual) for prefixo in prefixos_duplos]


        with multiprocessing.Pool(processes=nucleos_escolhidos) as pool:

            for resultado in pool.imap_unordered(testar_prefixo, tarefas):
                if resultado:
                    print("\n" + "="*50)
                    print(f" O HASH FOI QUEBRADO.")
                    print(f" A SENHA É: {resultado}")
                    print("="*50 + "\n")
                    encontrada = True
                    pool.terminate() 
                    break
        
        if encontrada:
            break
            
    fim = time.time()
    tempo_gasto = round(fim - inicio, 2)
    
    if encontrada:
        print(f" Tempo total gasto: {tempo_gasto} segundos.")
    else:

        print(f"\n A senha não foi encontrada nas combinações de 1 a 12 dígitos.")
