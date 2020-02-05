from tkinter import *
from tkinter import ttk
from CleverTom import *

my_hospital = Hospital(100)
num_new_patient = 0
day = 0


def take_patient_internal():
    try:
        temp = float(temperature.get())
        wu = True if wuhan.get()=='T' else False
        lung = float(lung_infc.get())
        oxy = float(oxy_satu.get())
        global my_hospital
        global diagose_result
        global num_new_patient
        res = my_hospital.take_patient(temp, wu, lung, oxy)
        if res < 0:
            diagose_result.set("We recommend a self quarantine.")
        else:
            num_new_patient += 1
            diagose_result.set("Patient No. " + str(res) + " taken, temperature: " + str(temp) + ", lung infection: " + str(lung) + ", oxygen saturation: " + str(oxy))
    except ValueError:
        pass


def hospital_report():
    # Monitor and EOD report,
    # need to disable input entries and buttons
    global my_hospital
    global num_new_patient
    global day
    day += 1
    death, recover = my_hospital.monitor()
    report.set("day " + str(day) + ": " + str(num_new_patient) + " new patients, " + str(death) + " new death(s), " + str(recover) + " discharged.")
    num_new_patient = 0


def clear_entry():
    temp_entry.delete(0, 'end')
    wu_entry.delete(0, 'end')
    lung_entry.delete(0, 'end')
    oxy_entry.delete(0, 'end')
    temp_entry.focus()


root = Tk()
root.title("My Hospital")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

diagose_result = StringVar()
report = StringVar()
temperature = StringVar()
wuhan = StringVar()
lung_infc = StringVar()
oxy_satu = StringVar()

ttk.Label(mainframe, text="Input Patient Info:").grid(column=1, row=1, sticky=W)

ttk.Label(mainframe, text="Temperature").grid(column=1, row=2, sticky=W)
temp_entry = ttk.Entry(mainframe, width=4, textvariable=temperature)
temp_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Have been to Wuhan? (T/F)").grid(column=3, row=2, sticky=(W,E))
wu_entry = ttk.Entry(mainframe, width=4, textvariable=wuhan)
wu_entry.grid(column=4, row=2, sticky=E)

ttk.Label(mainframe, text="Lung infection (%)").grid(column=1, row=3, sticky=W)
lung_entry = ttk.Entry(mainframe, width=4, textvariable=lung_infc)
lung_entry.grid(column=2, row=3, sticky=(W,E))

ttk.Label(mainframe, text="Oxygen saturation").grid(column=3, row=3, sticky=E)
oxy_entry = ttk.Entry(mainframe, width=4, textvariable=oxy_satu)
oxy_entry.grid(column=4, row=3, sticky=(W,E))

ttk.Button(mainframe, text="Diagnose", command=take_patient_internal).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Next Patient", command=clear_entry).grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, textvariable=diagose_result).grid(column=1, row=5, columnspan=3, sticky=(W, E))

ttk.Label(mainframe, text="That's all the patients we got today. Click to finish:").grid(column=1, row=6, columnspan=2, sticky=(W,E))
ttk.Button(mainframe, text="Finish", command=hospital_report).grid(column=1, row=7, sticky=(W,E))

ttk.Label(mainframe, textvariable=report).grid(column=1, row=8, columnspan=3, sticky=(W,E))

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)
temp_entry.focus()

#root.bind('<Return>', take_patient_internal)

root.mainloop()