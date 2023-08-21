import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    event_at = Column(DateTime(timezone=True), nullable=True, server_default=text('now()'))
    expire_at = Column(DateTime(timezone=True), nullable=True, server_default=text('now()'))
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))
    # Add Role Column
    # role = Column(String, nullable=False, server_default=text('member'))


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    membership_id = Column(Integer, nullable=False, unique=True)
    # DEFAULT value should pass
    membership_status = Column(String, nullable=True)
    batch_no = Column(Integer, nullable=False)
    contact_no = Column(String, nullable=True)
    dob = Column(DateTime(timezone=True), nullable=True, server_default=text('now()'))
    birth_place = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    present_address = Column(String, nullable=True)
    permanent_address = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    spouse_name = Column(String, nullable=True)
    wedding_anniversary = Column(DateTime(timezone=True), nullable=True, server_default=text('now()'))
    # education_id = Column(String, nullable=False)
    # experience_id = Column(String, nullable=False)
    about = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True)
