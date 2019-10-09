import numpy as np
from scipy.io.wavfile import write
from obspy.io.segy.segy import _read_segy
from obspy import read

def norm(data):
    return (data - np.min(data))/np.ptp(data).astype('float')

segy_file = 'data/sweep.sgy'
tracks = [1,12,24,45,70,92]
rate = 3600 #Hz

stream = _read_segy(segy_file, headonly=True)
data = np.stack(t.data for t in stream.traces).T

for track in tracks:
    write('playlist/%s_sweep.wav'%track, rate, norm(data[:,track]))
    
seed_file = 'data/rumble'
rate = 60000 #Wav file sampling frequency

seed= read('%s.BHE' %seed_file)
seed+= read('%s.BHN' %seed_file)
seed+= read('%s.BHZ' %seed_file)

start = 2500000
for i, tr in enumerate(seed):
    write('playlist/ch_%s.wav'%i, rate, norm(tr.data)[start:])
