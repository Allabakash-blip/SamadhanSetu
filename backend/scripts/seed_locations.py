from app.database.connection import SessionLocal
from app.models import State, District

STATES = [
("Andhra Pradesh","AP"),("Arunachal Pradesh","AR"),("Assam","AS"),("Bihar","BR"),
("Chhattisgarh","CG"),("Goa","GA"),("Gujarat","GJ"),("Haryana","HR"),
("Himachal Pradesh","HP"),("Jharkhand","JH"),("Karnataka","KA"),("Kerala","KL"),
("Madhya Pradesh","MP"),("Maharashtra","MH"),("Manipur","MN"),("Meghalaya","ML"),
("Mizoram","MZ"),("Nagaland","NL"),("Odisha","OD"),("Punjab","PB"),
("Rajasthan","RJ"),("Sikkim","SK"),("Tamil Nadu","TN"),("Telangana","TG"),
("Tripura","TR"),("Uttar Pradesh","UP"),("Uttarakhand","UK"),("West Bengal","WB"),
("Andaman and Nicobar Islands","AN"),("Chandigarh","CH"),
("Dadra and Nagar Haveli and Daman and Diu","DN"),("Delhi","DL"),
("Jammu and Kashmir","JK"),("Ladakh","LA"),("Lakshadweep","LD"),("Puducherry","PY")
]

JHARKHAND_DISTRICTS = [
"Bokaro","Chatra","Deoghar","Dhanbad","Dumka","East Singhbhum","Garhwa","Giridih",
"Godda","Gumla","Hazaribagh","Jamtara","Khunti","Koderma","Latehar","Lohardaga",
"Pakur","Palamu","Ramgarh","Ranchi","Sahibganj","Seraikela-Kharsawan","Simdega","West Singhbhum"
]

db = SessionLocal()
try:
    for name, code in STATES:
        if not db.query(State).filter(State.name == name).first():
            db.add(State(name=name, code=code))
    db.commit()
    jh = db.query(State).filter(State.code == "JH").first()
    for name in JHARKHAND_DISTRICTS:
        if not db.query(District).filter(District.state_id == jh.id, District.name == name).first():
            db.add(District(state_id=jh.id, name=name))
    db.commit()
    print("Seeded Indian states/UTs and 24 Jharkhand districts.")
    print("Blocks/villages are not fabricated; import official LGD data for those.")
finally:
    db.close()
