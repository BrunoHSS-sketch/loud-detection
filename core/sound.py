import numpy as np
import sounddevice as sd

class VoiceMonitor:
    def __init__(self, duration=5.5, threshold_db=-15.0):
        self.duration = duration
        self.threshold_db = threshold_db

    def _callback(self, indata, outdata, frames, time, status):
        if status:
            print(status)

        rms_chunk = np.sqrt(np.mean(np.square(indata)))

        if rms_chunk < 1e-12:
            dbfs_chunk = -120.0
        else:
            dbfs_chunk = 20 * np.log10(rms_chunk)

        if dbfs_chunk > self.threshold_db:
            print(f"⚠️ ALERTA: Volume alto detectado! ({dbfs_chunk:.2f} dBFS)")
        else:
            print(f"Volume normal: {dbfs_chunk:.2f} dBFS", end="\r")

        outdata[:] = indata

    def start(self):
        print("Monitorando áudio...")
        with sd.Stream(channels=1, callback=self._callback, blocksize=2048):
            sd.sleep(int(self.duration * 1000))
