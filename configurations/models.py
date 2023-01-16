from sqlalchemy import Column, Integer, Boolean, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from configurations.database import Base
from datetime import datetime

  ######################################
 ###########      User     ############
######################################
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True,index=True)
    password = Column(String, nullable= False)
    is_active = Column(Boolean, default=True)
    admin_user = Column(Boolean, default=False)
    super_user = Column(Boolean, default=False)
    profile_picture = Column(String, nullable=True)
    education_files = Column(Text, nullable=True)

    navbar_fixed = Column(String, nullable=True, default="")
    site_mode = Column(String, nullable=True, default="")
    sidebar_selected_color = Column(String, nullable=True, default="1")

    name_surname = Column(String(150), nullable=True, default="")
    age = Column(String, nullable=True)
    city = Column(String(100), nullable=True, default="")
    phone = Column(String(30),nullable=True, default="")
    education = Column(String(150), nullable=True, default="")
    certificate_points = Column(String, nullable=True, default="")
    about = Column(Text, nullable=True)


    select_university_id = Column(Integer, ForeignKey("education.id", ondelete='CASCADE'), default=None)
    select_university = relationship("Education", back_populates="select_education")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ###########   Education   ############
######################################
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

    select_education = relationship("User", back_populates="select_university", passive_deletes='all')

  ######################################
 ##########   Edu Category   ##########
######################################

class EduCategory(Base):
    __tablename__ = 'edu_category'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

  ######################################
 ###########   SiteNews  ##############
######################################
class SiteNews(Base):
    __tablename__ = 'sitenews'

    id = Column(Integer, primary_key=True)
    news_title = Column(String, nullable=True)
    news_image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    news_active = Column(Boolean, default=True)
    views = Column(Integer, default=0)

    select_category_id = Column(Integer, ForeignKey("newscategory.id", ondelete='CASCADE'), default=1)
    select_category = relationship("NewsCategory", back_populates="category")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ##########   NewsCategory   ##########
######################################
class NewsCategory(Base):
    __tablename__ = 'newscategory'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category = relationship("SiteNews", back_populates="select_category", passive_deletes=True)

  ######################################
 ##########   SiteSettings   ##########
######################################
class SiteSettings(Base):
    __tablename__ = 'site_settings'

    id = Column(Integer, primary_key=True)
    site_url = Column(Text, nullable=True, default="")
    site_title = Column(String, nullable=True, default="")
    site_description = Column(Text, nullable=True, default="")
    site_logo = Column(Text, nullable=True, default="")
    site_slogan = Column(String, nullable=True, default="")
    phone = Column(String, nullable=True, default="")
    wp_number = Column(String, nullable=True, default="")
    wp_text = Column(String, nullable=True, default="")
    is_active = Column(Boolean, default=True)
    site_about = Column(Text, nullable=True, default="")
    about_teams = Column(Text, nullable=True, default="")
    site_email = Column(String, nullable=True, default="")
    address = Column(String, nullable=True, default="")
    google_map = Column(String, nullable=True, default="")


    youtube_video = Column(String, nullable=True, default="")
    facebook = Column(Text, nullable=True, default="")
    instagram = Column(Text, nullable=True, default="")
    linkedin = Column(Text, nullable=True, default="")

    monday = Column(String, nullable=True, default="")
    tuesday = Column(String, nullable=True, default="")
    wednesday = Column(String, nullable=True, default="")
    thursday = Column(String, nullable=True, default="")
    friday = Column(String, nullable=True, default="")
    saturday = Column(String, nullable=True, default="")
    sunday = Column(String, nullable=True, default="")

  ######################################
 ########   Admin Messages   ##########
######################################
class AdminMessages(Base):
    __tablename__ = 'admin_messages'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    sender_id = Column(Integer, nullable=True)
    readed = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 ##########     Staff     #############
######################################
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

  ######################################
 #########  SliderSettings  ###########
######################################
class SliderSettings(Base):
    __tablename__ = 'slider_settings'

    id = Column(Integer, primary_key=True)
    slider = Column(Integer, nullable = True)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    news_photo = Column(String, nullable=True)
    photos = Column(String, nullable=True)
    views = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())

  ######################################
 #########    Models end    ###########
######################################