"""File that extracts the basic info and the features from an audio file. Plots are optional."""
# Author: Laurens Van Goethem, UGent

import librosa as lr
import numpy as np
import scipy
import sklearn
from matplotlib import pyplot as plt
from librosa import display
from collections import Counter


###################################################################################################
# Plotting of features


# Plot all audio basic info
def plot_all_basic(audio, sr, name):
    plot_signal(audio, sr, name)
    plot_spectrum(audio, sr)
    plot_spectogram(audio, sr)
    plt.show()


# Plot signal
def plot_signal(audio, sr, name):
    plt.subplot(3, 1, 1)
    plt.title(name)
    lr.display.waveplot(audio, sr=sr, alpha=0.8)
    plt.xlabel('Time')


# Plot spectrum
def plot_spectrum(audio, sr):
    audio_fft = scipy.fft(audio)
    audio_fft_mag = np.absolute(audio_fft)  # spectral magnitude
    freq = np.linspace(0, sr, len(audio_fft_mag))  # frequency variable
    plt.subplot(3, 1, 2)
    plt.plot(freq[:100000], audio_fft_mag[:100000])  # magnitude spectrum, 22050 als sf= 44100
    plt.xlabel('Frequency')


# Plot spectogram
def plot_spectogram(audio, sr):
    audio_stft = lr.stft(audio)
    audio_db = lr.amplitude_to_db(abs(audio_stft))
    plt.subplot(3, 1, 3)
    lr.display.specshow(audio_db, sr=sr, x_axis='time', y_axis='hz')


###################################################################################################
# Extraction of features


# Gets all MIR features and returns it in list
def all_features(audio, sr):
    zcr = zero_crossing_rate(audio)
    rolloff = spectral_rolloff(audio, sr)
    spec_cent = spectral_centroid(audio, sr)
    spec_bw = bandwidth(audio, sr)
    chroma = chrome_freq(audio, sr)
    rmse = rmse_audio(audio, sr)
    tempo = est_tempo(audio, sr)
    return [np.mean(tempo), chroma, zcr, np.mean(rolloff), np.mean(spec_cent), np.mean(spec_bw), np.mean(rmse)]


# Gets all MIR features and plots them
def plot_all_features(audio, sr):
    zero_crossing_rate(audio)
    spectral_rolloff(audio, sr)
    spectral_centroid(audio, sr)
    bandwidth(audio, sr)
    chrome_freq(audio, sr)
    rmse_audio(audio, sr)
    plt.show()


# Gets bandwidth of audio
def bandwidth(audio, sr):
    # print("bb: ", lr.feature.spectral_bandwidth(audio, sr=sr))
    return lr.feature.spectral_bandwidth(audio, sr=sr)


# Gets onset samples
def get_onset_samples(audio, sr):
    onset_frames = lr.onset.onset_detect(audio, sr=sr)
    onset_samples = lr.frames_to_samples(onset_frames)
    return onset_samples


# Gets zero crossing rate
def zero_crossing_rate(audio):
    zero_crossings = lr.feature.zero_crossing_rate(audio + 0.0001)
    return np.max(zero_crossings)


# Gets spectral centroid
def spectral_centroid(audio, sr):
    spectral_centroids = lr.feature.spectral_centroid(audio, sr=sr)[0]

    # Computing the time variable for visualization
    frames = range(len(spectral_centroids))
    t = lr.frames_to_time(frames)

    # Plotting the Spectral Centroid along the waveform
    lr.display.waveplot(audio, sr=sr, alpha=0.4)
    plt.title('Spectral centroid')
    plt.plot(t, normalize(spectral_centroids), color='r')
    return spectral_centroids


# Normalising the spectral centroid for visualisation
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)


# Gets spectral rolloff
def spectral_rolloff(audio, sr):
    spectral_rolloff = lr.feature.spectral_rolloff(audio + 0.01, sr=sr)[0]
    lr.display.waveplot(audio, sr=sr, alpha=0.4)

    # Computing the time variable for visualization
    frames = range(len(spectral_rolloff))
    t = lr.frames_to_time(frames)

    plt.title('Spectral rolloff')
    plt.plot(t, normalize(spectral_rolloff), color='r')
    return spectral_rolloff


# Gets mel frequency cepstral coefficients
def mfcc(audio, sr):
    S = lr.feature.melspectrogram(audio, sr=sr, n_mels=125)
    log_S = lr.power_to_db(S, ref=np.max)
    plt.figure(figsize=(12, 4))
    lr.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
    plt.title('Mel power spectogram')
    plt.colorbar(format='%+02.0f db')
    plt.tight_layout()
    return log_S


# Gets chromagram
def chrome_freq(audio, sr):
    hop_length = 512
    chromagram = lr.feature.chroma_stft(audio, sr=sr, hop_length=hop_length)
    plt.figure(figsize=(15, 5))
    lr.display.specshow(chromagram, x_axis='time', y_axis='chroma', hop_length=hop_length, cmap='coolwarm')
    plt.title('Chromagram')
    list_counts = []
    for i in range(len(chromagram)):
        print(np.round(chromagram[i], 1))
        counts = np.round(chromagram[i], 1)
        for j in range(len(chromagram[i])):
            list_counts.append(counts[j])
    list_counts = Counter(list_counts)
    return list_counts.most_common()[0][0]


# Gets RMSE
def rmse_audio(x, sr):
    hop_length = 256
    frame_length = 512
    rmse = lr.feature.rms(x, frame_length=frame_length, hop_length=hop_length, center=True)
    list_rmse = []
    for i in range(len(rmse)):
        rmse = np.max(rmse)
        list_rmse.append(rmse)
    return np.max(rmse)


# Gets the tempo
def est_tempo(x, sr):
    onset_env = lr.onset.onset_strength(x, sr=sr)
    tempo = lr.beat.tempo(onset_envelope=onset_env, sr=sr)
    return tempo


###################################################################################################
# Extraction of Essentia features

# def essentia_features(audio):
#     loader = essentia.standard.Monoloader(filename=audio)
#     audio_ess = loader()
#     dance = Danceability()
#     danceability_value = dance(audio_ess)
#     keys = KeyExtractor()
#     key_value = keys(audio_ess)
#     rhyhtm = RhythmExtractor2013()
#     bpm = rhyhtm(audio_ess)
#     level = LevelExtractor()
#     level_loudness = level(audio_ess)
#     l10 = np.percentile(level_loudness, 10)
#     l90 = np.percentile(level_loudness, 90)
#     dyn = DynamicComplexity()
#     comp = dyn(audio_ess)
#     return [danceability_value[0], key_value[0], key_value[1], l10, l90, comp[0]]
