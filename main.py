import sys
import time
from core.calibrator import VoiceCalibrator
from core.monitor import VoiceMonitor
from core.config import load_config, save_config
from ui.overlay import ShoutOverlay

if __name__ == "__main__":
    print("========================================")
    print("     INICIALIZANDO LOUD DETECTION       ")
    print("========================================")

    # Tenta carregar o limite salvo anteriormente
    limiar_grito = load_config()

    if limiar_grito is not None:
        print(f"\n[INFO] Configuração carregada com sucesso!")
        print(f"[INFO] Limite de grito atual: {limiar_grito:.2f} dBFS")
        print("[INFO] (Para re-calibrar, delete o arquivo config.json)")
    else:
        print("\n[INFO] Nenhuma calibração anterior encontrada.")
        print("[INFO] Iniciando calibração automática (fale em tom normal por 3s)...")

        calibrator = VoiceCalibrator()
        limiar_grito = calibrator.calibrate(duration=3.0)

        # Salva o novo limite no arquivo JSON para as próximas vezes
        save_config(limiar_grito)
        print(f"[SUCCESS] Calibração salva! Novo limite: {limiar_grito:.2f} dBFS")

    print("\n[INFO] O aplicativo está rodando em background. Boa jogatina!\n")

    # Inicializa o overlay visual de alerta
    overlay = ShoutOverlay()

    # Inicializa o monitor de áudio passando o callback do overlay
    monitor = VoiceMonitor(
        shout_limit=limiar_grito,
        on_shout_callback=overlay.show_alert
    )

    try:
        # Roda o monitoramento por tempo indefinitivo (ex: 24 horas contínuas)
        monitor.start(duration=86400.0)
    except KeyboardInterrupt:
        print("\n[INFO] Aplicação encerrada pelo usuário.")
        sys.exit(0)