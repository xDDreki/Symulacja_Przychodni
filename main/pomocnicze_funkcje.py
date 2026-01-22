import numpy as np

def readable_time(time):
    hours = 8 + int(time // 60)
    minutes = int(time % 60)
    if len(str(minutes)) == 1:
        return f"{hours}:0{minutes}"
    return f"{hours}:{minutes}"

def randomized_service_time(mean=15, std=2, minimal_time=5):
    return max(np.random.normal(mean, std), minimal_time)

def stats(patient_df, queue_df, n, service_minutes):
    #czas oczekiwania na wizyte
    avg_waiting_time = patient_df["waiting_time"].mean()
    print(f"Średni czas oczekiwania: {round(avg_waiting_time,2)} min")
    median_waiting = patient_df['waiting_time'].median()
    print(f"Mediana czasu oczekiwania: {round(median_waiting,2)} min")
    min_waiting = patient_df['waiting_time'].min()
    print(f"Minimalna wartość czasu oczekiwania: {round(min_waiting,2)} min")
    max_waiting = patient_df['waiting_time'].max()
    print(f"Maksymalna wartość czasu oczekiwania: {round(max_waiting,2)} min")
    #Ilość obsużonych pacjentów
    served_patients = len(patient_df)
    print(f"Ilość obsłużonych pacjentów: {served_patients}")
    #Długość kolejki
    #Średnia
    df = queue_df.sort_values('time').reset_index()
    total_time = service_minutes * n
    weighted_sum = 0

    for i in range(len(df)-1):
        queue_len = df.loc[i, 'total_queue_length']

        current_time = df.loc[i, 'time']
        next_time = df.loc[i+1, 'time']

        duration = next_time - current_time
        weighted_sum += queue_len * duration
        last_time = current_time

    weighted_sum += df['total_queue_length'].iloc[-1] * (total_time - last_time)
    avg_queue = weighted_sum / total_time
    print(f"Średnia długość kolejki: {round(avg_queue,2)}")
    max_queue = df['total_queue_length'].max()
    print(f"Maksymalna długość kolejki: {max_queue}")
    #Czas pracy lekarzy
    total_service_time = patient_df["service_time"].sum()
    print(f"Średnia ilość godzin dziennie poświęconych na obsługę pacjentów: {round(total_service_time/60/n, 2)} h")