import numpy as np

def readable_time(time):
    hours = 8 + int(time // 60)
    minutes = int(time % 60)
    if len(str(minutes)) == 1:
        return f"{hours}:0{minutes}"
    return f"{hours}:{minutes}"

def randomized_service_time(mean=15, std=2, minimal_time=5):
    return max(np.random.normal(mean, std), minimal_time)

def print_statistics(data, label, unit=""):
    """
    Wypisuje statystyki dla danego zbioru danych.
    
    Args:
        data: lista lub tablica wartości
        label: nazwa statystyki (np. "czas oczekiwania na wizytę")
        unit: jednostka (np. "min", "%")
    """
    print(f"\n--- Statystyki {label} ---")
    print(f"Średnia: {np.mean(data):.2f} {unit}")
    print(f"Mediana: {np.median(data):.2f} {unit}")
    print(f"Odchylenie standardowe: {np.std(data):.2f} {unit}")
    print(f"Min: {np.min(data):.2f} {unit}")
    print(f"Max: {np.max(data):.2f} {unit}")
    print(f"\nPercentyle:")
    print(f"25. percentyl: {np.percentile(data, 25):.2f} {unit}")
    print(f"95. percentyl: {np.percentile(data, 95):.2f} {unit}")

def stats(patient_df, queue_df, service_minutes=15, total_time_hours=8):
    #Ilość obsłużonych pacjentów
    served_patients = len(patient_df)
    print(f"Ilość obsłużonych pacjentów: {served_patients}")

    n = queue_df.index.get_level_values('day').unique().shape[0]
    print(f"Liczba dni symulacji: {n}")

    daily_waiting_times = []
    for day in range(1, n+1):
        day_patients = patient_df.xs(day, level='day')
        if len(day_patients) == 0:
            continue
        
        avg_wait = day_patients["waiting_time"].mean()
        daily_waiting_times.append(avg_wait)
    
    # Statystyki czasu oczekiwania per dzień
    print_statistics(daily_waiting_times, "średni czas oczekiwania na wizytę", "min")
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

    print_statistics(daily_queue_lengths, "średnia długość kolejki per dzień")

    #Czas pracy lekarzy
    num_doctors = patient_df['room'].nunique()
    total_available_minutes_per_day = total_time_hours * 60
    
    daily_utilizations = []
    for day in range(1, n+1):
        day_patients = patient_df.xs(day, level='day')
        if len(day_patients) == 0:
            daily_utilizations.append(0)
            continue
        
        day_service_time = day_patients["service_time"].sum()
        day_utilization = (day_service_time / (total_available_minutes_per_day * num_doctors)) * 100
        daily_utilizations.append(day_utilization)
    
    # Statystyki wykorzystania
    print_statistics(daily_utilizations, "współczynnik wykorzystania lekarzy", "%")