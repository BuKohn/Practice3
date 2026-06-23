import numpy as np
import pandas as pd

np.random.seed(42)

# ПАРАМЕТРЫ В МАСШТАБЕ РЕАЛЬНЫХ ДАННЫХ
SEGMENT_LENGTH = 100
SAMPLES_PER_CLASS = 200
BASE_LEVEL = 0.60        # ← как в реальных данных
NOISE_LEVEL = 0.003      # ← очень маленький шум (0.5%)
JUMP_AMPLITUDE = 0.3     # ← скачок в 100 раз больше шума

def generate_stable(n_samples):
    """Класс 1: Стабильный — только шум, без тренда"""
    segments = []
    for _ in range(n_samples):
        level = BASE_LEVEL + np.random.uniform(-0.01, 0.01)
        signal = level + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_increase(n_samples):
    """Класс 2: Плавный рост от 0.6 до 0.8-1.0"""
    segments = []
    for _ in range(n_samples):
        start = BASE_LEVEL + np.random.uniform(-0.02, 0.02)
        end = start + np.random.uniform(0.15, 0.35)
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_gradual_decrease(n_samples):
    """Класс 3: Плавное падение от 0.8-1.0 до 0.6"""
    segments = []
    for _ in range(n_samples):
        start = BASE_LEVEL + np.random.uniform(0.15, 0.35)
        end = start - np.random.uniform(0.15, 0.35)
        trend = np.linspace(start, end, SEGMENT_LENGTH)
        signal = trend + np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

def generate_sharp_changes(n_samples):
    """Класс 4: Резкие скачки (обвал/подъем/оба)"""
    segments = []
    for _ in range(n_samples):
        signal = np.ones(SEGMENT_LENGTH) * BASE_LEVEL
        
        # 1-3 скачка в случайных позициях
        n_jumps = np.random.randint(1, 4)
        for _ in range(n_jumps):
            pos = np.random.randint(20, 80)
            duration = np.random.randint(5, 15)  # Короткие скачки!
            amplitude = np.random.choice([-1, 1]) * JUMP_AMPLITUDE
            signal[pos:pos+duration] += amplitude
        
        signal += np.random.normal(0, NOISE_LEVEL, SEGMENT_LENGTH)
        segments.append(signal)
    return np.array(segments)

# Генерация
class1 = generate_stable(SAMPLES_PER_CLASS)
class2 = generate_gradual_increase(SAMPLES_PER_CLASS)
class3 = generate_gradual_decrease(SAMPLES_PER_CLASS)
class4 = generate_sharp_changes(SAMPLES_PER_CLASS)

all_segments = np.vstack([class1, class2, class3, class4])
all_labels = np.array([1]*SAMPLES_PER_CLASS + [2]*SAMPLES_PER_CLASS + 
                      [3]*SAMPLES_PER_CLASS + [4]*SAMPLES_PER_CLASS)

# Сохранение
all_t, all_a, all_klass = [], [], []
current_t = 0
for segment, label in zip(all_segments, all_labels):
    all_t.extend(range(current_t, current_t + SEGMENT_LENGTH))
    all_a.extend(segment)
    all_klass.extend([label] * SEGMENT_LENGTH)
    current_t += SEGMENT_LENGTH

df = pd.DataFrame({'t': all_t, 'a': all_a, 'klass': all_klass})
df.to_csv('train_data_scaled.csv', index=False, header=False)

print(f"✓ Создан train_data_real_scale.csv")
print(f"Диапазон: [{df['a'].min():.3f}, {df['a'].max():.3f}]")
print(f"Соотношение скачок/шум: {JUMP_AMPLITUDE/NOISE_LEVEL:.0f}x")