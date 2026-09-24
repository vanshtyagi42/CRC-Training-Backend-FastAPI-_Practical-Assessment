from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Event
from models import Event, Reservation

app = FastAPI(title="Campus Event Seat Reservation API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/events", response_model=Event, status_code=201)
def create_event(event: Event, session: Session = Depends(get_session)):
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.get("/events", response_model=List[Event])
def get_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@app.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@app.put("/events/{event_id}", response_model=Event)
def update_event(event_id: int, updated_event: Event, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    event.title = updated_event.title
    event.venue = updated_event.venue
    event.capacity = updated_event.capacity
    event.organizer = updated_event.organizer
    event.status = updated_event.status

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return None 

@app.post("/events/{event_id}/reserve", response_model=Reservation, status_code=201)
def create_reservation(event_id: int, reservation: Reservation, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.status != "Open":
        raise HTTPException(status_code=400, detail="Event is closed for reservations")

    existing = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()

    if len(existing) >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is full")

    reservation.event_id = event_id
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


@app.get("/events/{event_id}/reservations", response_model=List[Reservation])
def get_event_reservations(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    return session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()


@app.delete("/reservations/{reservation_id}", status_code=204)
def cancel_reservation(reservation_id: int, session: Session = Depends(get_session)):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    session.delete(reservation)
    session.commit()
    return None


@app.get("/events/{event_id}/availability")
def get_event_availability(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    booked = len(session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all())

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": event.capacity - booked
    } 