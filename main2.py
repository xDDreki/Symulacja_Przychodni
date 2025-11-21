"""
- Dodac spoznienia/przyjscia wczesniej w umawianym
- csv z danymi o id_Pacjenta, id_gabinetu, arrival_time, service_start_time, czas_oczekiwania, service_end_time, czas_
- procesowanie danych
*lekarze przerwa od pracy
- naprawić żeby klienci nie wchodzili do gabinetu {service_time} przed zamknięciem
- dlugosci kolejki
"""
import matplotlib

matplotlib.use('TkAgg')  # or 'Qt5Agg'
import numpy as np
import simpy
import seaborn
import matplotlib.pyplot as plt
import random


class Pacjent:
    def __init__(self, id):
        self.id = id
        self.arrival_time = None
        self.service_start_time = None
        self.service_end_time = None
        self.room = None


class Gabinet:
    def __init__(self, id, env):
        self.id = id
        self.env = env
        self.patients_served = 0
        self.no_show = 0
        self.resource = simpy.Resource(env, capacity=1)


class Clinic:
    def __init__(self, env, number_of_rooms, service_time, no_show=0.2, seed=None):
        self.curr_patient_id = 1
        self.env = env
        self.service_time = service_time
        self.no_show = no_show
        self.seed = seed
        self.list_rooms = [Gabinet(id=i + 1, env=self.env) for i in range(number_of_rooms)]
        self.processed_patients = []
        if self.seed:
            random.seed(self.seed)

    def czas(self):
        hours = 9+self.env.now//60
        minutes = self.env.now%60
        if len(str(minutes))==1:
            return f"{hours}:0{minutes}"
        return f"{hours}:{minutes}"

    def generate_patients(self, room):
        def time_between_new_patients():
            return self.service_time

        while True:
            patient = Pacjent(id=f"{room.id}.{self.curr_patient_id}")

            if random.random() < self.no_show:
                print(f'Czas {self.czas()}: Pacjent {patient.id} nie pojawił w gabinecie {room.id} w ciągu 15 minut')
                patient.room = room.id
                room.no_show += 1
                self.curr_patient_id += 1
                yield self.env.timeout(15)
            else:
                patient.arrival_time = self.env.now
                print(f"Czas {self.czas()}: Pacjent {patient.id} przybył do kliniki")
                patient.room = room.id
                self.env.process(self.serve_patient(patient, room))
                self.curr_patient_id += 1
                yield self.env.timeout(time_between_new_patients())

    def serve_patient(self, patient, room):
        with room.resource.request() as request:
            yield request
            patient.service_start_time = self.env.now
            print(f"Czas {self.czas()}: Pacjent {patient.id} wchodzi do gabinetu {room.id} ")
            yield self.env.timeout(self.service_time)
            patient.service_end_time = self.env.now
            room.patients_served += 1
            print(f"Czas {self.czas()}: Pacjent {patient.id} wychodzi z gabinetu {room.id}")
            self.processed_patients.append(patient)

    def run(self, sim_time):
        for room in self.list_rooms:
            self.env.process(self.generate_patients(room))
        env.run(until=sim_time)

    def stats(self):
        def patient_bar_plot():
            patients_served_ls = []
            id_ls = []
            for room in self.list_rooms:
                patients_served_ls.append(room.patients_served)
                id_ls.append(str(room.id))
            fig = seaborn.barplot(x=id_ls, y=patients_served_ls)
            fig.set_xlabel('Gabinet')
            fig.set_ylabel('Ilosc Pacjentow')
            plt.savefig("patients_served_noshow.png")
            plt.show()

        patient_bar_plot()

#z umowieniami
env = simpy.Environment()

clinic = Clinic(env, number_of_rooms=3, service_time=20)

clinic.run(420)

clinic.stats()
