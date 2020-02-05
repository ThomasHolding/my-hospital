import numpy.random as rnd


class Log:
    # During each process, a log book (a list of Logs) is maintained,
    # with index representing patient id.
    # We may need a database later
    def __init__(self):
        self.temps = list()
        self.infs = list()
        self.oxys = list()

    def new_log(self, temperature, lung_inf_pctg, oxy_satu):
        self.temps.append(temperature)
        self.infs.append(lung_inf_pctg)
        self.oxys.append(oxy_satu)


class Patient:
    def __init__(self, id, temperature=37, lung_inf_pctg=0, oxy_satu=1):
        self.id = id
        self.temperature = temperature
        self.lung_inf_pctg = lung_inf_pctg
        self.oxy_satu = oxy_satu
        # self.daysInHospital = 0

    def develop_symptoms(self):
        # We can later make the development relevant to age, derivative of previous development, time in hospital, etc.,
        # and different symptoms correlate to each other.
        # Each patient does this once a day, triggered when hospital monitoring happens.
        r1 = rnd.normal(0, 0.5)
        self.temperature = max(36.7, self.temperature + r1)
        # Not all patients will develop a lung infection; same holds for oxygen saturation
        self.lung_inf_pctg = max(0, min(1, self.lung_inf_pctg + r1*0.3))
        self.oxy_satu = max(0, min(1, self.oxy_satu - r1*0.1))


class Hospital:
    def __init__(self, capacity):
        self.beds_remain = capacity
        self.cur_id = 0
        self.patients = list()
        self.log_book = list()

    def take_patient(self, temperature, wuhan, lung_inf_pctg, oxy_satu):
        # Currently we take and only take patients who have been to Wuhan in the past 2 weeks,
        # with a body temperature above 37.3
        if self.beds_remain > 0 and wuhan and temperature > 37.3:
            num = self.cur_id
            #ret =
            patient = Patient(num, temperature, lung_inf_pctg, oxy_satu)
            self.patients.append(patient)
            log = Log()
            log.new_log(temperature, lung_inf_pctg, oxy_satu)
            self.log_book.append(log)
            self.cur_id += 1
            self.beds_remain -= 1
            return num
        return -1

    def monitor(self):
        death = 0
        recover = 0
        for patient in self.patients:
            if patient.id == -1:
                continue
            patient.develop_symptoms()
            if patient.temperature > 38:
                self.treat_temp(patient)
            if patient.lung_inf_pctg > 0:
                self.treat_lung(patient)
            if patient.oxy_satu < 0.98:
                self.treat_oxy(patient)
            self.log_book[patient.id].new_log(patient.temperature, patient.oxy_satu, patient.lung_inf_pctg)
            if self.discharge(patient):
                recover += 1
        return death, recover


    @staticmethod
    def treat_temp(patient):
        # We can include hospital strategies later; keep it static for now
        r = max(0, rnd.normal(1, 0.5))
        patient.temperature = max(37, patient.temperature - r)

    @staticmethod
    def treat_lung(patient):
        r = max(0, rnd.normal(1, 0.15))
        patient.lung_inf_pctg = max(0, patient.lung_inf_pctg - r)

    @staticmethod
    def treat_oxy(patient):
        r = max(0, rnd.normal(1, 0.05))
        patient.oxy_satu = min(1, patient.oxy_satu + r)

    def discharge(self, patient):
        log = self.log_book[patient.id]
        temps = log.temps
        n_days = len(temps)
        if n_days < 3:
            return False
        if temps[n_days-1] < 37.3 and temps[n_days-2] < 37.3 and temps[n_days-2] < 37.3 and patient.lung_inf_pctg < 0.05 and patient.oxy_satu > 0.98:
            print("Patient No. " + str(patient.id) + " discharged from hospital.")
            patient.id = -1
            self.beds_remain += 1
            return True
        return False

"""
my_hospital = Hospital(100)


for day in range(10):
    print("day " + str(day))
    for i in range(50):
        # We assume temperature to be independent from the other two
        # whether or not having been to Wuhan independent from all symptoms
        temp = max(36.5, rnd.normal(37, 0.5))
        wuhan = True if rnd.random() > 0.5 else False
        r = rnd.normal(0, 0.15)
        infc = min(1, max(0, r))
        oxy = min(1, max(0, 1-0.2*r))
        my_hospital.take_patient(temp, wuhan, infc, oxy)
    my_hospital.monitor()
"""
