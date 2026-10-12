import numpy as np
import sounddevice as sd

class VoiceMonitor:
    def __init__(self, shout_limit, sample_rate=44100, blocksize=2048):
        self.shout_limit = shout_limit
        self.sample_rate = sample_rate
        self.blocksize = blocksize

    def _calculate_dbfs(self, indata):
        rms = np.sqrt(np.mean(np.square(indata)))
        if rms < 1e-12:
            return -120.0
        return 20 * np.log10(rms)

    def start(self, duration=10.0):
        print("🔴 Monitorando áudio em tempo real...")

        def monitor_callback(indata, outdata, frames, time_info, status):
            if status:
                print(status)

            dbfs_chunk = self._calculate_dbfs(indata)

            if dbfs_chunk > self.shout_limit:
                print(f"🚨 GRITO DETECTADO! ({dbfs_chunk:.2f} dBFS)")
            else:
                print(f"Volume normal: {dbfs_chunk:.2f} dBFS", end="\r")

            outdata[:] = indata

        with sd.Stream(channels=1, samplerate=self.sample_rate, blocksize=self.blocksize, callback=monitor_callback):
            sd.sleep(int(duration * 1000))