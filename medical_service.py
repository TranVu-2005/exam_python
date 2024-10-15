from datetime import datetime
from db_connection import connect_to_db

# Add patients
def add_patients(db):
    patients = []
    for _ in range(3):
        full_name = input("Enter patient's full name: ")
        birth_year = input("Enter birth year: ")
        gender = input("Enter gender: ")
        address = input("Enter address: ")
        phone_number = input("Enter phone number: ")
        email = input("Enter email: ")
        patients.append({
            "full_name": full_name,
            "birth_year": int(birth_year),  # Lưu lại năm sinh dưới dạng số nguyên
            "gender": gender,
            "address": address,
            "phone_number": phone_number,
            "email": email
        })
    db.patients.insert_many(patients)
    print("Patients added successfully!")

# Add doctors
def add_doctors(db):
    doctors = []
    for _ in range(5):
        full_name = input("Enter doctor's full name: ")
        specialization = input("Enter specialization: ")
        phone_number = input("Enter phone number: ")
        email = input("Enter email: ")
        years_of_experience = int(input("Enter years of experience: "))
        doctors.append({
            "full_name": full_name,
            "specialization": specialization,
            "phone_number": phone_number,
            "email": email,
            "years_of_experience": years_of_experience
        })
    db.doctors.insert_many(doctors)
    print("Doctors added successfully!")

# Add appointments
def add_appointments(db):
    for _ in range(3):
        patient_name = input("Enter patient's name: ")
        doctor_name = input("Enter doctor's name: ")
        appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
        reason = input("Enter reason for appointment: ")

        patient = db.patients.find_one({"full_name": patient_name})
        doctor = db.doctors.find_one({"full_name": doctor_name})

        if patient and doctor:
            appointment = {
                "patient_id": patient["_id"],
                "doctor_id": doctor["_id"],
                "appointment_date": datetime.strptime(appointment_date, "%Y-%m-%d"),
                "reason": reason,
                "status": "pending"
            }
            db.appointments.insert_one(appointment)
            print("Appointment added successfully!")
        else:
            print("Patient or Doctor not found.")

# Generate report
def generate_report(db):
    appointments = db.appointments.find()
    print("No | Patient Name | Birth Year | Gender | Address | Doctor Name | Reason      | Date")
    print("---|--------------|------------|--------|---------|-------------|-------------|------------")
    for i, appointment in enumerate(appointments, start=1):
        patient = db.patients.find_one({"_id": appointment["patient_id"]})
        doctor = db.doctors.find_one({"_id": appointment["doctor_id"]})
        print(f"{i} | {patient['full_name']} | {patient['birth_year']} | "
              f"{patient['gender']} | {patient['address']} | {doctor['full_name']} | "
              f"{appointment['reason']} | {appointment['appointment_date'].strftime('%Y-%m-%d')}")

# Get today's appointments
def get_todays_appointments(db):
    today = datetime.today().date()
    appointments = db.appointments.find({"appointment_date": {"$gte": datetime(today.year, today.month, today.day)}})
    print("Address   | No | Patient Name | Birth Year | Gender | Doctor Name | Status   | Note")
    print("----------|----|--------------|------------|--------|-------------|----------|------")
    for i, appointment in enumerate(appointments, start=1):
        patient = db.patients.find_one({"_id": appointment["patient_id"]})
        doctor = db.doctors.find_one({"_id": appointment["doctor_id"]})
        print(f"{patient['address']} | {i} | {patient['full_name']} | {patient['birth_year']} | "
              f"{patient['gender']} | {doctor['full_name']} | {appointment['status']} | ")

# Main menu
def main():
    db = connect_to_db()
    while True:
        print("\nMedical Service System")
        print("1. Add Patients")
        print("2. Add Doctors")
        print("3. Add Appointments")
        print("4. Generate Report")
        print("5. Get Today's Appointments")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_patients(db)
        elif choice == '2':
            add_doctors(db)
        elif choice == '3':
            add_appointments(db)
        elif choice == '4':
            generate_report(db)
        elif choice == '5':
            get_todays_appointments(db)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
