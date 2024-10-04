from models import db, User, Patient, Doctor, Medication, Allergy
from datetime import datetime

def seed_database():
    # Create sample users
    user1 = User(username='johndoe', password='hashed_password_1', role='patient')
    user2 = User(username='drsmith', password='hashed_password_2', role='doctor')

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()  # Commit after adding users

    # Create sample patients
    patient1 = Patient(user_id=user1.id, name='John Doe', date_of_birth=datetime(1990, 1, 1),
                       contact_info='123-456-7890', mental_health='None', exercises='Running',
                       lifestyle='Active', height=180, weight=75)

    # Create sample doctors
    doctor1 = Doctor(user_id=user2.id, name='Dr. Smith', specialization='Cardiology',
                     contact_info='987-654-3210')

    # Create sample medications
    medication1 = Medication(name='Aspirin', description='Pain reliever')
    medication2 = Medication(name='Ibuprofen', description='Anti-inflammatory')

    # Create sample allergies
    allergy1 = Allergy(name='Peanut Allergy', description='Severe allergic reaction to peanuts')

    # Add all entries to the session
    db.session.add(patient1)
    db.session.add(doctor1)
    db.session.add(medication1)
    db.session.add(medication2)
    db.session.add(allergy1)

    # Commit all changes
    db.session.commit()

if __name__ == '__main__':
    from models import app
    with app.app_context():
        db.create_all()  # Ensure all tables are created
        seed_database()  # Seed the database