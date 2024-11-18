import tkinter as tk
from main import iniciar_conversa
import threading

# Função para rodar a IA em uma thread separada
def iniciarapp():
    threading.Thread(target=iniciar_conversa, daemon=True).start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Assistente Feriado")
root.geometry("600x400")

# Layout do app
label_titulo = tk.Label(root, text="Feriado - Assistente Virtual", font=("Arial", 20))
label_titulo.pack(pady=10)

botao_iniciar = tk.Button(root, text="Iniciar Conversa 🎤", command=iniciarapp, bg="blue", fg="white", font=("Arial", 15), height=2, width=20)
botao_iniciar.pack(pady=20)

# Exibe o app
root.mainloop()

