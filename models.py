from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
import os  # Add this import

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://Rehaan08:admin@localhost/health_assist')  # Update this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Association tables for many-to-many relationships
patient_doctor = db.Table('patient_doctor',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True),
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True)
)

patient_medication = db.Table('patient_medication',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True)
)

patient_allergy = db.Table('patient_allergy',
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True),
    db.Column('allergy_id', db.Integer, db.ForeignKey('allergy.id'), primary_key=True)
)

ailment_medication = db.Table('ailment_medication',
    db.Column('ailment_id', db.Integer, db.ForeignKey('ailment.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True)
)

ailment_surgery = db.Table('ailment_surgery',
    db.Column('ailment_id', db.Integer, db.ForeignKey('ailment.id'), primary_key=True),
    db.Column('surgery_id', db.Integer, db.ForeignKey('surgery.id'), primary_key=True)
)

ailment_vaccine = db.Table('ailment_vaccine',
    db.Column('ailment_id', db.Integer, db.ForeignKey('ailment.id'), primary_key=True),
    db.Column('vaccine_id', db.Integer, db.ForeignKey('vaccine.id'), primary_key=True)
)

visit_medication = db.Table('visit_medication',
    db.Column('visit_id', db.Integer, db.ForeignKey('visit.id'), primary_key=True),
    db.Column('medication_id', db.Integer, db.ForeignKey('medication.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  
    
    patient = db.relationship('Patient', back_populates='user', uselist=False)
    doctor = db.relationship('Doctor', back_populates='user', uselist=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_info = db.Column(db.String(200))
    mental_health = db.Column(LONGTEXT)
    exercises = db.Column(LONGTEXT)
    lifestyle = db.Column(LONGTEXT)
    height = db.Column(db.Integer)  # in centimeters
    weight = db.Column(db.Integer)  # in kilograms
    
    user = db.relationship('User', back_populates='patient')
    doctors = db.relationship('Doctor', secondary=patient_doctor, back_populates='patients')
    treatments = db.relationship('Treatment', back_populates='patient')
    current_medications = db.relationship('Medication', secondary=patient_medication, back_populates='patients')
    allergies = db.relationship('Allergy', secondary=patient_allergy, back_populates='patients')

## can u see this??

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Link to User
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100))
    contact_info = db.Column(db.String(200))
    
    user = db.relationship('User', back_populates='doctor')
    patients = db.relationship('Patient', secondary=patient_doctor, back_populates='doctors')
    treatments = db.relationship('Treatment', back_populates='doctor')

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20))  # 'Ongoing' or 'Completed'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    ailment_id = db.Column(db.Integer, db.ForeignKey('ailment.id'), nullable=False)
    
    patient = db.relationship('Patient', back_populates='treatments')
    doctor = db.relationship('Doctor', back_populates='treatments')
    ailment = db.relationship('Ailment', back_populates='treatments')
    visits = db.relationship('Visit', back_populates='treatment')

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(LONGTEXT)
    
    treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'), nullable=False)
    
    treatment = db.relationship('Treatment', back_populates='visits')
    medications = db.relationship('Medication', secondary=visit_medication, back_populates='visits')

class Ailment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(LONGTEXT)
    
    treatments = db.relationship('Treatment', back_populates='ailment')
    medications = db.relationship('Medication', secondary=ailment_medication, back_populates='ailments')
    surgeries = db.relationship('Surgery', secondary=ailment_surgery, back_populates='ailments')
    vaccines = db.relationship('Vaccine', secondary=ailment_vaccine, back_populates='ailments')

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(LONGTEXT)
    
    ailments = db.relationship('Ailment', secondary=ailment_medication, back_populates='medications')
    patients = db.relationship('Patient', secondary=patient_medication, back_populates='current_medications')
    visits = db.relationship('Visit', secondary=visit_medication, back_populates='medications')

class Surgery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(LONGTEXT)
    
    ailments = db.relationship('Ailment', secondary=ailment_surgery, back_populates='surgeries')

class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(LONGTEXT)
    
    ailments = db.relationship('Ailment', secondary=ailment_vaccine, back_populates='vaccines')

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(LONGTEXT)
    
    patients = db.relationship('Patient', secondary=patient_allergy, back_populates='allergies')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)