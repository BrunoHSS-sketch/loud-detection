import customtkinter as ctk
from core.calibrator import VoiceCalibrator
import threading


class SettingsWindow:
    def __init__(self, current_limit, on_limit_updated=None):
        self.current_limit = current_limit
        self.on_limit_updated = on_limit_updated
        self.window = None

    def open(self):
        # Como o tray roda em sua própria thread, criamos a janela de config isolada
        self.window = ctk.CTk()
        self.window.title("Configurações - Loud Detection")
        self.window.geometry("380x260")
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)  # Mantém visível em cima

        title_label = ctk.CTkLabel(self.window, text="Painel de Controle", font=("Arial", 18, "bold"))
        title_label.pack(pady=15)

        self.status_label = ctk.CTkLabel(
            self.window,
            text=f"Limite de Grito Atual: {self.current_limit:.2f} dBFS",
            font=("Arial", 13)
        )
        self.status_label.pack(pady=5)

        def handle_recalibration():
            self.status_label.configure(text="🎙️ Calibrando... Fale em tom normal por 3s")
            self.window.update()

            def run_calib_thread():
                calibrator = VoiceCalibrator()
                new_limit = calibrator.calibrate(duration=3.0)
                self.current_limit = new_limit

                self.window.after(0, lambda: self.status_label.configure(
                    text=f"✅ Novo Limite: {new_limit:.2f} dBFS"
                ))
                if self.on_limit_updated:
                    self.on_limit_updated(new_limit)

            threading.Thread(target=run_calib_thread, daemon=True).start()

        cal_btn = ctk.CTkButton(
            self.window,
            text="Re-calibrar Microfone (3s)",
            command=handle_recalibration,
            fg_color="#1f538d",
            hover_color="#14375e"
        )
        cal_btn.pack(pady=15)

        close_btn = ctk.CTkButton(
            self.window,
            text="Fechar Painel",
            command=self.window.destroy,
            fg_color="gray",
            hover_color="#555555"
        )
        close_btn.pack(pady=5)

        self.window.mainloop()