import numpy as np
import pandas as pd

np.random.seed(42)

SEGMENT_LENGTH = 100  # точек в сегменте
SAMPLES_PER_CLASS = 100  # сегментов на каждый класс (было ~10-50)
BASE_LEVEL = 425  # фиксированный базовый уровень
NOISE_LEVEL = 12  # уровень шума

def generate_stable(n_samples, segment_length, base_level, noise_level):
    """Класс 1: Стабильный сигнал"""
    segments = []
    for _ in range(n_samples):
        level_variation = np.random.uniform(-20, 20)
        drift = np.random.uniform(-0.1, 0.1) * np.arange(segment_length)
        signal = base_level + level_variation + drift + \
                 np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_increase(n_samples, segment_length, base_level, noise_level):
    """Класс 2: Плавный рост"""
    segments = []
    for _ in range(n_samples):
        start = base_level + np.random.uniform(-30, 30)
        increase = np.random.uniform(80, 180)
        end = start + increase
        
        t = np.linspace(0, 1, segment_length)
        nonlinearity = np.random.uniform(-0.2, 0.2) * (t ** 2)
        trend = np.linspace(start, end, segment_length) + nonlinearity
        
        signal = trend + np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_decrease(n_samples, segment_length, base_level, noise_level):
    """Класс 3: Плавное падение"""
    segments = []
    for _ in range(n_samples):
        start = base_level + np.random.uniform(80, 150)
        decrease = np.random.uniform(80, 180)
        end = start - decrease
        
        t = np.linspace(0, 1, segment_length)
        nonlinearity = np.random.uniform(-0.2, 0.2) * (t ** 2)
        trend = np.linspace(start, end, segment_length) + nonlinearity
        
        signal = trend + np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_drop(n_samples, segment_length, base_level, noise_level):
    """Класс 4: Резкий обвал с возвращением"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(segment_length) * base_level
        
        drop_start = np.random.randint(30, 70)
        drop_duration = np.random.randint(15, 30)
        drop_end = min(drop_start + drop_duration, segment_length - 5)
        
        drop_amplitude = np.random.uniform(150, 250)
        signal[drop_start:drop_end] -= drop_amplitude
        
        signal += np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_rise(n_samples, segment_length, base_level, noise_level):
    """Класс 5: Резкий подъем с возвращением"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(segment_length) * base_level
        
        rise_start = np.random.randint(30, 70)
        rise_duration = np.random.randint(15, 30)
        rise_end = min(rise_start + rise_duration, segment_length - 5)
        
        rise_amplitude = np.random.uniform(150, 250)
        signal[rise_start:rise_end] += rise_amplitude
        
        signal += np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)

def generate_drop_and_rise(n_samples, segment_length, base_level, noise_level):
    """Класс 6: Обвал + подъем (или наоборот)"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(segment_length) * base_level
        
        jump1_pos = np.random.randint(10, 40)
        jump1_duration = np.random.randint(12, 20)
        jump1_amplitude = np.random.choice([-1, 1]) * np.random.uniform(120, 200)
        
        signal[jump1_pos:jump1_pos+jump1_duration] += jump1_amplitude
        
        jump2_pos = np.random.randint(60, 85)
        jump2_duration = np.random.randint(12, 20)
        jump2_amplitude = -jump1_amplitude * np.random.uniform(0.8, 1.2)
        
        signal[jump2_pos:jump2_pos+jump2_duration] += jump2_amplitude
        
        signal += np.random.normal(0, noise_level, segment_length)
        segments.append(signal)
    return np.array(segments)


class1_segments = generate_stable(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)
class2_segments = generate_gradual_increase(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)
class3_segments = generate_gradual_decrease(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)
class4_segments = generate_sharp_drop(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)
class5_segments = generate_sharp_rise(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)
class6_segments = generate_drop_and_rise(SAMPLES_PER_CLASS, SEGMENT_LENGTH, BASE_LEVEL, NOISE_LEVEL)

all_segments = np.vstack([
    class1_segments,
    class2_segments,
    class3_segments,
    class4_segments,
    class5_segments,
    class6_segments
])

all_labels = np.array(
    [1] * SAMPLES_PER_CLASS +
    [2] * SAMPLES_PER_CLASS +
    [3] * SAMPLES_PER_CLASS +
    [4] * SAMPLES_PER_CLASS +
    [5] * SAMPLES_PER_CLASS +
    [6] * SAMPLES_PER_CLASS
)

all_t = []
all_a = []
all_klass = []

current_t = 0
for segment, label in zip(all_segments, all_labels):
    all_t.extend(np.arange(current_t, current_t + SEGMENT_LENGTH))
    all_a.extend(segment)
    all_klass.extend([label] * SEGMENT_LENGTH)
    current_t += SEGMENT_LENGTH

df = pd.DataFrame({
    't': all_t,
    'a': np.round(all_a).astype(int),
    'klass': all_klass
})

df.to_csv('train_data.csv', index=False, header=False)