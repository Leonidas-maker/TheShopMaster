import bcrypt
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute() / "models"))

from models import m_user, s_user
from sqlalchemy.orm import Session

class CrudUser:
    def __init__(self, db: Session):
        self.db = db
        
    def get_user(self, user_id: int):
        return self.db.query(m_user.User).filter(m_user.User.user_id == user_id).first()

    def get_user(self, username: str):
        return self.db.query(m_user.User).filter(m_user.User.username == username).first()

    def get_user(self, email: str):
        return self.db.query(m_user.User).filter(m_user.User.email == email).first()

    def get_user(self, email: str, username: str):
        return self.db.query(m_user.User).filter(
            m_user.User.email == email or m_user.User.username == username
        ).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(m_user.User).offset(skip).limit(limit).all()

    def create_user(self, user: s_user.UserCreate):
        # Check if request.address exists
        if user.address:
            # TODO: Performance improvements
            new_city = (
                self.db.query(m_user.Address)
                .join(m_user.City)
                .join(m_user.Country)
                .filter(
                    m_user.City.city == user.address.city,
                    m_user.Country.country == user.address.country,
                )
                .first()
            )

            if not new_city:
                # Check if country exists
                new_country = (
                    self.db.query(m_user.Country).filter_by(country=user.address.country).first()
                )
                if not new_country:
                    # Create new country
                    new_country = m_user.Country(country=user.address.country)
                    self.db.add(new_country)
                    self.db.flush()

                # Create new city
                new_city = m_user.City(city=user.address.city, country_id=new_country.country_id)
                self.db.add(new_city)
                self.db.flush()

            # Check if address exists
            new_address = (
                self.db.query(m_user.Address)
                .filter_by(
                    address1=user.address.address1,
                    address2=user.address.address2,
                    postal_code=user.address.postal_code,
                    city_id=new_city.city_id,
                )
                .first()
            )
            if not new_address:
                # Create new address
                new_address = m_user.Address(
                    address1=user.address.address1,
                    address2=user.address.address2,
                    district=user.address.district,
                    postal_code=user.address.postal_code,
                    city_id=new_city.city_id,
                )
                self.db.add(new_address)
                self.db.flush()

        # Create new user
        new_user = m_user.User(
            username=user.username,
            email=user.email,
            address_id=new_address.address_id,
            is_active=True,
        )
        self.db.add(new_user)
        self.db.flush()

        # Create new user_security
        new_user_security = m_user.UserSecurity(
            user_id=new_user.user_id,
            password=bcrypt.hashpw(
                user.security.password.encode("utf-8"), bcrypt.gensalt()
            ),
        )

        self.db.add(new_user_security)
        self.db.commit()
        return new_user

    def update_user(self, user: s_user.User):
        # TODO Check if something changed
        pass

    def delete_user(self, user_id: int):
        # TODO Recursive delete address, city, country
        # TODO Delete user_security
        # TODO Delete shopping_cart
        # TODO Delete favorite
        # TODO Delete user
        pass