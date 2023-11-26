import csv
import sqlite3
import datetime

# Database connection
conn = sqlite3.connect('clinic.db')
cursor = conn.cursor()

# Creating tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        patient_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Doctors (
        doctor_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialty TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        appointment_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        doctor_id INTEGER,
        patient_id INTEGER,
        time_slot DATETIME,
        FOREIGN KEY(doctor_id) REFERENCES Doctors(doctor_id),
        FOREIGN KEY(patient_id) REFERENCES Patients(patient_id)
    )
''')

cursor.execute('SELECT count(*) FROM Patients')
patient_count = cursor.fetchone()[0]

cursor.execute('SELECT count(*) FROM Doctors')
doctor_count = cursor.fetchone()[0]

# If tables are empty, populate them
if patient_count == 0:
    with open('patients.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            cursor.execute("INSERT INTO Patients (name, age, gender) VALUES (?, ?, ?)",
                           (row['name'], int(row['age']), row['gender']))
    conn.commit()

if doctor_count == 0:
    with open('doctors.csv', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            cursor.execute("INSERT INTO Doctors (name, specialty) VALUES (?, ?)",
                           (row['name'], row['specialty']))
    conn.commit()



# Commit the changes and close the connection after creating tables
conn.commit()
conn.close()


class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


class Patient(Person):
    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)

    @staticmethod
    def create_patient(name, age, gender):
        new_patient = Patient(name, age, gender)
        new_patient.save_to_db()
        print("Patient added successfully.")

    def save_to_db(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Patients (name, age, gender) VALUES (?, ?, ?)',
                       (self.name, self.age, self.gender))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()
    @staticmethod
    def get_all_patients():
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Patients')
        patients = cursor.fetchall()
        conn.close()
        return patients

    def save_to_db(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Patients (name, age, gender) VALUES (?, ?, ?)',
                       (self.name, self.age, self.gender))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()

    def update_in_db(self, new_name, new_age, new_gender):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('UPDATE Patients SET name = ?, age = ?, gender = ? WHERE patient_id = ?',
                       (new_name, new_age, new_gender, self.patient_id))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()

    def delete_from_db(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Patients WHERE patient_id = ?', (self.patient_id,))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()



class Doctor(Person):
    def __init__(self, name, specialty):
        super().__init__(name, None, None)
        self.specialty = specialty

    def save_to_db(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO Doctors (name, specialty) VALUES (?, ?)',
                       (self.name, self.specialty))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()

    @staticmethod
    def get_all_doctors():
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Doctors')
        doctors = cursor.fetchall()
        conn.close()
        return doctors

    @staticmethod
    def create_doctor(name, specialty):
        new_doctor = Doctor(name, specialty)
        new_doctor.save_to_db()
        print("Doctor added successfully.")

    # Add methods for update and delete as per CRUD operations

    def update_in_db(self, new_name, new_specialty):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.cursor.execute('UPDATE Doctors SET name = ?, specialty = ? WHERE doctor_id = ?',
                              (new_name, new_specialty, self.doctor_id))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()

    def delete_from_db(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Doctors WHERE doctor_id = ?', (self.doctor_id,))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()


class Clinic:

    def get_patient_id_by_name(self, name):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT patient_id FROM Patients WHERE name = ?', (name,))
        patient_id = cursor.fetchone()
        conn.close()
        return patient_id

    def get_doctor_id_by_name(self, name):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT doctor_id FROM Doctors WHERE name = ?', (name,))
        doctor_id = cursor.fetchone()
        conn.close()
        return doctor_id

    def appointment_exists(self, doctor_id, time_slot):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('SELECT appointment_id FROM Appointments WHERE doctor_id = ? AND time_slot = ?',
                       (doctor_id, time_slot))
        existing_appointment = cursor.fetchone()
        conn.close()
        return existing_appointment

    def make_appointment(self, doctor_name, patient_name, time_slot):
        clinic = Clinic()
        doctor_id = clinic.get_doctor_id_by_name(doctor_name)
        patient_id = clinic.get_patient_id_by_name(patient_name)

        mytime = time_slot
        m = mytime.split()
        hours, mints = m[1].split(':')
        if 15 <= int(mints) <= 45:
            mints = ':30'
        elif int(mints) < 15:
            mints = ':00'
        elif int(mints) > 45:
            mints = ':00'
            h = int(hours) + 1
            hours = str(h)
        # print(m[0] + " " + hours + mints)
        if int(hours) < 8 or int(hours) > 15:
            print("You are trying to book an appointment outside of the normal working hours.")
        else:
            time_slot = m[0] + " " + hours + mints

            if doctor_id and patient_id:
                existing_appointment = clinic.appointment_exists(doctor_id[0], time_slot)

                if not existing_appointment:
                    conn = sqlite3.connect('clinic.db')
                    cursor = conn.cursor()
                    try:
                        cursor.execute('INSERT INTO Appointments (doctor_id, patient_id, time_slot) VALUES (?, ?, ?)',
                                   (doctor_id[0], patient_id[0], time_slot))
                        conn.commit()
                    except Exception as ex:
                        print(ex)
                    conn.close()
                    print("Appointment made successfully.")
                else:
                    print("An appointment already exists for the doctor at the specified time.")
            else:
                if not patient_id:
                    print("Patient not found.")
                if not doctor_id:
                    print("Doctor not found.")

    def view_all_appointments(self):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Patients.name AS patient_name, Doctors.name AS doctor_name, Appointments.time_slot 
            FROM Appointments 
            INNER JOIN Patients ON Appointments.patient_id = Patients.patient_id 
            INNER JOIN Doctors ON Appointments.doctor_id = Doctors.doctor_id
        ''')
        appointments = cursor.fetchall()
        conn.close()
        return appointments



    def update_appointment(self, appointment_id, new_time_slot):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            mytime = new_time_slot
            m = mytime.split()
            hours, mints = m[1].split(':')
            if 15 <= int(mints) <= 45:
                mints = ':30'
            elif int(mints) < 15:
                mints = ':00'
            elif int(mints) > 45:
                mints = ':00'
                h = int(hours) + 1
                hours = str(h)
            # print(m[0] + " " + hours + mints)
            if int(hours) < 8 or int(hours) > 15:
                print("You are trying to 3"
                      "book an appointment outside of the normal working hours.")
            else:
                new_time_slot = m[0] + " " + hours + mints
                cursor.execute('UPDATE Appointments SET time_slot = ? WHERE appointment_id = ?',
                           (new_time_slot, appointment_id))
                conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()
        print("Appointment updated successfully.")

    def delete_appointment(self, appointment_id):
        conn = sqlite3.connect('clinic.db')
        cursor = conn.cursor()
        try:
            cursor.execute('DELETE FROM Appointments WHERE appointment_id = ?', (appointment_id,))
            conn.commit()
        except Exception as ex:
            print(ex)
        conn.close()
        print("Appointment deleted successfully.")


def main_menu():
    print("Welcome to the Clinic Scheduler")
    while True:
        print("\nMenu:")
        print("1. Add a new Patient")
        print("2. Make an appointment")
        print("3. View all appointments")
        print("4. Update an appointment")
        print("5. Delete an appointment")
        print("6. List all Patients")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("Add a new Patient:")
            name = input("Enter patient's name: ")
            age = int(input("Enter patient's age: "))
            gender = input("Enter patient's gender M/F: ")

            # Adding a new patient
            Patient.create_patient(name, age, gender)

        elif choice == '2':
            print("Make an Appointment:")
            doctor_name = input("Enter doctor's name: ")
            patient_name = input("Enter patient's name: ")
            time_slot = input("Enter appointment time slot (YYYY-MM-DD HH:MM): ")
            # Making an appointment
            clinic = Clinic()
            clinic.make_appointment(doctor_name, patient_name, time_slot)

        elif choice == '3':
                print("View All Appointments:")
                # Viewing all appointments
                clinic = Clinic()
                all_appointments = clinic.view_all_appointments()

                if all_appointments:
                    print("List of Appointments:")
                    for appointment in all_appointments:
                        print(appointment)  # Print or format the appointment details as needed
                else:
                    print("No appointments found.")

        elif choice == '4':
            # Logic to update an appointment
            print("Update an Appointment:")

            appointment_id = int(input("Enter the ID of the appointment to update: "))
            new_time_slot = input("Enter the new time slot for the appointment (YYYY-MM-DD HH:MM): ")

            # Updating an appointment
            clinic = Clinic()
            clinic.update_appointment(appointment_id, new_time_slot)

        elif choice == '5':
            print("Delete an Appointment:")

            appointment_id = int(input("Enter the ID of the appointment to delete: "))

            # Deleting an appointment
            clinic = Clinic()
            clinic.delete_appointment(appointment_id)

        elif choice == '6':
            pwd = input("Please enter your password: ")
            if pwd == "william":
                print("List of Patients:")
                all_patients = Patient.get_all_patients()
                if all_patients:
                    print("Patient ID | Name | Age | gender")
                    for patient in all_patients:
                        print(f"{patient[0]} | {patient[1]} | {patient[2]} | {patient[3]}")
                else:
                    print("No patients found.")
            else:
                print("Please enter the valid password.")


        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main_menu()