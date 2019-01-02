import obspy
import numpy as np
from scipy.io.wavfile import write
from obspy.io.segy.segy import _read_segy

# Exemple 1

filename = 'chrirp_chirp.sgy'
tracks = {1,12,24,45,70,92}
rate = 3200 #Hz

stream = _read_segy(filename, headonly=True)
data = np.stack(t.data for t in stream.traces).T

for track in tracks:
    scaled = np.int16(data[:,track])
    scaled_norm = scaled / scaled.ptp(0)*2**4
    write('%s_sweep.wav'%track, rate, scaled_norm[::1])


# Exemple 2

files = 'IRIS_STATION'
rate = 8000 #Wave file sampling frequency

seed= obspy.read('%s.BHE' %filename)
seed+= obspy.read('%s.BHN' %filename)
seed+= obspy.read('%s.BHZ' %filename)

for i, tr in enumerate(seed):
    write('%s_%s_boom_whoom.wav'%(i,files), rate, np.int16(tr.data)[::1])