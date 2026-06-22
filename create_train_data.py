import numpy as np
import pandas as pd

np.random.seed(42)

SEGMENT_LENGTH = 100
SAMPLES_PER_CLASS = 200
BASE_LEVEL = 0.65
NOISE_LEVEL = 0.03

def generate_stable(n_samples):
    segments = []
    for _ in range(n_samples):
        level = BASE_LEVEL + np.random.uniform(-0.02, 0.02)
        signal = level + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_increase(n_samples):
    segments = []
    for _ in range(n_samples):
        start = BASE_LEVEL + np.random.uniform(-0.03, 0.03)
        increase = np.random.uniform(0.08, 0.15)
        end = start + increase
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_decrease(n_samples):
    segments = []
    for _ in range(n_samples):
        start = BASE_LEVEL + np.random.uniform(0.08, 0.15)
        decrease = np.random.uniform(0.08, 0.15)
        end = start - decrease
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_drop(n_samples):
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        drop_start = np.random.randint(30, 60)
        drop_end = drop_start + np.random.randint(15, 25)
        signal[drop_start:drop_end] = BASE_LEVEL - np.random.uniform(0.15, 0.25)
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_rise(n_samples):
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        rise_start = np.random.randint(30, 60)
        rise_end = rise_start + np.random.randint(15, 25)
        signal[rise_start:rise_end] = BASE_LEVEL + np.random.uniform(0.15, 0.25)
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_drop_and_rise(n_samples):
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        rise_start = np.random.randint(25, 35)
        rise_end = rise_start + np.random.randint(18, 22)
        signal[rise_start:rise_end] = BASE_LEVEL + np.random.uniform(0.15, 0.25)
        drop_start = rise_end + np.random.randint(0, 5)
        drop_end = drop_start + np.random.randint(18, 22)
        signal[drop_start:drop_end] = BASE_LEVEL - np.random.uniform(0.15, 0.25)
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

class1 = generate_stable(SAMPLES_PER_CLASS)
class2 = generate_gradual_increase(SAMPLES_PER_CLASS)
class3 = generate_gradual_decrease(SAMPLES_PER_CLASS)
class4 = generate_sharp_drop(SAMPLES_PER_CLASS)
class5 = generate_sharp_rise(SAMPLES_PER_CLASS)
class6 = generate_drop_and_rise(SAMPLES_PER_CLASS)

all_segments = np.vstack([class1, class2, class3, class4, class5, class6])
all_labels = np.array([1]*SAMPLES_PER_CLASS + [2]*SAMPLES_PER_CLASS + [3]*SAMPLES_PER_CLASS +
                      [4]*SAMPLES_PER_CLASS + [5]*SAMPLES_PER_CLASS + [6]*SAMPLES_PER_CLASS)

all_t, all_a, all_klass = [], [], []
current_t = 0
for segment, label in zip(all_segments, all_labels):
    all_t.extend(range(current_t, current_t + SEGMENT_LENGTH))
    all_a.extend(segment)
    all_klass.extend([label] * SEGMENT_LENGTH)
    current_t += SEGMENT_LENGTH

df = pd.DataFrame({'t': all_t, 'a': all_a, 'klass': all_klass})
df.to_csv('train_data_scaled.csv', index=False, header=False)