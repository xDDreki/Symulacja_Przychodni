import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
import numpy as np
import simpy
import seaborn
import matplotlib.pyplot as plt


class Pacjent:
    def __init__(self, id):
        self.id = id
        self.arrival_time = None
        self.service_start_time = None
        self.service_end_time = None

class Gabinet:
    def __init__(self, id, env):
        self.id = id
        self.env = env
        self.patients_served = 0

class Clinic:
    def __init__(self, env, number_of_rooms, service_time, lambda_per_hour=14, seed=None):
        self.curr_patient_id = 1
        self.env = env
        self.service_time = service_time
        self.lambda_per_hour = lambda_per_hour
        self.seed = seed
        self.list_rooms = [Gabinet(id=i + 1, env=self.env) for i in range(number_of_rooms)]
        self.rooms = simpy.Store(self.env, capacity=3)
        for room in self.list_rooms:
            self.rooms.put(room)
        self.processed_patients = []

    def generate_patients(self):
        def time_between_new_patients():
            if self.seed:
                np.random.seed(self.seed)
            return np.random.poisson(self.lambda_per_hour)

        while True:
            patient = Pacjent(id=self.curr_patient_id)
            patient.arrival_time = self.env.now
            print(f"Czas {self.env.now}: Pacjent {patient.id} przybył do kliniki")
            self.env.process(self.serve_patient(patient))
            self.curr_patient_id += 1
            yield self.env.timeout(time_between_new_patients())

    def serve_patient(self, patient):
        room = yield self.rooms.get()
        print(f"Czas {self.env.now}: Pacjent {patient.id} wchodzi do gabinetu {room.id} ")

        yield self.env.timeout(self.service_time)

        patient.service_end_time = self.env.now
        room.patients_served += 1
        print(f"Czas {self.env.now}: Pacjent {patient.id} wychodzi z gabinetu {room.id}")
        self.processed_patients.append(patient)
        yield self.rooms.put(room)

    def run(self, sim_time):
        self.env.process(self.generate_patients())
        env.run(until=sim_time)

    def stats(self):
        def patient_bar_plot():
            patients_served_ls = []
            id_ls = []
            for room in self.list_rooms:
                patients_served_ls.append(room.patients_served)
                id_ls.append(str(room.id))
            seaborn.barplot(x=id_ls, y=patients_served_ls)
            plt.savefig("patients_served.png")
            plt.close()
        patient_bar_plot()


env = simpy.Environment()

clinic = Clinic(env, number_of_rooms=3, service_time=15)

clinic.run(420)

clinic.stats()
