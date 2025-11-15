import simpy


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
    def __init__(self, env, number_of_rooms, service_time):
        self.curr_patient_id = 1
        self.env = env
        self.service_time = service_time

        temp_rooms = [Gabinet(id=i + 1, env=self.env) for i in range(number_of_rooms)]
        self.rooms = simpy.Store(self.env, capacity=3)
        for room in temp_rooms:
            self.rooms.put(room)
        self.processed_patients =[]

    def generate_patients(self):

        def time_between_new_patients():
            #uzupelnic poissona
            return 10

        while True:
            patient = Pacjent(id=self.curr_patient_id)
            patient.arrival_time = self.env.now
            print(f"Czas {self.env.now}: Patient {patient.id} arrives")
            self.env.process(self.serve_patient(patient))
            self.curr_patient_id += 1
            yield self.env.timeout(time_between_new_patients())

    def serve_patient(self, patient):
        room = yield self.rooms.get()
        print(f"Czas {self.env.now}: Patient {patient.id} enters Room {room.id} ")

        yield self.env.timeout(self.service_time)

        patient.service_end_time = self.env.now
        room.patients_served += 1
        print(f"Czas {self.env.now}: Patient {patient.id} leaves Room {room.id}")
        self.processed_patients.append(patient)
        yield self.rooms.put(room)

    def run(self, sim_time):
        self.env.process(self.generate_patients())
        env.run(until=sim_time)

    def stats(self):
        #uzupelnic
        pass


env = simpy.Environment()

clinic = Clinic(env, number_of_rooms=3, service_time=15)

clinic.run(420) 


