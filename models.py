from sqlalchemy import create_engine, String, Float, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship, sessionmaker, DeclarativeBase
from werkzeug.utils import secure_filename
from magic import Magic

mime = Magic(mime=True)

PG_USER = "postgres"
PG_PASSWORD = "147896352"
PG_DBNAME = "shoes_shop"

engine = create_engine(
    f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@localhost:5432/{PG_DBNAME}",
    echo=False
)

Session = sessionmaker(bind=engine)

CLEAR_DATABASE = True


class Base(DeclarativeBase):
    pass


class Shoes(Base):
    __tablename__ = "shoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    image_filename: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String)

    orders = relationship("Orders", back_populates="shoes")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)

    orders = relationship("Orders", back_populates="user")


class Orders(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    shoes_id: Mapped[int] = mapped_column(ForeignKey("shoes.id"))

    user = relationship("Users", back_populates="orders")
    shoes = relationship("Shoes", back_populates="orders")


def init_db():
    Base.metadata.create_all(engine)


def get_all_products():
    with Session() as session:
        return session.query(Shoes).all()


def create_order(user_id, shoes_id):
    with Session() as session:
        new_order = Orders(
            user_id=user_id,
            shoes_id=shoes_id
        )

        session.add(new_order)
        session.commit()


def main():
    with Session() as session:

        if CLEAR_DATABASE:
            session.query(Orders).delete()
            session.query(Shoes).delete()
            session.commit()

        shoes = [
            Shoes(
                name="Nike Air Max",
                image_filename="nike_air_max.png",
                price=4300,
                description="Класичні кросівки для бігу"
            ),
            Shoes(
                name="Adidas Ultraboost",
                image_filename="adidas_ultrboost.png",
                price=3100,
                description="Легкі та комфортні кросівки"
            ),
            Shoes(
                name="Puma RS-X",
                image_filename="puma_rsx.png",
                price=3750,
                description="Стильні кросівки для міста"
            )
        ]

        session.add_all(shoes)
        session.commit()


init_db()
main()