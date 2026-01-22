import numpy as np

def readable_time(time):
    hours = 8 + int(time // 60)
    minutes = int(time % 60)
    if len(str(minutes)) == 1:
        return f"{hours}:0{minutes}"
    return f"{hours}:{minutes}"

def randomized_service_time(mean=15, std=2, minimal_time=5):
    return max(np.random.normal(mean, std), minimal_time)

def stats(patient_df, queue_df, service_minutes=15, total_time_hours=8):
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


    #Długość kolejki - średnia ważona per dzień
    daily_queue_lengths = []
    
    n = queue_df.index.get_level_values('day').unique().shape[0]  # Liczba dni w danych
    print(f"Liczba dni symulacji: {n}")

    for day in range(1, n+1):
        day_queue = queue_df.xs(day, level='day').sort_index()  # Sortuj po czasie!
        if len(day_queue) == 0:
            continue
            
        # Oblicz średnią ważoną dla tego dnia
        time_intervals = []
        queue_lengths = []
        
        # Wyodrębnij czasy i długości kolejki
        for time, length in day_queue.itertuples():
            time_intervals.append(time)
            queue_lengths.append(length)
        
        # Oblicz wagi (czas trwania dla każdej obserwacji)
        weighted_sum = 0
        for i in range(len(time_intervals) - 1):
            duration = time_intervals[i + 1] - time_intervals[i]
            weighted_sum += queue_lengths[i] * duration
        
        # Dodaj ostatni interwał do końca dnia
        last_duration = service_minutes - time_intervals[-1]
        weighted_sum += queue_lengths[-1] * last_duration
        
        daily_average = weighted_sum / service_minutes
        daily_queue_lengths.append(daily_average)
    
    # Średnia ze wszystkich dni
    overall_avg_queue = np.mean(daily_queue_lengths) if daily_queue_lengths else 0
    print(f"Średnia długość kolejki: {round(overall_avg_queue, 2)}")

    #Czas pracy lekarzy
    num_doctors = patient_df['room'].nunique()
    total_service_time = patient_df["service_time"].sum()
    total_available_minutes =  total_time_hours * 60 * n * num_doctors
    doctor_utilization = (total_service_time / total_available_minutes) * 100
    print(f"Średnie wykorzystanie lekarza: {round(doctor_utilization, 2)} %")