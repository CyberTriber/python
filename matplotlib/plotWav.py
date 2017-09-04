# coding=utf-8
"""
  Wav spectral plot by CyberTriber (https://github.com/CyberTriber)

==============================================================
"""
import matplotlib.pyplot as plt
import numpy as np
import wave

file = 'm.wav'

with wave.open(file,'r') as wav_file:
	#Extract Raw Audio from Wav File
	signal = wav_file.readframes(-1)
	signal = np.fromstring(signal, 'Int16')

	#Split the data into channels 
	channels = [[] for channel in range(wav_file.getnchannels())]
	for index, datum in enumerate(signal):
	    channels[index%len(channels)].append(datum)

	fs = wav_file.getframerate()
	dt = 0.0005
	NFFT = 1024
	Fs = int(1.0/dt)
	Pxx, freqs, bins, im = plt.specgram(signal, NFFT=NFFT, Fs=Fs, noverlap=900)
	plt.show()