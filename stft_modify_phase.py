import numpy as np
from ketos.audio.spectrogram import MagSpectrogram
from ketos.audio.waveform import Waveform
import matplotlib.pyplot as plt

''' Compute the magnitude spectrogram and complex phase.
    Use Griffin-Lim algorithm to recover waveform.
    In one case use the actual complex phase, in the 
    other case distort the phase matrix randomly/maximally.
    Outputs: 
        original_stft.wav
        recovered_stft.wav
        modified_stft.wav
'''


window = 0.02
step = 0.004

# compute magnitude spectrogram and phase angle
s = MagSpectrogram.from_wav("original_stereo.wav", window=window, step=step,  compute_phase=True)

a = s.get_phase_angle()


def random_phase_distortion(size):
    return np.random.uniform(0, 2*np.pi, size=size)

# apply random phase distortion
am = a + random_phase_distortion(a.shape)


# recover waveform from magnitude + phase
wf = s.recover_waveform(num_iters=25, phase_angle=a)
wfm = s.recover_waveform(num_iters=25, phase_angle=am)


# load the original audio
wf_orig = Waveform.from_wav("original_stereo.wav")


# crop start and end to remove artifacts
d = wf_orig.duration()
wf_orig.crop(start=window/2, end=d-window/2)
wf.crop(start=window/2, end=d-window/2)
wfm.crop(start=window/2, end=d-window/2)


# save output wav files
wf_orig.to_wav("./original_stft.wav")
wf.to_wav("./recovered_stft.wav")
wfm.to_wav("./modified_stft.wav")
