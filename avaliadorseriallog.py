import os
import time
import random
import string
import argparse
import multiprocessing as mp


# ===============================
# Consolidação dos resultados
# ===============================

def consolidar_resultados(resultados):
    total_linhas = 0
    total_palavras = 0
    total_caracteres = 0

    contagem_global = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for r in resultados:
        total_linhas += r["linhas"]
        total_palavras += r["palavras"]
        total_caracteres += r["caracteres"]

        for chave in contagem_global:
            contagem_global[chave] += r["contagem"][chave]

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem_global
    }


# ===============================
# Processamento de arquivo
# ===============================

def processar_arquivo(caminho, carga_cpu=100):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.readlines()

    total_linhas = len(conteudo)
    total_palavras = 0
    total_caracteres = 0

    contagem = {
        "erro": 0,
        "warning": 0,
        "info": 0
    }

    for linha in conteudo:
        palavras = linha.split()

        total_palavras += len(palavras)
        total_caracteres += len(linha)

        for p in palavras:
            if p in contagem:
                contagem[p] += 1

        # Simulação de processamento pesado parametrizável
        for _ in range(carga_cpu):
            pass

    return {
        "linhas": total_linhas,
        "palavras": total_palavras,
        "caracteres": total_caracteres,
        "contagem": contagem
    }


def _produtor(arquivos, fila_tarefas, num_consumidores):
    for caminho in arquivos:
        fila_tarefas.put(caminho)

    for _ in range(num_consumidores):
        fila_tarefas.put(None)


def _consumidor(fila_tarefas, fila_resultados, carga_cpu):
    while True:
        caminho = fila_tarefas.get()
        if caminho is None:
            break

        fila_resultados.put(processar_arquivo(caminho, carga_cpu=carga_cpu))


def executar_paralelo(pasta, num_processos=2, tamanho_buffer=32, exibir=True, carga_cpu=100):
    arquivos = [
        os.path.join(pasta, arquivo)
        for arquivo in os.listdir(pasta)
        if os.path.isfile(os.path.join(pasta, arquivo))
    ]

    if not arquivos:
        raise ValueError(f"Nenhum arquivo encontrado na pasta '{pasta}'.")

    fila_tarefas = mp.Queue(maxsize=tamanho_buffer)
    fila_resultados = mp.Queue()

    inicio = time.time()

    produtor = mp.Process(
        target=_produtor,
        args=(arquivos, fila_tarefas, num_processos),
        daemon=False,
    )
    consumidores = [
        mp.Process(
            target=_consumidor,
            args=(fila_tarefas, fila_resultados, carga_cpu),
            daemon=False,
        )
        for _ in range(num_processos)
    ]

    produtor.start()
    for c in consumidores:
        c.start()

    resultados = [fila_resultados.get() for _ in range(len(arquivos))]

    produtor.join()
    for c in consumidores:
        c.join()

    fim = time.time()
    resumo = consolidar_resultados(resultados)

    if exibir:
        print("\n=== EXECUÇÃO PARALELA ===")
        print(f"Processos consumidores: {num_processos}")
        print(f"Arquivos processados: {len(resultados)}")
        print(f"Tempo total: {fim - inicio:.4f} segundos")

        print("\n=== RESULTADO CONSOLIDADO ===")
        print(f"Total de linhas: {resumo['linhas']}")
        print(f"Total de palavras: {resumo['palavras']}")
        print(f"Total de caracteres: {resumo['caracteres']}")

        print("\nContagem de palavras-chave:")
        for k, v in resumo["contagem"].items():
            print(f"  {k}: {v}")

    return resumo, fim - inicio


def executar_serial_com_tempo(pasta, carga_cpu=100):
    resultados = []

    inicio = time.time()

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho):
            resultados.append(processar_arquivo(caminho, carga_cpu=carga_cpu))

    fim = time.time()
    resumo = consolidar_resultados(resultados)
    return resumo, fim - inicio


def benchmark(pasta, processos, repeticoes=3, tamanho_buffer=32, carga_cpu=100):
    estatisticas = {}
    resumo_referencia = None

    for p in processos:
        tempos = []
        for _ in range(repeticoes):
            if p == 1:
                resumo, tempo = executar_serial_com_tempo(pasta, carga_cpu=carga_cpu)
            else:
                resumo, tempo = executar_paralelo(
                    pasta,
                    num_processos=p,
                    tamanho_buffer=tamanho_buffer,
                    exibir=False,
                    carga_cpu=carga_cpu,
                )

            if resumo_referencia is None:
                resumo_referencia = resumo
            tempos.append(tempo)

        media = sum(tempos) / len(tempos)
        estatisticas[p] = {
            "tempos": tempos,
            "media": media,
        }

        print(f"\n=== RESULTADO p={p} ===")
        print("Tempos: " + ", ".join(f"{t:.4f}s" for t in tempos))
        print(f"Média: {media:.4f}s")
        print("=== RESULTADO CONSOLIDADO ===")
        print(f"Total de linhas: {resumo['linhas']}")
        print(f"Total de palavras: {resumo['palavras']}")
        print(f"Total de caracteres: {resumo['caracteres']}")
        print("Contagem de palavras-chave:")
        for k, v in resumo["contagem"].items():
            print(f"  {k}: {v}")

    return resumo_referencia, estatisticas



# ===============================
# Execução serial
# ===============================

def executar_serial(pasta, carga_cpu=100):
    resultados = []

    inicio = time.time()

    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)

        resultado = processar_arquivo(caminho, carga_cpu=carga_cpu)
        resultados.append(resultado)

    fim = time.time()

    resumo = consolidar_resultados(resultados)

    print("\n=== EXECUÇÃO SERIAL ===")
    print(f"Arquivos processados: {len(resultados)}")
    print(f"Tempo total: {fim - inicio:.4f} segundos")

    print("\n=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {resumo['linhas']}")
    print(f"Total de palavras: {resumo['palavras']}")
    print(f"Total de caracteres: {resumo['caracteres']}")

    print("\nContagem de palavras-chave:")
    for k, v in resumo["contagem"].items():
        print(f"  {k}: {v}")

    return resumo


# ===============================
# Main
# ===============================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Avaliador serial/paralelo de arquivos de log"
    )
    parser.add_argument("--pasta", default="log2", help="Pasta dos arquivos de log")
    parser.add_argument(
        "--modo",
        choices=["serial", "paralelo", "benchmark"],
        default="benchmark",
        help="Modo de execução",
    )
    parser.add_argument(
        "--processos",
        type=int,
        default=max(2, mp.cpu_count() // 2),
        help="Quantidade de processos consumidores no modo paralelo",
    )
    parser.add_argument(
        "--buffer",
        type=int,
        default=32,
        help="Tamanho do buffer limitado no modelo produtor-consumidor",
    )
    parser.add_argument(
        "--repeticoes",
        type=int,
        default=3,
        help="Quantidade de repetições para cada configuração no benchmark",
    )
    parser.add_argument(
        "--carga",
        type=int,
        default=20,
        help="Carga de CPU simulada por linha (quanto maior, mais lento)",
    )
    args = parser.parse_args()

    if args.modo == "serial":
        print("Executando versão serial...")
        executar_serial(args.pasta, carga_cpu=args.carga)
    elif args.modo == "paralelo":
        print("Executando versão paralela...")
        executar_paralelo(
            args.pasta,
            num_processos=args.processos,
            tamanho_buffer=args.buffer,
            carga_cpu=args.carga,
        )
    else:
        configuracoes = [1, 2, 4, 8, 12]
        print("Executando benchmark...")
        resumo, estatisticas = benchmark(
            args.pasta,
            configuracoes,
            repeticoes=args.repeticoes,
            tamanho_buffer=args.buffer,
            carga_cpu=args.carga,
        )

        print("\n=== BENCHMARK (MÉDIA) ===")
        t1 = estatisticas[1]["media"]
        for p in configuracoes:
            media = estatisticas[p]["media"]
            speedup = t1 / media
            eficiencia = speedup / p
            print(
                f"p={p:>2} | média={media:.4f}s | speedup={speedup:.4f} | eficiência={eficiencia:.4f}"
            )

        print("\n=== RESULTADO CONSOLIDADO (REFERÊNCIA) ===")
        print(f"Total de linhas: {resumo['linhas']}")
        print(f"Total de palavras: {resumo['palavras']}")
        print(f"Total de caracteres: {resumo['caracteres']}")
        print("Contagem de palavras-chave:")
        for k, v in resumo["contagem"].items():
            print(f"  {k}: {v}")
