import numpy as np
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt

N = 1000
f1 = 20
f2 = 50
T = 1.0/1000.0

xt = np.linspace(0.0,N*T,N)
yt = np.sin(f1*2.0*np.pi*xt) + 0.8*np.sin(f2*2.0*np.pi*xt)

yf = fft(yt)
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

fig = plt.figure()

ax1 = fig.add_subplot(122)
ax1.plot(xf, 2.0/N *np.abs(yf[0:N//2]))
ax1.grid()
ax1.set_title('Frequency Domain')
ax1.set_xlabel('Frequency -->')
ax1.set_ylabel('FFT Magnitude -->')

ax2 = fig.add_subplot(121)
ax2.plot(xt,yt)
ax2.grid()
ax2.set_title('Time Domain')
ax2.set_xlabel('Time -->')
ax2.set_ylabel('Signal Amplitude -->')

plt.show()