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

* 25 arquivos
* 250000 linhas
* 5000000 palavras
* 34170981 caracteres

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
| 1                    | 5.4185                |
| 2                    | 2.6391                |
| 4                    | 1.7748                |
| 8                    | 1.5175                |
| 12                   | 1.5740                |

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
| 1                 | 5.4185    | 1.0000  | 1.0000     |
| 2                 | 2.6391    | 2.0531  | 1.0266     |
| 4                 | 1.7748    | 3.0530  | 0.7633     |
| 8                 | 1.5175    | 3.5707  | 0.4463     |
| 12                | 1.5740    | 3.4425  | 0.2869     |

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

O speedup não foi linear, mas houve ganho consistente até 8 processos. O melhor tempo foi com 8 processos (1.5175 s), com speedup 3.5707.

Análise das perguntas propostas:

* O speedup obtido foi próximo do ideal?
Não. A curva ficou abaixo da ideal, como esperado em cargas reais com overhead.

* A aplicação apresentou escalabilidade?
Sim, de forma parcial, com ganhos claros até 8 processos.

* Em qual ponto a eficiência começou a cair?
A queda fica mais evidente a partir de 4 processos e continua em 8 e 12.

* O número de threads ultrapassa o número de núcleos físicos da máquina?
Sim. A máquina possui 4 núcleos físicos; 8 e 12 processos ultrapassam esse limite.

* Houve overhead de paralelização?
Sim. Há custo de criação/sincronização de processos e comunicação por fila.

Possíveis causas para perdas de desempenho:

* sincronização e comunicação entre processos
* contenção de CPU quando há muitos processos ativos
* overhead fixo do modelo produtor-consumidor para o volume de 25 arquivos

---

# 11. Conclusão

O paralelismo trouxe ganho significativo de desempenho nesta máquina, reduzindo de 5.4185 s (serial) para 1.5175 s (8 processos), com speedup 3.5707.

Conclusões principais:

* melhor configuração observada: 8 processos
* o programa escala bem até 8 processos
* com 12 processos houve regressão em relação a 8, indicando saturação/overhead

Melhorias possíveis:

* ajuste automático da quantidade de processos com base nos núcleos disponíveis
* balanceamento de carga por lotes
* repetições adicionais e mediana dos tempos para reduzir efeito de variação do sistema

