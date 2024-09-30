from typing import List, Dict
from langchain_core.pydantic_v1 import BaseModel, Field, validator

class Lecture(BaseModel):
    day_of_week: str = Field(default="", description="Day of week (Monday, Tuesday, etc) when lecture takes place")
    start_time: str = Field(default="", description="Time when lecture starts")
    end_time: str = Field(default="", description="Time when lecture ends")
    lecture_location: str = Field(default="", description="Lecture location")

class Professor(BaseModel):
    name : str = Field(default = "", description = "Professor's name")
    email: str = Field(default = "", description= "Professor's email") 
    lectures : List[Lecture] = Field(default = [], description = "List of Lectures associated with professor")

class Scale(BaseModel):
    upper_bound : float = Field(default = -1, description = "Upper bound scale for grade")
    lower_bound : float = Field(default = -1, description = "Lower bound scale for grade")

class Course(BaseModel):
    name : str = Field(default = "", description = "Course name in 'course_abbreviation course_number' format")
    description : str = Field(default = "", description = "Concise course description")
    professors : List[Professor] = Field(default = [], description = "List of Professors")
    weights : Dict[str, float] = Field(default = {}, description = "Dictionary of assignment weights in assignment_type : assignment_weight format ")
    scaling : Dict[str, Scale] = Field(default = {}, description="Dictionary of grade scales in grade : Scale format")

    @validator("name")
    def validate_course_name(cls, name):
        try:  
            if len(name.split(" ")) == 2: # separate the course abbreviation and course number 
                return name
            else:
                return "Invalid Name"
        except Exception as e:
            print("something went wrong: ", e)
            return "error"
        
    @validator("description")
    def validate_description_length(cls, description):
        try:
            words = description.split(" ")
            if len(words) > 75:
                return ""
            else:
                return description
        except Exception as e:
            print("something went wrong: ", e)
            return "error"
        
    # objectives : List[str] = Field(description="Course objectives")
    # materials : List[str] = Field(description="Course materials") 
    # removed temporaririly ^^^
        