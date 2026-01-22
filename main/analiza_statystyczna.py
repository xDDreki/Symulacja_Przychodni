import numpy as np
from scipy import stats
import pandas as pd

def z_test_waiting_times(df_bez_um, df_z_um, alpha=0.05):
    
    # Pobranie czasów oczekiwania
    waiting_times_bez_um = df_bez_um['waiting_time'].values
    waiting_times_z_um = df_z_um['waiting_time'].values
    
    # Statystyki opisowe
    mean_bez_um = np.mean(waiting_times_bez_um)
    mean_z_um = np.mean(waiting_times_z_um)
    std_bez_um = np.std(waiting_times_bez_um, ddof=1)
    std_z_um = np.std(waiting_times_z_um, ddof=1)
    n_bez_um = len(waiting_times_bez_um)
    n_z_um = len(waiting_times_z_um)
    
    print("=" * 60)
    print("Z-TEST: PORÓWNANIE CZASÓW OCZEKIWANIA")
    print("=" * 60)
    print(f"\n--- System BEZ UMAWIANIA ---")
    print(f"Średnia: {mean_bez_um:.2f} min")
    print(f"Odchylenie std: {std_bez_um:.2f} min")
    print(f"Liczba obserwacji: {n_bez_um}")
    
    print(f"\n--- System Z UMAWIANIEM ---")
    print(f"Średnia: {mean_z_um:.2f} min")
    print(f"Odchylenie std: {std_z_um:.2f} min")
    print(f"Liczba obserwacji: {n_z_um}")
    
    print(f"\n--- RÓŻNICA ---")
    print(f"Δμ = {mean_bez_um - mean_z_um:.2f} min")
    
    # Z-test
    se = np.sqrt((std_bez_um**2 / n_bez_um) + (std_z_um**2 / n_z_um))
    z_statistic = (mean_bez_um - mean_z_um) / se
    
    # P-value dla testu jednostronnego (H1: μ_z_um < μ_bez_um)
    p_value = 1 - stats.norm.cdf(z_statistic)  # prawy ogon
    
    print(f"\n--- WYNIKI Z-TESTU ---")
    print(f"Z-statystyka: {z_statistic:.4f}")
    print(f"P-value (jednostronny): {p_value:.6f}")
    print(f"Poziom istotności alfa: {alpha}")
    
    print(f"\n--- WNIOSKI ---")
    if p_value < alpha:
        print(f"ODRZUCAMY H0 (p < {alpha})")
        print(f"System Z UMAWIANIEM ma ISTOTNIE NIŻSZE czasy oczekiwania")
    else:
        print(f"NIE ODRZUCAMY H0 (p ≥ {alpha})")
        print(f"Brak istotnych różnic w czasach oczekiwania")
    
    print("=" * 60)
    
    return {
        'z_statistic': z_statistic,
        'p_value': p_value,
        'mean_bez_um': mean_bez_um,
        'mean_z_um': mean_z_um,
        'std_bez_um': std_bez_um,
        'std_z_um': std_z_um,
        'odrzuc_h0': p_value < alpha
    }