import customtkinter as ctk
from core.calibrator import VoiceCalibrator
from core.monitor import VoiceMonitor
from ui.overlay import ShoutOverlay
import threading


class FloatingWidget:
    def __init__(self, initial_limit):
        self.shout_limit = initial_limit
        self.window = None
        self.overlay = ShoutOverlay()

        # Inicializa o monitor de áudio em background
        self.monitor = VoiceMonitor(
            shout_limit=self.shout_limit,
            on_shout_callback=self.overlay.show_alert
        )
        self.monitor_thread = None

    def start_monitoring(self):
        self.monitor_thread = threading.Thread(
            target=self.monitor.start, args=(3600,), daemon=True
        )
        self.monitor_thread.start()

    def update_limit(self, new_limit):
        self.shout_limit = new_limit
        self.monitor.shout_limit = new_limit
        if self.status_label and self.status_label.winfo_exists():
            self.status_label.configure(text=f"Limite: {new_limit:.2f} dBFS")

    def run(self):
        self.window = ctk.CTk()
        self.window.title("Loud Detection - Painel")
        self.window.geometry("240x130")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)  # Sempre visível em cima dos jogos/apps

        # Título / Status
        title_label = ctk.CTkLabel(self.window, text="🎙️ Loud Detection", font=("Arial", 13, "bold"))
        title_label.pack(pady=(10, 2))

        self.status_label = ctk.CTkLabel(
            self.window,
            text=f"Limite: {self.shout_limit:.2f} dBFS",
            font=("Arial", 11),
            text_color="gray"
        )
        self.status_label.pack(pady=(0, 8))

        # Ação de Re-calibrar
        def handle_calibrate():
            self.status_label.configure(text="Calibrando (3s)...", text_color="#ffaa00")
            self.window.update()

            def run_calib():
                calibrator = VoiceCalibrator()
                new_limit = calibrator.calibrate(duration=3.0)
                self.window.after(0, lambda: self.update_limit(new_limit))
                self.window.after(0, lambda: self.status_label.configure(text=f"Limite: {new_limit:.2f} dBFS",
                                                                         text_color="gray"))

            threading.Thread(target=run_calib, daemon=True).start()

        cal_btn = ctk.CTkButton(
            self.window,
            text="Re-calibrar",
            width=200,
            height=28,
            command=handle_calibrate,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        cal_btn.pack(pady=2)

        # Ação de Sair
        def handle_quit():
            self.window.destroy()
            exit(0)

        quit_btn = ctk.CTkButton(
            self.window,
            text="Sair",
            width=200,
            height=24,
            command=handle_quit,
            fg_color="#555555",
            hover_color="#333333"
        )
        quit_btn.pack(pady=(2, 10))

        # Inicia o monitor de áudio assim que a interface sobe
        self.start_monitoring()

        # Roda o loop principal da interface
        self.window.mainloop()