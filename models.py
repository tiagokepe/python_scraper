from pydantic import BaseModel
from typing import List
from datetime import date
from typing import Optional


# Model class for loading the credentials in the credentials.json file
class Credentials(BaseModel):
    username: str
    password: str
    secret: str
    url: str

# Model classes to hold all the relevant information in profile setting ###########

class Language(BaseModel):
    language: str
    title: str
    proficiencyLevel: str
    
class GeneralSkill(BaseModel):
    prefLabel: str

class Education(BaseModel):
    institutionName: str
    areaOfStudy: str
    degree: str
    dateStarted: date
    dateEnded: date

class EmploymentHistory(BaseModel):
    companyName: str
    jobTitle: str
    startDate: date
    endDate: date = None
    description: str
    city: str
    country: str
    startYear: int
    startMonth: int
    endYear: int = None
    endMonth: int = None
    isCurrentPosition: bool

class Address(BaseModel):
    state: str
    city: str
    zip: str = None
    country: str
    address: str
    street: str

class FreelancerCategory(BaseModel):
    name: str

class Freelancer(BaseModel):
    lastName: str
    firstName: str
    
class UserState(BaseModel):
    languages: List[Language] = None
    englishLevel: str
    generalSkills: List[GeneralSkill] = None
    educations: List[Education] = None
    employmentHistory: List[EmploymentHistory] = None
    profileTitle: str
    profileOverview: str
    countryCode: str
    rate: float
    phoneNumber: str
    phoneCountryCode: str
    address: Address
    freelancerCategories: List[FreelancerCategory] = None

class UserProfile(BaseModel):
    state: UserState
    freelancer: Optional[Freelancer] = None
