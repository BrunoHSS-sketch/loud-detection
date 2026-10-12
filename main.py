from core.calibrator import VoiceCalibrator
from core.monitor import VoiceMonitor

if __name__ == "__main__":
    calibrator = VoiceCalibrator()
    limiar_grito = calibrator.calibrate(duration=5.0)

    monitor = VoiceMonitor(shout_limit=limiar_grito)
    monitor.start(duration=10.0)