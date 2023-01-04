from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True,index=True)
    password = Column(String(50), nullable= False)
    is_active = Column(Boolean, default=True)
    admin_user = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
    education_files = Column(Text, nullable=True)

    name_surname = Column(String(120), nullable=True)
    age = Column(Integer, nullable=True)
    city = Column(String(50), nullable=True)
    phone = Column(String(20),nullable=True)
    education = Column(String(50), nullable=True)
    certificate_points = Column(String(200), nullable=True)
    about = Column(Text, nullable=True)


    select_university_id = Column(Integer, ForeignKey("education.id"), default=None)
    select_university = relationship("Education", back_populates="select_education", cascade="all, delete")

    created_at = Column(String, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())


##### admin panel #######
##### create education #########
class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    city = Column(String, nullable=True)
    education_type = Column(String, nullable=True)
    students_count = Column(String, nullable=True, default=0)
    about_education = Column(String, nullable=True)
    documents = Column(String, nullable=True)
    photos = Column(String, nullable=True)

    select_education = relationship("User", back_populates="select_university", cascade="all, delete")

class EduCategory(Base):
    __tablename__ = 'edu_category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


#### news and category ##########   
class SiteNews(Base):
    __tablename__ = 'sitenews'

    id = Column(Integer, primary_key=True)
    news_title = Column(String, nullable=True)
    news_image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    news_active = Column(Boolean, default=True)
    views = Column(Integer, default=0)

    select_category_id = Column(Integer, ForeignKey("newscategory.id"), default=1)
    select_category = relationship("NewsCategory", back_populates="category")

    created_at = Column(String, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

class NewsCategory(Base):
    __tablename__ = 'newscategory'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category = relationship("SiteNews", back_populates="select_category")

###### site settings #########
class SiteSettings(Base):
    __tablename__ = 'site_settings'

    id = Column(Integer, primary_key=True)
    site_title = Column(String, nullable=True)
    site_description = Column(Text, nullable=True)
    site_logo = Column(Text, nullable=True)
    site_slogan = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    wp_number = Column(String, nullable=True)
    wp_text = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    site_about = Column(Text, nullable=True)
    about_teams = Column(Text, nullable=True)
    site_email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    google_map = Column(String, nullable=True)


    youtube_video = Column(String, nullable=True)
    facebook = Column(Text, nullable=True)
    instagram = Column(Text, nullable=True)
    linkedin = Column(Text, nullable=True)

    monday = Column(String, nullable=True)
    tuesday = Column(String, nullable=True)
    wednesday = Column(String, nullable=True)
    thursday = Column(String, nullable=True)
    friday = Column(String, nullable=True)
    saturday = Column(String, nullable=True)
    sunday = Column(String, nullable=True)

###### messages #######
class AdminMessages(Base):
    __tablename__ = 'admin_messages'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    sender_id = Column(Integer, nullable=True)
    readed = Column(Integer, default=0)

    created_at = Column(String, default=datetime.now())
    created_at_date = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

###### staff ######
class Staff(Base):
    __tablename__ = 'staff'

    id = Column(Integer, primary_key=True)
    name_surname = Column(String, nullable=False)
    job_position = Column(String, nullable=False)
    photo = Column(Text, nullable=False)
    facebook = Column(Text, nullable=True)
    instagram = Column(Text, nullable=True)
    linkedin = Column(Text, nullable=True)
    twitter = Column(Text, nullable=True)
    behance = Column(Text, nullable=True)


###### slider settings ########
class SliderSettings(Base):
    __tablename__ = 'slider_settings'

    id = Column(Integer, primary_key=True)
    slider = Column(Integer, nullable = True)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    news_photo = Column(String, nullable=True)
    photos = Column(String, nullable=True)
    views = Column(Integer, default=0)

    created_at = Column(String, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())