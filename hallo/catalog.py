import os
import shutil
import numpy as np
import pandas as pd
from ketos.utils import ensure_dir
from ketos.audio.spectrogram import MagSpectrogram
from ketos.audio.waveform import Waveform
from ketos.data_handling.data_handling import find_wave_files
import matplotlib.pyplot as plt

''' Compute the magnitude spectrogram and complex phase.
    Use Griffin-Lim algorithm to recover waveform.
    In one case use the actual complex phase, in the 
    other case distort the phase matrix randomly/maximally.

    Input: 
        WAV files with calls from the Orcasound call catalog
        (sampled at 44100 Hz)
        https://www.orcasound.net/FordOsborneVocabulary/_SouthernVocabularyTable.html

    Output:
        WAV files with distorted / un-distorted calls
'''


input_dir = 'orcasound_call_catalog/'
output_dir = 'output_os/'
window = 0.04
step = 0.01
freq_min = 400
buffer = 1.0 #s
distort_frac = 0.6 #how large a fraction of the samples should be distorted
offset = 1.5 #cut away human speech at beginning
np.random.seed(1)
num_repeat = 1 #repeat each this many times



def random_phase_distortion(size):
    return np.random.uniform(0, 2*np.pi, size=size)


if os.path.isdir(output_dir):
    shutil.rmtree(output_dir)


# find WAV files
paths = find_wave_files(path=input_dir)


# which samples should be distorted
num_tot = num_repeat * len(paths)
num_distort = int(distort_frac * num_tot)
distort = np.concatenate([np.ones(num_distort), np.zeros(num_tot - num_distort)])
np.random.shuffle(distort)

# randomize order
order = np.arange(num_tot)
np.random.shuffle(order)


df = {'filename':[], 'orig_filename':[], 'is_modified_1':[], 'is_modified_2':[]}


counter = 0
for path in paths:
    for _ in range(num_repeat):

        print(os.path.basename(path))

        df['orig_filename'].append(path)

        # compute magnitude spectrogram and phase angle
        s = MagSpectrogram.from_wav(os.path.join(input_dir,path), window=window, step=step,  
                                    compute_phase=True, freq_min=freq_min, offset=offset)

        ##s.plot()
        ##plt.show()

        a = s.get_phase_angle()

        # apply random phase distortion
        am = a + random_phase_distortion(a.shape)

        # recover waveform from magnitude + phase
        wf = s.recover_waveform(num_iters=25, phase_angle=a)
        wfm = s.recover_waveform(num_iters=25, phase_angle=am)

        # crop start and end to remove artifacts
        d = wf.duration()
        wf.crop(start=window/2, end=d-window/2)
        wfm.crop(start=window/2, end=d-window/2)

        # randomly select distortion
        if distort[counter] == 1:
            if np.random.uniform() > 0.5:
                y1 = wf.get_data()
                y2 = wfm.get_data()
                df['is_modified_1'].append(0)
                df['is_modified_2'].append(1)
            else:
                y1 = wfm.get_data()
                y2 = wf.get_data()
                df['is_modified_1'].append(1)
                df['is_modified_2'].append(0)
        else:
            y1 = wf.get_data()
            y2 = np.copy(y1)
            df['is_modified_1'].append(0)
            df['is_modified_2'].append(0)

        # stitch together
        n_samples = int(buffer * wf.rate)
        yb = np.zeros(n_samples)
        y = np.concatenate([yb, y1, yb, y2, yb])
        wfo = Waveform(data=y, rate=wf.rate)

        # save output
        sample_id = order[counter]
        fname = f"sample_{sample_id:02d}.wav"
        df['filename'].append(fname)
        output_path = os.path.join(output_dir, fname)
        ensure_dir(output_path)
        wfo.to_wav(output_path)

        counter += 1


df = pd.DataFrame(df)
df.to_csv(os.path.join(output_dir, "truth.csv"), index=False) 

print(f"{counter} WAV files saved to {output_dir}")
