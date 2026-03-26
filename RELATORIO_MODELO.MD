# Relatório da Atividade 3 - Paralelização de Avaliador de Logs

**Disciplina:** Programação Concorrente e Paralela  
**Aluno(s):** Marcos de Oliveira Campos  
**Turma:** ADS04N1  
**Professor:** Rafael Marconi Ramos  
**Data:** 25/03/2026

---

# 1. Descrição do Problema

O problema consiste no processamento de múltiplos arquivos de log para extrair informações consolidadas. Cada arquivo é lido e analisado para contabilizar:

* total de linhas
* total de palavras
* total de caracteres
* contagem das palavras-chave erro, warning e info

Foi implementada uma versão serial e uma versão paralela com modelo produtor-consumidor e buffer limitado, usando processos. O produtor coloca caminhos de arquivos em uma fila limitada e os consumidores processam os arquivos em paralelo.

Objetivo da paralelização: reduzir o tempo total de execução mantendo o mesmo resultado final.

Volume de dados processado nos testes (pasta log2):

* 1000 arquivos
* 10000000 linhas
* 200000000 palavras
* 1366663305 caracteres

Algoritmo utilizado:

* varredura linear por linha e por palavra
* consolidação final por soma dos resultados parciais

Complexidade aproximada:

* tempo: O(T), onde T é o total de tokens/palavras processados
* espaço: O(P), com P processos ativos e estruturas de consolidação

---

# 2. Ambiente Experimental

| Item                        | Descrição                                            |
| --------------------------- | ---------------------------------------------------- |
| Processador                 | AMD Ryzen 5 7520U with Radeon Graphics               |
| Número de núcleos           | 4 núcleos físicos (8 threads lógicas)               |
| Memória RAM                 | 16 GB                                             |
| Sistema Operacional         | Microsoft Windows 11 Pro 10.0.26200 64 bits         |
| Linguagem utilizada         | Python                                               |
| Biblioteca de paralelização | multiprocessing (biblioteca padrão do Python)       |
| Compilador / Versão         | CPython 3.13.7                                       |

---

# 3. Metodologia de Testes

Os experimentos foram executados com o programa em modo benchmark.

Configurações testadas:

* 1 thread/processo (versão serial)
* 2 threads/processos
* 4 threads/processos
* 8 threads/processos
* 12 threads/processos

Procedimento experimental:

* foi realizada 1 execução para cada configuração (última rodada de medição)
* o tempo de execução foi medido com time.time()
* como houve 1 execução por configuração, o tempo medido coincide com a média
* a entrada foi fixa (pasta log2)
* a execução ocorreu em máquina de uso geral, sem isolamento exclusivo de carga

---

# 4. Resultados Experimentais

| Nº Threads/Processos | Tempo de Execução (s) |
| -------------------- | --------------------- |
| 1                    | 37.5872               |
| 2                    | 19.6569               |
| 4                    | 11.2445               |
| 8                    | 8.4068                |
| 12                   | 8.3570                |

---

# 5. Cálculo de Speedup e Eficiência

## Fórmulas Utilizadas

### Speedup

```
Speedup(p) = T(1) / T(p)
```

Onde:

* **T(1)** = tempo da execução serial
* **T(p)** = tempo com p threads/processos

### Eficiência

```
Eficiência(p) = Speedup(p) / p
```

Onde:

* **p** = número de threads ou processos

---

# 6. Tabela de Resultados

| Threads/Processos | Tempo (s) | Speedup | Eficiência |
| ----------------- | --------- | ------- | ---------- |
| 1                 | 37.5872   | 1.0000  | 1.0000     |
| 2                 | 19.6569   | 1.9122  | 0.9561     |
| 4                 | 11.2445   | 3.3427  | 0.8357     |
| 8                 | 8.4068    | 4.4711  | 0.5589     |
| 12                | 8.3570    | 4.4977  | 0.3748     |

---

# 7. Gráfico de Tempo de Execução

![Gráfico Tempo Execução](graficos/tempo_execucao.png)

---

# 8. Gráfico de Speedup

![Gráfico Speedup](graficos/speedup.png)

---

# 9. Gráfico de Eficiência

![Gráfico Eficiência](graficos/eficiencia.png)

---

# 10. Análise dos Resultados

O speedup não foi linear, mas houve ganho consistente até 12 processos. O melhor tempo observado foi com 12 processos (8.3570 s), com speedup 4.4977.

Análise das perguntas propostas:

* O speedup obtido foi próximo do ideal?
Não. A curva ficou abaixo da ideal, como esperado em cargas reais com overhead.

* A aplicação apresentou escalabilidade?
Sim, de forma parcial, com ganhos claros de 1 até 12 processos, embora com redução de eficiência em p maiores.

* Em qual ponto a eficiência começou a cair?
A eficiência já cai de p=2 para p=4 e continua reduzindo em p=8 e p=12.

* O número de threads ultrapassa o número de núcleos físicos da máquina?
Sim. A máquina possui 4 núcleos físicos; 8 e 12 processos ultrapassam esse limite.

* Houve overhead de paralelização?
Sim. Há custo de criação/sincronização de processos e comunicação por fila.

Possíveis causas para perdas de desempenho:

* sincronização e comunicação entre processos
* contenção de CPU quando há muitos processos ativos
* overhead fixo do modelo produtor-consumidor para o volume processado

---

# 11. Conclusão

O paralelismo trouxe ganho significativo de desempenho nesta máquina, reduzindo de 37.5872 s (serial) para 8.3570 s (12 processos), com speedup 4.4977.

Conclusões principais:

* melhor configuração observada: 12 processos
* o programa escala de forma consistente até 12 processos
* a eficiência cai com o aumento de processos, indicando overhead crescente

Melhorias possíveis:

* ajuste automático da quantidade de processos com base nos núcleos disponíveis
* balanceamento de carga por lotes
* repetições adicionais e mediana dos tempos para reduzir efeito de variação do sistema

