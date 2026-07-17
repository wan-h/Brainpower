"""
梅尔频谱

pip install librosa
pip install matplotlib
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt

############################## 获取音频信号 ###############################
y, sr = librosa.load("C:\\code\\wanhui\\Brainpower\\Code\\DL\\Audio\\zh.wav", sr=None)
print(f"sample rate: {sr}")
# y中存储的按照sr的采样率采样的数据
print(f"y length: {len(y)}, time cal: {len(y)/sr}s")
# 截取前两秒的数据
tmin, tmax = 0, 4
t = np.linspace(tmin, tmax, (tmax - tmin) * sr)
plt.figure(figsize=(12, 10))
plt.subplot(2, 2, 1)
plt.plot(t, y[int(tmin*sr): int(tmax*sr)])
plt.title('Signal')
plt.xlabel('time/s')
plt.ylabel('Amplitude')

############################## 时间域转频域 ###############################
# 快速傅里叶变换
n_fft = 2048  # 傅里叶变换的窗口大小
# stft返回的是一个复数数组,这里只需要它的模值,所以用np.abs()
ft = np.abs(librosa.stft(y[: n_fft], hop_length = n_fft + 1))
plt.subplot(2, 2, 2)
plt.plot(ft)
plt.title('Spectrum')
plt.xlabel('Frequency Bin')
plt.ylabel('Amplitude')

############################## 频谱图 ###############################
# 我们将hot_length设置为512,这里就相当于按照步进为512的窗口进行滑动计算
spec = np.abs(librosa.stft(y=y, n_fft=2048, hop_length=512))
print(f"sepc shape: {spec.shape}", spec[:,0])
# 横轴为时间,纵轴为频率,每个点的颜色表示傅里叶变化后幅值(分贝)
spec = librosa.amplitude_to_db(spec, ref=np.max)
plt.subplot(2, 2, 3)
librosa.display.specshow(spec, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spectrogram')

############################## 梅尔刻度(Mel Scale) ###############################
# Mel Scale是一种对人耳感知更加友好的频率尺度,它将声音的频率从赫兹(Hz)转换为梅尔(Mel)
spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048, hop_length=512)
mel_spect = librosa.power_to_db(spect, ref=np.max)
plt.subplot(2, 2, 4)
librosa.display.specshow(mel_spect, sr=sr, x_axis='time', y_axis='mel')
plt.title('Mel Spectrogram')
plt.colorbar(format='%+2.f dB')

plt.show()