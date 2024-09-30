## What is Calendr
Calendr is a tool designed to extract important dates/deadlines from college PDFs.

## How does it work
Calendr uses the latest LLM technologies to extract dates from PDF extracted text. It has been tested on OpenAI's latest models but it can also be swapped with other state of the art models as well.

## What's inside this repo
This repo contains a half built backend (FastAPI) and frontend (React) infrastructure that holds web app functionality of being able to attach files and upload them to provided export options. The backend and frontend infrastructure are half built but the actual core logic of extracting dates/deadlines from the PDFs is almost fully built. 

## Notes
I discontinued this app because I realized that there were many different variables that went into dates/deadlines and that they are constantly changing. The risk that comes with getting a date wrong was not worth it and would only cause more work for the user. 

## Tools used
#### Core Logic
- Python
- Langchain
- OpenAI
- Sklearn
- Pydantic
#### Backend
- Python
- FastAPI
- MySQL
#### Frontend
- JavaScript
- React
- MaterialUI

## Questions?
Reach out at parkjae433@gmail.com
