from typing import List, Any, Optional, Union
from langchain_core.pydantic_v1 import BaseModel, Field, validator
import datetime
from dateutil import parser

output_format = "%m/%d/%Y %H:%M:%S"

class CalendarEvent(BaseModel):
    name : str = Field(description = "Name of assignment")
    type : str = Field(description = "Type of assignment")
    deadline: str = Field(description = "Deadline of assignment in YYYY-MM-DDThh:mm:ss format")

    # @validator("date", pre = True, always = True)
    # def validate_date(cls, raw_date):
    #     try:
    #         date = parser.parse(raw_date) # subject to change
    #         return date.strftime(output_format)
    #     except Exception as e:
    #         print(raw_date, e)

    #     return "NA" # NA if accepted date not found

class Calendar(BaseModel):
    course_number : str = Field(default = "NA", description = "Course number")
    homework: List[CalendarEvent] = Field(default=[], description = "List of homework assignments")
    exams: List[CalendarEvent] = Field(default=[], description = "List of exams")
    labs: List[CalendarEvent] = Field(default=[], description = "List of labs")
    projects: List[CalendarEvent] = Field(default=[], description = "List of projects")
    quizzes: List[CalendarEvent] = Field(default=[], description = "List of quizzes")
    other: List[CalendarEvent] = Field(default=[], description = "List of other assignments") 

    @validator("homework", "exams", "labs", "projects", "quizzes", "other", pre = True, always = True)
    def check_empty(cls, value):
        if value == None:
            return []
        else:
            return value