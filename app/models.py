import datetime

from sqlalchemy import ForeignKey, String, Time
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class City(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    streets: Mapped[list["Street"]] = relationship(back_populates="city")


class Street(Base):
    __tablename__ = "streets"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), nullable=False)

    city: Mapped["City"] = relationship(back_populates="streets")
    street_shops: Mapped["Shop"] = relationship(back_populates="street")


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    street_id: Mapped[int] = mapped_column(ForeignKey("streets.id"), nullable=False)
    house: Mapped[str] = mapped_column(nullable=False)
    time_open: Mapped[datetime.time] = mapped_column(
        Time(timezone=True), nullable=False
    )
    time_close: Mapped[datetime.time] = mapped_column(
        Time(timezone=True), nullable=False
    )

    street: Mapped["Street"] = relationship(back_populates="street_shops")
