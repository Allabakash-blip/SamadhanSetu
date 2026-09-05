"""
Import real LGD data (Districts, Sub-Districts/Blocks, Villages) for one state
from the raw .xls files downloaded from https://lgdirectory.gov.in/downloadDirectory.do

Usage:
  1. Put this file in backend/scripts/
  2. Put your 3 downloaded files in backend/scripts/lgd_data/ and rename them to:
       lgd_data/districts.xls
       lgd_data/subdistricts.xls
       lgd_data/villages.xls
  3. From the backend/ folder run:
       python -m scripts.import_jharkhand_lgd

Notes:
- These "xls" files are actually Excel's XML SpreadsheetML format (openable in Excel,
  but not a real binary .xls) -- this script parses that XML directly, no extra
  libraries needed.
- Districts are matched/created under the State row that already exists in your DB
  (looked up by name, e.g. "Jharkhand") -- it does NOT try to force LGD's numeric
  codes as your database IDs, since your States table already has its own
  auto-generated IDs from seed_locations.py.
- Blocks are linked to Districts, and Villages to Blocks, using LGD's own codes
  as a temporary lookup -- not as stored primary keys.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from app.database.connection import SessionLocal
from app.models import State, District, Block, Village

NS = {"ss": "urn:schemas-microsoft-com:office:spreadsheet"}
DATA_DIR = Path(__file__).parent / "lgd_data"

STATE_NAME = "Jharkhand"  # change this if importing a different state


def read_rows(path: Path):
    """Yield each data row (list of cell strings) from an LGD SpreadsheetML file,
    skipping title/header rows and the blank + timestamp footer rows."""
    tree = ET.parse(path)
    root = tree.getroot()
    table = root.find("ss:Worksheet", NS).find("ss:Table", NS)
    for row in table.findall("ss:Row", NS):
        cells = row.findall("ss:Cell", NS)
        vals = [(c.find("ss:Data", NS).text if c.find("ss:Data", NS) is not None else "") for c in cells]
        if not vals:
            continue
        first = (vals[0] or "").strip()
        # real data rows start with a row number like "1" or "1.0" -- skip
        # title rows, header rows, the blank footer row, and the timestamp row
        if not first:
            continue
        try:
            float(first)
        except ValueError:
            continue
        yield vals


def main():
    db = SessionLocal()
    try:
        state = db.query(State).filter(State.name == STATE_NAME).first()
        if not state:
            raise RuntimeError(f"State '{STATE_NAME}' not found - run seed_locations.py first.")

        # ---- Districts ----
        # columns: S.No, District Code, District Version, District Name(En), District Name(Local), Census2001, Census2011
        district_lgd_to_id = {}
        added_d = 0
        for r in read_rows(DATA_DIR / "districts.xls"):
            lgd_code, name = r[1].strip(), r[3].strip()
            existing = db.query(District).filter(District.state_id == state.id, District.name == name).first()
            if existing:
                district_lgd_to_id[lgd_code] = existing.id
                continue
            d = District(state_id=state.id, name=name)
            db.add(d)
            db.flush()  # get d.id without committing yet
            district_lgd_to_id[lgd_code] = d.id
            added_d += 1
        db.commit()
        print(f"Districts: {added_d} added, {len(district_lgd_to_id)} total mapped.")

        # ---- Sub-Districts / Blocks ----
        # columns: S.No, District code, District Name, Subdistrict Code, Subdistrict Version,
        #          Subdistrict Name(En), Subdistrict Name(Local), Census2001, Census2011
        block_lgd_to_id = {}
        added_b = 0
        skipped_b = 0
        for r in read_rows(DATA_DIR / "subdistricts.xls"):
            dist_lgd_code = r[1].strip()
            block_code = r[3].strip()
            block_name = r[5].strip()
            district_id = district_lgd_to_id.get(dist_lgd_code)
            if not district_id:
                skipped_b += 1
                continue
            existing = db.query(Block).filter(Block.district_id == district_id, Block.name == block_name).first()
            if existing:
                block_lgd_to_id[block_code] = existing.id
                continue
            b = Block(district_id=district_id, name=block_name)
            db.add(b)
            db.flush()
            block_lgd_to_id[block_code] = b.id
            added_b += 1
        db.commit()
        print(f"Blocks: {added_b} added, {skipped_b} skipped (no matching district), {len(block_lgd_to_id)} total mapped.")

        # ---- Villages ----
        # columns: S.No, District Code, District Name, Sub-District Code, Sub-District Name,
        #          Village Code, Village Version, Village Name(En), Village Name(Local),
        #          Village Status, Census2001, Census2011, Remark
        added_v = 0
        skipped_v = 0
        batch = 0
        for r in read_rows(DATA_DIR / "villages.xls"):
            subdist_code = r[3].strip()
            village_name = (r[7] or "").strip()
            if not village_name:
                continue
            block_id = block_lgd_to_id.get(subdist_code)
            if not block_id:
                skipped_v += 1
                continue
            db.add(Village(block_id=block_id, name=village_name))
            added_v += 1
            batch += 1
            if batch >= 1000:  # commit in chunks -- villages file is large
                db.commit()
                batch = 0
        db.commit()
        print(f"Villages: {added_v} added, {skipped_v} skipped (no matching block).")

        print("Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()