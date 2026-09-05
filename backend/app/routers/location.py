from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import State, District, Block, Village

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/states")
def states(db: Session = Depends(get_db)):
    return [{"id":x.id,"name":x.name,"code":x.code} for x in db.query(State).order_by(State.name).all()]

@router.get("/states/{state_id}/districts")
def districts(state_id: int, db: Session = Depends(get_db)):
    rows = db.query(District).filter(District.state_id == state_id).order_by(District.name).all()
    return [{"id":x.id,"name":x.name} for x in rows]

@router.get("/districts/{district_id}/blocks")
def blocks(district_id: int, db: Session = Depends(get_db)):
    rows = db.query(Block).filter(Block.district_id == district_id).order_by(Block.name).all()
    return [{"id":x.id,"name":x.name} for x in rows]

@router.get("/blocks/{block_id}/villages")
def villages(block_id: int, db: Session = Depends(get_db)):
    rows = db.query(Village).filter(Village.block_id == block_id).order_by(Village.name).all()
    return [{"id":x.id,"name":x.name} for x in rows]

@router.get("/status")
def location_status(db: Session = Depends(get_db)):
    return {
        "states": db.query(State).count(),
        "districts": db.query(District).count(),
        "blocks": db.query(Block).count(),
        "villages": db.query(Village).count(),
        "note": "Import official LGD administrative data for the complete hierarchy."
    }
