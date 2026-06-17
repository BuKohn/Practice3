import numpy as np
import pandas as pd

np.random.seed(42)

SEGMENT_LENGTH = 100
SAMPLES_PER_CLASS = 200
BASE_LEVEL = 425
NOISE_LEVEL = 15

def generate_stable(n_samples):
    """Класс 1: Стабильный сигнал"""
    segments = []
    for _ in range(n_samples):
        level = np.random.choice([425, 525])
        signal = level + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_increase(n_samples):
    """Класс 2: Плавный рост"""
    segments = []
    for _ in range(n_samples):
        start = np.random.uniform(400, 450)
        end = start + np.random.uniform(80, 120)
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_decrease(n_samples):
    """Класс 3: Плавное падение"""
    segments = []
    for _ in range(n_samples):
        start = np.random.uniform(500, 550)
        end = start - np.random.uniform(80, 120)
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_drop(n_samples):
    """Класс 4: Резкий обвал"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        drop_start = np.random.randint(40, 60)
        drop_end = drop_start + np.random.randint(15, 25)
        signal[drop_start:drop_end] = np.random.uniform(200, 250, drop_end - drop_start)
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_rise(n_samples):
    """Класс 5: Резкий подъем"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        rise_start = np.random.randint(30, 50)
        rise_end = rise_start + np.random.randint(20, 30)
        signal[rise_start:rise_end] = np.random.uniform(600, 650, rise_end - rise_start)
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_drop_and_rise(n_samples):
    """Класс 6: Подъем + обвал"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        rise_start = np.random.randint(25, 35)
        rise_end = rise_start + np.random.randint(18, 22)
        signal[rise_start:rise_end] = np.random.uniform(650, 700, rise_end - rise_start)
        
        drop_start = rise_end + np.random.randint(0, 5)
        drop_end = drop_start + np.random.randint(18, 22)
        signal[drop_start:drop_end] = np.random.uniform(300, 350, drop_end - drop_start)
        
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

# Создаем DataFrame
all_t, all_a, all_klass = [], [], []
current_t = 0

for segment, label in zip(all_segments, all_labels):
    all_t.extend(range(current_t, current_t + SEGMENT_LENGTH))
    all_a.extend(np.round(segment).astype(int))
    all_klass.extend([label] * SEGMENT_LENGTH)
    current_t += SEGMENT_LENGTH

df = pd.DataFrame({'t': all_t, 'a': all_a, 'klass': all_klass})
df.to_csv('val_data.csv', index=False, header=False)