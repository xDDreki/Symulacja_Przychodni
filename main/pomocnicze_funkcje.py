import numpy as np

def readable_time(time):
    hours = 8 + int(time // 60)
    minutes = int(time % 60)
    if len(str(minutes)) == 1:
        return f"{hours}:0{minutes}"
    return f"{hours}:{minutes}"

def randomized_service_time(mean=15, std=2, minimal_time=5):
    return max(np.random.normal(mean, std), minimal_time)
