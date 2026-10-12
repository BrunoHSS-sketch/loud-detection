import numpy as np
import sounddevice as sd


class VoiceCalibrator:
    def __init__(self, sample_rate=44100, blocksize=2048):
        self.sample_rate = sample_rate
        self.blocksize = blocksize

    def _calculate_dbfs(self, indata):
        rms = np.sqrt(np.mean(np.square(indata)))
        if rms < 1e-12:
            return -120.0
        return 20 * np.log10(rms)

    def calibrate(self, duration=3.0, threshold_offset=15.0):
        print("🎙️ INICIANDO CALIBRAÇÃO...")
        print("Fale em tom normal...")

        dbfs_samples = []

        def cal_callback(indata, outdata, frames, time_info, status):
            if status:
                print(status)
            dbfs = self._calculate_dbfs(indata)
            dbfs_samples.append(dbfs)


        with sd.Stream(channels=1, samplerate=self.sample_rate, blocksize=self.blocksize, callback=cal_callback):
            sd.sleep(int(duration * 1000))

        reference_db = np.mean(dbfs_samples)
        shout_limit = min(reference_db + threshold_offset, -2.0)

        print(f"✅ Calibração ok! Fala ref: {reference_db:.2f} dBFS | Limite de grito ajustado: {shout_limit:.2f} dBFS")
        return shout_limit