import sys
sys.path.append("...")

from api.utils.google_calendar import add_events_to_google_calendar
from api.utils.calendar_pipeline import calendar_pipeline
from api.utils.file_parser import FileParser
from api.models.calendar import Calendar
from db.models.user import User
from db.session import get_db

from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_login import LoginManager
from fastapi.responses import RedirectResponse
from fastapi import Depends, HTTPException, Request, Response, File, HTTPException, Request, UploadFile, APIRouter, Form
from fastapi.responses import JSONResponse

from langchain_openai import ChatOpenAI

from sqlalchemy.orm import Session

import requests
import os
import io
import csv

from google.auth.transport import requests as google_auth_request
from google.oauth2 import id_token

from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SECRET_KEY = os.getenv("GOOGLE_SECRET_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_URL = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}&response_type=code"
        f"&scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar"
        f"&access_type=offline&prompt=consent"
        f"&redirect_uri={REDIRECT_URI}&state=state_parameter_passthrough_value"
    )

manager = LoginManager(SECRET_KEY, token_url="/auth/token", use_cookie=True)
oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="https://accounts.google.com/o/oauth2/auth",
                                              tokenUrl=TOKEN_URI)
router = APIRouter()

file_parser = FileParser()
model = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model="gpt-4o-2024-08-06", temperature=0.1)

def convert_calendar_to_csv(calendar : Calendar) -> io.StringIO:
    """
    Converts calendar object to CSV format. Used for other calendar app exports such as Notion. 

    calendar (Calendar) : calendar object to extract events 

    Returns:
    (io.StringIO) : CSV represented as bytes to send back to frontend to allow the user to download
    """
    buffer = io.StringIO()
    data = [
        ["Title", "Date", "Type"]
    ]
    if type(calendar) != dict:
        calendar = calendar.dict()

    for homework in calendar['homework']:
        homework_event = [calendar['course_number'] + " " + homework['name'], homework['deadline'], homework['type']]
        data.append(homework_event)
    for exam in calendar['exams']:
        exam_event = [calendar['course_number'] + " " + exam['name'], exam['deadline'], exam['type']]
        data.append(exam_event)
    for lab in calendar['labs']:
        lab_event = [calendar['course_number'] + " " + lab['name'], lab['deadline'], lab['type']]
        data.append(lab_event)
    for project in calendar['projects']:
        project_event = [calendar['course_number'] + " " + project['name'], project['deadline'], project['type']]
        data.append(project_event)
    for quiz in calendar['quizzes']:
        quiz_event = [calendar['course_number'] + " " + quiz['name'], quiz['deadline'], quiz['type']]
        data.append(quiz_event)
    for other in calendar['other']:
        other_event = [calendar['course_number'] + " " + other['name'], other['deadline'], other['type']]
        data.append(other_event)

    writer = csv.writer(buffer, quoting=csv.QUOTE_MINIMAL)
    
    writer.writerows(data)

    csv_bytes = buffer.getvalue().encode('utf-8') 

    return csv_bytes

@router.post("/register")
def register():
    pass

@router.get("/login")
def login() -> None:
    """
    Google Auth login endpoint
    
    Returns:
    (None)
    """
    return RedirectResponse(GOOGLE_AUTH_URL)

@router.get("/callback")
def callback(request: Request, code: str, db: Session = Depends(get_db)) -> RedirectResponse:
    """
    Callback function from Google Auth. Creates a Redirect Response to the frontend home page and attaches access token and refresh token as cookies to the response. 

    code (str) : code to exchange access token from Google API.

    Returns:
    (RedirectResponse) : Redirect Response to route specificied with necessary cookies attached. 
    """
    # setup token data to post to Google to exchange access token
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    # retrieve metadata for auth 
    token_response = requests.post(TOKEN_URI, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")
    refresh_token = token_json.get("refresh_token")
    id_token_str = token_json.get("id_token")
    
    # attach access and refresh tokens to repsonse cookies for verification purposes after logging in and holding session information
    response = RedirectResponse("http://localhost:3000/home")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=False,
        secure=False,
        samesite="Lax",
        path="/" 
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=False,
        secure=False,
        samesite="Lax",
        path="/" 
    )
    id_token_str = token_json.get("id_token")
    # verifies and extracts user's google account metadata from id token 
    id_info = id_token.verify_oauth2_token(id_token_str, google_auth_request.Request(), CLIENT_ID)
    email = id_info['email']

    user_search = db.query(User).filter(User.email == email).all()
    # check if email exists in database
    if not user_search:
        new_user = User(email = email, auth_type = "google", num_docs = 1)
        user_insert_result = db.add(new_user)
        db.commit()

    return response

@router.get("/validate_token")
def validate_token(request: Request):
    """
    Endpoint to validate token by cross checking for a cookie. 
    """
    token = request.cookies.get("access_token")
    if not token:
        return JSONResponse(content={"valid": False}, status_code=401)
    
    is_valid = True
    
    return JSONResponse(content={"valid": is_valid})

@router.post("/logout")
def logout(response: Response):
    # remove access token and refresh token cookie
    response.delete_cookie(key="access_token")
    response.delete_cookie(key = "refresh_token")
    return {"message": "Logged out successfully"}

@router.post("/extract_events_to_google")
async def extract_events_to_google(request : Request, file: UploadFile = File(...)) -> JSONResponse:
    """
    Extract and add events from PDF to Google Calendar. User must have access token and refresh token available for this to work (on Google Calendar as of 08/27/24, with other future export options, an
    access token and refresh token is not required)

    request (Request) : incoming request should contain access token and refresh token tags from cookies
    file (UploadFile) : containing contents of uploaded file

    Returns:
    (JSONResponse) : JSON response with status of extraction, either a resubmit, success, or error response
    """
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    content_type = file.content_type
    if content_type is None:
        raise HTTPException(status_code=400, detail="Could not determine file content type")
  
    content_bytes = await file.read()

    if "pdf" in content_type:
        pdf_text = file_parser.ml_from_pdf(content_bytes, 0, 'calendar')
        calendar_object = calendar_pipeline(model, pdf_text)
        # no course number found in Calendar object, so we need to ask for it from the user
        if calendar_object.course_number == "NA":
            return JSONResponse(content = {"success" : False, "code" : 100, "data" : calendar_object.dict()})
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        add_events_to_google_calendar(calendar_object, access_token, refresh_token)

        return JSONResponse(content = {"success" : True, "code" : 200})
    else:
        raise HTTPException(status_code=400, detail="Not a PDF file, instead: " + content_type)
    
@router.post("/submit_course_name")
async def submit_course_name(request: Request) -> JSONResponse:
    """
    Request missing course name from initial PDF extraction. Takes in previous Calendar object created from initial request and simply
    attaches the course name to that JSON and adds the events to Google Calendar. 

    request (Request) : incoming request should contain access token and refresh token tags from cookies

    Returns:
    (JSONResponse) : response on status of resubmit on course name
    """
    try:
        # retrieve already parsed calendar data contents from previous request
        calendar_data = await request.json()
        
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")
        add_events_to_google_calendar(calendar_data, access_token, refresh_token)

        return JSONResponse(content = {"success" : True, "code" : 200})
    except Exception as e:
        print("error at submit_course_name route:", e)
        return JSONResponse(content = {"success" : False, "code" : 400})
    
@router.post("/extract_and_convert_events_to_csv")
async def extract_and_convert_events_to_csv(request : Request, file: UploadFile = File(...)):
    """
    Converts calendar object to CSV format. Used for other calendar app exports such as Notion. 

    request (Request) : incoming request should contain access token and refresh token tags from cookies
    file (UploadFile) : containing contents of uploaded file
    """
    if file is None:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    content_type = file.content_type
    if content_type is None:
        raise HTTPException(status_code=400, detail="Could not determine file content type")
  
    content_bytes = await file.read()

    if "pdf" in content_type:
        try:
            pdf_text = file_parser.ml_from_pdf(content_bytes, 0, 'calendar')
            calendar_object = calendar_pipeline(model, pdf_text)
            csv_bytes = convert_calendar_to_csv(calendar_object)
            print("returning csv bytes")
            return Response(content=csv_bytes, media_type="text/csv")
        except Exception as e:
            print("error at extract and convert events to csv", e)
            return JSONResponse(content = {"success" : False, "code" : 400})
    else:
        raise HTTPException(status_code=400, detail="Not a PDF file, instead: " + content_type)
    