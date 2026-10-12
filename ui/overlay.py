import customtkinter as ctk


class ShoutOverlay:
    def __init__(self):
        self.window = None

    def show_alert(self):
        if self.window is not None and self.window.winfo_exists():
            return  # Já está exibindo um alerta

        self.window = ctk.CTk()
        self.window.overrideredirect(True)  # Remove bordas da janela
        self.window.attributes("-topmost", True)  # Mantém acima de tudo (jogos)

        # Tamanho e posição (Ex: Centralizado no topo da tela)
        width, height = 300, 80
        screen_width = self.window.winfo_screenwidth()
        x = (screen_width // 2) - (width // 2)
        y = 30
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        # Visual do Alerta
        self.window.configure(fg_color="#1a1a1a")

        label = ctk.CTkLabel(
            self.window,
            text="⚠️ ALERTA: Fale mais baixo!",
            font=("Arial", 16, "bold"),
            text_color="#ff4d4d"
        )
        label.pack(expand=True, fill="both", padx=10, pady=10)

        # Fecha o alerta automaticamente após 2.5 segundos
        self.window.after(2500, self.close_alert)
        self.window.mainloop()

    def close_alert(self):
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            self.window = None