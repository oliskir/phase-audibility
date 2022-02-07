import numpy as np
import soundfile as sf

''' Compute fft of waveform.
    Distort the phase matrix randomly/maximally or 
    using a period distortion.
    Apply inverse fft to retrieve waveform.
    Outputs: 
        original_fft.wav
        modified_fft.wav
'''



def random_phase_distortion(size):
    return np.random.uniform(0, 2*np.pi, size=size)
    
def periodic_phase_distortion(size, num_periods=100):
    x = np.linspace(0, num_periods * 2 * np.pi, size)
    return np.pi * (1 + np.sin(x))
    

# set random seed for reproducibility
np.random.seed(1)

# load audio file
y, sr = sf.read("original_stereo.wav")

# select 1st channel
y = y[:,0]

# fft
z = np.fft.fft(y)

# sample random phase
# (note that the phase shift applied to the negative frequency terms
#  must match the phase shift applied to the corresponding positive 
#  frequency term but with reverse sign. Also no shift should be 
#  applied to the 0th term and the n//2 term.) 
# https://numpy.org/doc/stable/reference/generated/numpy.fft.ifft.html
n = len(z)
if n%2 != 0:
    print('Warning: script only tested for positive sample size')

# choose type of phase distortion:
a = random_phase_distortion(size=n//2-1)
###a = periodic_phase_distortion(size=n//2-1, num_periods=300)

a = np.concatenate([[0], a, [0], -a[::-1]])
rndm_phase = np.exp(1j * a)

# apply phase rotation
z *= rndm_phase

# inverse fft
ym = np.fft.ifft(z)

# remove tiny (1e-18) imaginary component arising due to 
# numerical inaccuracies in fft reversal
ym = np.real(ym)

# save output audio files
sf.write("original_fft.wav", y, sr)
sf.write("modified_fft.wav", ym, sr)
