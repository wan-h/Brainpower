"""
梅尔频谱
"""

import librosa
import matplotlib.pyplot as plt

y, sr = librosa.load("/home/vastai/workspace/AICSystem/test/src/zh.wav", sr=None)
plt.plot(y)
plt.title('Signal')
plt.xlabel('Time (samples)')
plt.ylabel('Amplitude')
plt.show()