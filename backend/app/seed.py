from app.core.database import SessionLocal
from app.models.hcp import HCP
from app.models.hcp import HCP
from app.models.interaction import Interaction

db = SessionLocal()

doctors = [
    HCP(
        name="Dr. Ananya Rao",
        specialization="Cardiology",
        hospital="Apollo Hospital",
        city="Bangalore",
        email="ananya.rao@apollo.com",
    ),
    HCP(
        name="Dr. Vivek Sharma",
        specialization="Neurology",
        hospital="Manipal Hospital",
        city="Bangalore",
        email="vivek.sharma@manipal.com",
    ),
    HCP(
        name="Dr. Priya Nair",
        specialization="Dermatology",
        hospital="Fortis Hospital",
        city="Bangalore",
        email="priya.nair@fortis.com",
    ),
    HCP(
        name="Dr. Rahul Mehta",
        specialization="Orthopedics",
        hospital="Aster CMI",
        city="Bangalore",
        email="rahul.mehta@aster.com",
    ),
    HCP(
        name="Dr. Sneha Kulkarni",
        specialization="Pediatrics",
        hospital="Narayana Health",
        city="Bangalore",
        email="sneha.kulkarni@narayana.com",
    ),
]

try:
    for doctor in doctors:
        existing = (
            db.query(HCP)
            .filter(HCP.email == doctor.email)
            .first()
        )

        if not existing:
            db.add(doctor)

    db.commit()

    print("✅ HCP seed data inserted successfully.")

finally:
    db.close()