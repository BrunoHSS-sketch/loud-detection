import sys
import threading
from core.calibrator import VoiceCalibrator
from core.monitor import VoiceMonitor
from ui.overlay import ShoutOverlay

# Detecta se é Windows ou Linux para usar a API de Tray correta
IS_WINDOWS = sys.platform.startswith('win')

if IS_WINDOWS:
    import pystray
    from PIL import Image, ImageDraw
else:
    import gi

    gi.require_version('Gtk', '3.0')
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as appindicator
    except ValueError:
        gi.require_version('AyatanaAppIndicator3', '0.1')
        from gi.repository import AyatanaAppIndicator3 as appindicator
    from gi.repository import Gtk


class SystemTrayApp:
    def __init__(self, initial_limit):
        self.shout_limit = initial_limit
        self.overlay = ShoutOverlay()

        # Inicia o monitor de áudio em background
        self.monitor = VoiceMonitor(
            shout_limit=self.shout_limit,
            on_shout_callback=self.overlay.show_alert
        )
        self.monitor_thread = None

    def start_monitoring_background(self):
        self.monitor_thread = threading.Thread(
            target=self.monitor.start, args=(3600,), daemon=True
        )
        self.monitor_thread.start()

    def update_limit(self, new_limit):
        self.shout_limit = new_limit
        self.monitor.shout_limit = new_limit
        print(f"\n[INFO] Limite atualizado dinamicamente para: {new_limit:.2f} dBFS")

    def recalibrate_action(self, *args):
        print("\n🎙️ Re-calibrando microfone (fale por 3s)...")

        def run_calib():
            calibrator = VoiceCalibrator()
            new_limit = calibrator.calibrate(duration=3.0)
            self.update_limit(new_limit)

        threading.Thread(target=run_calib, daemon=True).start()

    def quit_app(self, *args):
        print("\nSaindo da aplicação...")
        if not IS_WINDOWS:
            Gtk.main_quit()
        exit(0)

    def run(self):
        # Inicia o motor de áudio em background
        self.start_monitoring_background()

        if IS_WINDOWS:
            # Implementação via pystray para Windows
            image = Image.new('RGB', (64, 64), color=(30, 144, 255))
            dc = ImageDraw.Draw(image)
            dc.ellipse([16, 16, 48, 48], fill=(255, 255, 255))

            menu = pystray.Menu(
                pystray.MenuItem("Status: Monitorando", lambda: None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Re-calibrar Microfone", lambda: self.recalibrate_action()),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Sair", lambda: self.quit_app())
            )
            icon = pystray.Icon("LoudDetection", image, "Loud Detection", menu)
            icon.run()
        else:
            # Implementação nativa via AppIndicator para Linux (Mint XFCE, Gnome, etc)
            APPID = "loud-detection-tray"
            # Usa um ícone padrão do sistema ou icone genérico de áudio
            indicator = appindicator.Indicator.new(
                APPID,
                "audio-input-microphone-symbolic",
                appindicator.IndicatorCategory.APPLICATION_STATUS
            )
            indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

            # Constrói o menu GTK
            menu = Gtk.Menu()

            # Item de Status (apenas informativo)
            item_status = Gtk.MenuItem(label="Status: Monitorando")
            item_status.set_sensitive(False)
            menu.append(item_status)

            menu.append(Gtk.SeparatorMenuItem())

            # Item de Re-calibrar
            item_calib = Gtk.MenuItem(label="Re-calibrar Microfone (3s)")
            item_calib.connect("activate", self.recalibrate_action)
            menu.append(item_calib)

            menu.append(Gtk.SeparatorMenuItem())

            # Item de Sair
            item_quit = Gtk.MenuItem(label="Sair")
            item_quit.connect("activate", self.quit_app)
            menu.append(item_quit)

            menu.show_all()
            indicator.set_menu(menu)

            # Inicia o loop nativo do GTK para o tray no Linux
            Gtk.main()