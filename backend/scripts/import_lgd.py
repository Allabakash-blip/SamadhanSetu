# Template for importing official Local Government Directory (LGD) data.
#
# Put these CSV files inside backend/scripts/lgd_data/:
# states.csv    -> state_code,state_name
# districts.csv -> district_code,district_name,state_code
# blocks.csv    -> block_code,block_name,district_code
# villages.csv  -> village_code,village_name,block_code
#
# Review and map the exact columns from the LGD export before running.
# Do not fabricate administrative records.

from pathlib import Path
import csv
from app.database.connection import SessionLocal
from app.models import State, District, Block, Village

DATA = Path(__file__).parent / "lgd_data"

def load_csv(name):
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def main():
    db = SessionLocal()
    try:
        for r in load_csv("states.csv"):
            if not db.query(State).filter(State.id == int(r["state_code"])).first():
                db.add(State(id=int(r["state_code"]), name=r["state_name"].strip(), code=r["state_code"]))
        db.commit()
        for r in load_csv("districts.csv"):
            if not db.query(District).filter(District.id == int(r["district_code"])).first():
                db.add(District(id=int(r["district_code"]), state_id=int(r["state_code"]), name=r["district_name"].strip()))
        db.commit()
        for r in load_csv("blocks.csv"):
            if not db.query(Block).filter(Block.id == int(r["block_code"])).first():
                db.add(Block(id=int(r["block_code"]), district_id=int(r["district_code"]), name=r["block_name"].strip()))
        db.commit()
        for r in load_csv("villages.csv"):
            if not db.query(Village).filter(Village.id == int(r["village_code"])).first():
                db.add(Village(id=int(r["village_code"]), block_id=int(r["block_code"]), name=r["village_name"].strip()))
        db.commit()
        print("LGD import completed.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
