import os
import matplotlib.pyplot as plt

processos = [1, 2, 4, 8, 12]
tempos = [5.4185, 2.6391, 1.7748, 1.5175, 1.5740]
speedup = [1.0, 2.0531, 3.0530, 3.5707, 3.4425]
ef = [1.0, 1.0266, 0.7633, 0.4463, 0.2869]
speedup_ideal = processos

os.makedirs("graficos", exist_ok=True)

plt.figure(figsize=(8, 5))
plt.plot(processos, tempos, marker="o", linewidth=2)
plt.title("Tempo de Execucao x Numero de Processos")
plt.xlabel("Numero de processos")
plt.ylabel("Tempo (s)")
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.tight_layout()
plt.savefig("graficos/tempo_execucao.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(processos, speedup, marker="o", linewidth=2, label="Speedup medido")
plt.plot(processos, speedup_ideal, linestyle="--", linewidth=2, label="Speedup ideal")
plt.title("Speedup x Numero de Processos")
plt.xlabel("Numero de processos")
plt.ylabel("Speedup")
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.legend()
plt.tight_layout()
plt.savefig("graficos/speedup.png", dpi=160)
plt.close()

plt.figure(figsize=(8, 5))
plt.plot(processos, ef, marker="o", linewidth=2)
plt.title("Eficiencia x Numero de Processos")
plt.xlabel("Numero de processos")
plt.ylabel("Eficiencia")
plt.ylim(0, 1.05)
plt.grid(True, alpha=0.3)
plt.xticks(processos)
plt.tight_layout()
plt.savefig("graficos/eficiencia.png", dpi=160)
plt.close()

print("Graficos gerados em ./graficos")
