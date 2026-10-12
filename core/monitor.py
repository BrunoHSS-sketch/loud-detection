import numpy as np
import sounddevice as sd


class VoiceMonitor:
    def __init__(self, shout_limit, sample_rate=44100, blocksize=2048, on_shout_callback=None):
        self.shout_limit = shout_limit
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self.on_shout_callback = on_shout_callback  # Função externa que será chamada no grito

    def _calculate_dbfs(self, indata):
        rms = np.sqrt(np.mean(np.square(indata)))
        if rms < 1e-12:
            return -120.0
        return 20 * np.log10(rms)

    def start(self, duration=3600.0):
        print("🔴 Monitorando áudio em tempo real em background...")

        def monitor_callback(indata, outdata, frames, time_info, status):
            if status:
                print(status)

            dbfs_chunk = self._calculate_dbfs(indata)

            if dbfs_chunk > self.shout_limit:
                print(f"\n🚨 GRITO DETECTADO! ({dbfs_chunk:.2f} dBFS)")

                # Se houver uma função cadastrada para o evento de grito, dispara ela!
                if self.on_shout_callback:
                    self.on_shout_callback()
            else:
                print(f"Volume normal: {dbfs_chunk:.2f} dBFS", end="\r")


        with sd.Stream(channels=1, samplerate=self.sample_rate, blocksize=self.blocksize, callback=monitor_callback):
            sd.sleep(int(duration * 1000))