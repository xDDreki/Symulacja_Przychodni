import simpy
from queue import PriorityQueue

env = simpy.Environment()

'''
SPIS PARAMETRÓW:

Liczba gabinetów lekarskich - count_rooms

'''

data = []
data_arrival = []

simulation_time = 480  # Czas symulacji w minutach

class Clinic:
    def __init__(self, env, count_rooms):
        self.env = env
        self.count_rooms = count_rooms
        # WAŻNE: Tworzymy liste pokoi do której może wejsć 1 pacjent
        self.rooms = [simpy.Resource(env, capacity=1) for _ in range(count_rooms)]
        self.waiting_room = []  # Kolejka priorytetowa dla pacjentów
    

    def patient_process(self, patient_id):
        print(f'Pacjent {patient_id} przybywa do przychodni o {self.env.now}')
        
        self.waiting_room.append(patient_id)

        # Szukamy pierwszego dostępnego gabinetu
        while True:
            if self.waiting_room and self.waiting_room[0] == patient_id:
                for room_id, room in enumerate(self.rooms, 1):
                    if room.count == 0:  # Sprawdzamy czy gabinet jest wolny
                        with room.request() as request:
                            yield request
                            self.waiting_room.pop(0)
                            print(f'Pacjent {patient_id} wchodzi do gabinetu {room_id} o {self.env.now}')
                            visit_duration = 30
                            yield self.env.timeout(visit_duration)
                            print(f'Pacjent {patient_id} opuszcza gabinet {room_id} o {self.env.now}')
                            data.append((patient_id, room_id, self.env.now))
                            return
            # Jeśli nie znaleziono wolnego gabinetu, czekamy chwilę i próbujemy ponownie
            yield self.env.timeout(1)

    def patient_generator(self):
        patient_id = 0
        while env.now < simulation_time-60:  # Symulacja trwa 420 minut (7 godzin)
            yield self.env.timeout(10)  # Nowy pacjent co 10 minut
            patient_id += 1
            data_arrival.append((patient_id, self.env.now))
            self.env.process(self.patient_process(patient_id))

def run_clinic_simulation(env, count_rooms):
    clinic = Clinic(env, count_rooms)
    env.process(clinic.patient_generator())
    env.run(until=simulation_time)  # Symulacja na 480 minut
    return clinic
clinic = run_clinic_simulation(env, count_rooms=2)  # Przychodnia z 3 gabinetami

print(data)

print(data_arrival)