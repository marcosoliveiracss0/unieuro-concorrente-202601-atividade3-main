import os
import matplotlib.pyplot as plt

processos = [1, 2, 4, 8, 12]
tempos = [37.5872, 19.6569, 11.2445, 8.4068, 8.3570]
speedup = [1.0000, 1.9122, 3.3427, 4.4711, 4.4977]
eficiencia = [1.0000, 0.9561, 0.8357, 0.5589, 0.3748]

saida = "graficos"
os.makedirs(saida, exist_ok=True)

plt.style.use("seaborn-v0_8")

# Grafico de tempo
plt.figure(figsize=(8, 5))
plt.plot(processos, tempos, marker="o", linewidth=2)
plt.title("Tempo de Execucao x Numero de Processos")
plt.xlabel("Processos")
plt.ylabel("Tempo (s)")
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.tight_layout()
plt.savefig(os.path.join(saida, "tempo_execucao.png"), dpi=150)
plt.close()

# Grafico de speedup
plt.figure(figsize=(8, 5))
plt.plot(processos, speedup, marker="o", linewidth=2, label="Speedup medido")
plt.plot(processos, processos, linestyle="--", linewidth=1.5, label="Speedup ideal")
plt.title("Speedup x Numero de Processos")
plt.xlabel("Processos")
plt.ylabel("Speedup")
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(saida, "speedup.png"), dpi=150)
plt.close()

# Grafico de eficiencia
plt.figure(figsize=(8, 5))
plt.plot(processos, eficiencia, marker="o", linewidth=2)
plt.title("Eficiencia x Numero de Processos")
plt.xlabel("Processos")
plt.ylabel("Eficiencia")
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.ylim(0, 1.05)
plt.tight_layout()
plt.savefig(os.path.join(saida, "eficiencia.png"), dpi=150)
plt.close()

print("Graficos gerados em ./graficos")
