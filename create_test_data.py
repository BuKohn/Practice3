import csv
import random

data = []

BASE_LEVEL = 400

for t in range(1001):
    a = int(50 * random.random() + BASE_LEVEL)
    data.append((t, a))

    if 100 <= t <= 200:
        BASE_LEVEL += 1
    elif 300 <= t <= 400:
        BASE_LEVEL -= 0.25
    elif t == 540:
        BASE_LEVEL = 200
    elif t == 560:
        BASE_LEVEL = 400
    elif t == 735:
        BASE_LEVEL = 600
    elif t == 760:
        BASE_LEVEL = 400
    elif t == 930:
        BASE_LEVEL = 650
    elif t == 950:
        BASE_LEVEL = 300
    elif t == 970:
        BASE_LEVEL = 400

with open('data.csv', 'w', newline='', encoding='utf-8') as file:
    csv.writer(file).writerows(data)
