""" This module contais all models required for this project """
from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Credential(BaseModel):
    """Model class user credential"""

    username: str
    password: str
    secret: str
    url: str


class Credentials(BaseModel):
    """Model class to hold all provide credentials"""

    credentials: List[Credential]


class Language(BaseModel):
    """Model class for user language"""

    language: str
    title: str
    proficiencyLevel: str


class GeneralSkill(BaseModel):
    """Model class for general skill"""

    prefLabel: str


class Education(BaseModel):
    """Model class for education info"""

    institutionName: str
    areaOfStudy: str
    degree: str
    dateStarted: date
    dateEnded: date


class EmploymentHistory(BaseModel):
    """Model class for employment history"""

    companyName: str
    jobTitle: str
    startDate: date
    endDate: Optional[date] = None
    description: Optional[str]
    city: Optional[str]
    country: Optional[str]
    startYear: Optional[int]
    startMonth: Optional[int]
    endYear: Optional[int] = None
    endMonth: Optional[int] = None
    isCurrentPosition: bool


class Address(BaseModel):
    """Model class for address"""

    state: str
    city: str
    zip: Optional[str] = None
    country: str
    address: Optional[str]
    street: str


class FreelancerCategory(BaseModel):
    """Model class for frelancer category"""

    name: str


class Freelancer(BaseModel):
    """Model class for frelancer users"""

    lastName: str
    firstName: str


class UserState(BaseModel):
    """Model class for user state"""

    languages: Optional[List[Language]] = None
    englishLevel: Optional[str]
    generalSkills: Optional[List[GeneralSkill]] = None
    educations: Optional[List[Education]] = None
    employmentHistory: Optional[List[EmploymentHistory]] = None
    profileTitle: str
    profileOverview: Optional[str]
    countryCode: Optional[str]
    rate: float
    phoneNumber: Optional[str]
    phoneCountryCode: Optional[str]
    address: Optional[Address]
    freelancerCategories: Optional[List[FreelancerCategory]] = None


class UserProfile(BaseModel):
    """Main model class to hold all the relevant information in profile setting"""

    state: UserState
    freelancer: Optional[Freelancer] = None
