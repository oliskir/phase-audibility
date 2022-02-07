from ketos.audio.spectrogram import MagSpectrogram
import matplotlib.pyplot as plt

window = 0.02
step = 0.004

original = MagSpectrogram.from_wav("original_stft.wav", window=window, step=step)
recovered = MagSpectrogram.from_wav("recovered_stft.wav", window=window, step=step)
modified = MagSpectrogram.from_wav("modified_stft.wav", window=window, step=step)

original.plot()
recovered.plot()
modified.plot()

plt.show()
