import pdfplumber
from io import BytesIO
from pptx import Presentation
from dotenv import load_dotenv
from ..prompts.prompts import calendar_prompt_v4
import re
import pickle
from .parser_helpers.regex_helper import regex_pipeline
from .parser_helpers.ml_helper import ml_pipeline

MODEL_PATHS = [
            ('../backend/api/ml_models/calendar/lr_model.pkl', '../backend/api/ml_models/calendar/tfidf_vectorizer.pkl'),
            ('../backend/api/ml_models/course/lr_model.pkl', '../backend/api/ml_models/course/tfidf_vectorizer.pkl')
        ]

class FileParser:
    """
    FileParser v1:
    Object for all file parsing related operations, utilizing pdfplumber for pdf extraction 
    """
    def __init__(self):
        self.load_models()

    def load_models(self):
        for model_path, vectorizer_path in MODEL_PATHS:
            try:
                with open(model_path, 'rb') as f:
                    if 'calendar' in model_path:
                        self.calendar_model = pickle.load(f)
                        print("Calendar model loaded")
                    elif 'course' in model_path:
                        self.course_model = pickle.load(f)
                        print("Course model loaded")
            except Exception as e:
                print(e)
            
            try:
                with open(vectorizer_path, 'rb') as f:
                    if 'calendar' in vectorizer_path:
                        self.calendar_vectorizer = pickle.load(f)
                        print("Vectorizer loaded")
                    elif 'course' in vectorizer_path:
                        self.course_vectorizer = pickle.load(f)
                        print("Vectorizer loaded")
            except Exception as e:
                print(e)

    def remove_newlines(text : str) -> str:
        """
        Helper function that solves the excess new lines that come from pdfplumber extraction using regex. 

        text (str) : input text

        Returns:
        cleaned_text (str) : text without the excess new lines
        """
        pattern = r'(\n\s*){6,}'
        
        cleaned_text = re.sub(pattern, '\n\n', text)
        
        return cleaned_text
    
    def extract_text_from_pdf(self, pdf_bytes : bytes) -> str:
        """
        Extracts text from pdf bytes using pdfplumber

        pdf_bytes (bytes) : byte representation of pdf 
        
        Returns:
        cleaned_text (str) : text of pdf 
        """
        text = ""

        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text(layout = True, x_tolerance = 2)

        return text

    def regex_path_from_pdf(self, pdf_bytes : str, buffer_size : int, extraction_type : str) -> str:
        """
        Extracts text from PDF and uses regex to filter out pages simultaneously. 

        pdf_bytes (str) : byte representation of pdf 
        buffer_size (int) : buffer size in characters for pages
        extraction_type (str) : type of extraction: ('calendar', 'course')

        Returns:
        cleaned_text (str) : text that excludes irrelevant pages
        """
        if buffer_size > 0:
            pages = []
            prev_page_text = ""
            next_page_text = ""
            with pdfplumber.open(pdf_bytes) as pdf:
                total_pages = len(pdf.pages)
                for i in range(total_pages):
                    buffer_page_text = ""
                    if i == 0:
                        current_page_text = pdf.pages[i].extract_text(layout = True, x_tolerance = 2)
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size] # get first buffer_size characters from i + 1 page
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    elif i == total_pages - 1:
                        buffer_page_text += prev_page_text[-buffer_size:] # get last buffer_size characters from i - 1 page 
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    else:
                        prev_page_text = current_page_text
                        current_page_text = next_page_text
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += prev_page_text[-buffer_size:]
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
            text = regex_pipeline(pages, extraction_type)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text
        else:
            pages = []
            with pdfplumber.open(pdf_bytes) as pdf:
                for page in pdf.pages:
                    pages.append(page.extract_text(layout = True, x_tolerance = 2))
            text = regex_pipeline(pages, extraction_type)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text  

    def ml_from_pdf(self, pdf_bytes : str, buffer_size : int, extraction_type : str) -> str:
        """
        Extracts and filters text from PDF using machine learning.
        
        pdf_bytes (str) : bytes of pdf 
        buffer_size (int) : buffer size in characters for pages
        extraction_type (str) : type of extraction: ('calendar', 'course')

        Returns:
        str : filtered text of pdf 
        """
        if buffer_size > 0:
            pages = []
            prev_page_text = ""
            next_page_text = ""
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                total_pages = len(pdf.pages)
                for i in range(total_pages):
                    buffer_page_text = ""
                    if i == 0:
                        current_page_text = pdf.pages[i].extract_text(layout = True, x_tolerance = 2)
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size] # get first buffer_size characters from i + 1 page
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    elif i == total_pages - 1:
                        buffer_page_text += prev_page_text[-buffer_size:] # get last buffer_size characters from i - 1 page 
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    else:
                        prev_page_text = current_page_text
                        current_page_text = next_page_text
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += prev_page_text[-buffer_size:]
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
            if extraction_type == 'calendar':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            elif extraction_type == 'course':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text
        else:
            pages = []
            with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
                for page in pdf.pages:
                    pages.append(page.extract_text(layout = True, x_tolerance = 2))
            if extraction_type == 'calendar':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            elif extraction_type == 'course':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text

    def ml_from_pdf_path(self, pdf_path : str, buffer_size : int, extraction_type : str) -> str:
        """
        Extracts and filters text from PDF using machine learning.
        
        pdf_path (str) : path of pdf 
        buffer_size (int) : buffer size in characters for pages
        extraction_type (str) : type of extraction: ('calendar', 'course')

        Returns:
        str : filtered text of pdf 
        """
        if buffer_size > 0:
            pages = []
            prev_page_text = ""
            next_page_text = ""
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                for i in range(total_pages):
                    buffer_page_text = ""
                    if i == 0:
                        current_page_text = pdf.pages[i].extract_text(layout = True, x_tolerance = 2)
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size] # get first buffer_size characters from i + 1 page
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    elif i == total_pages - 1:
                        buffer_page_text += prev_page_text[-buffer_size:] # get last buffer_size characters from i - 1 page 
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
                    else:
                        prev_page_text = current_page_text
                        current_page_text = next_page_text
                        next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

                        buffer_page_text += prev_page_text[-buffer_size:]
                        buffer_page_text += "\n"
                        buffer_page_text += current_page_text
                        buffer_page_text += "\n"
                        buffer_page_text += next_page_text[:buffer_size]
                        buffer_page_text += "\n"
                        pages.append(buffer_page_text)
            if extraction_type == 'calendar':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            elif extraction_type == 'course':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text
        else:
            pages = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    pages.append(page.extract_text(layout = True, x_tolerance = 2))
            if extraction_type == 'calendar':
                text = ml_pipeline(pages, 'calendar', self.calendar_model, self.calendar_vectorizer)
            elif extraction_type == 'course':
                text = ml_pipeline(pages, 'course', self.course_model, self.course_vectorizer)
            cleaned_text = FileParser.remove_newlines(text)
            return cleaned_text

    # def rag_text_from_pdf(self, pdf_bytes : bytes, buffer_size : int, extraction_type : str) -> str:
    #     """
    #     RAG text from pdf path using pdfplumber and openai_rag_pipeline.

    #     pdf_path (bytes) : byte representation of pdf 
    #     buffer_size (int) : buffer size in characters for pages
    #     extraction_type (str) : type of extraction: ('calendar', 'course')

    #     Returns:
    #     cleaned_text (str) : text that excludes irrelevant pages
    #     """
    #     if buffer_size > 0:
    #         pages = []
    #         prev_page_text = ""
    #         next_page_text = ""
    #         with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
    #             total_pages = len(pdf.pages)
    #             for i in range(total_pages):
    #                 buffer_page_text = ""
    #                 if i == 0:
    #                     current_page_text = pdf.pages[i].extract_text(layout = True, x_tolerance = 2)
    #                     next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

    #                     buffer_page_text += current_page_text
    #                     buffer_page_text += "\n"
    #                     buffer_page_text += next_page_text[:buffer_size] # get first buffer_size characters from i + 1 page
    #                     buffer_page_text += "\n"
    #                     pages.append(buffer_page_text)
    #                 elif i == total_pages - 1:
    #                     buffer_page_text += prev_page_text[-buffer_size:] # get last buffer_size characters from i - 1 page 
    #                     buffer_page_text += "\n"
    #                     buffer_page_text += current_page_text
    #                     buffer_page_text += "\n"
    #                     buffer_page_text += next_page_text[:buffer_size]
    #                     buffer_page_text += "\n"
    #                     pages.append(buffer_page_text)
    #                 else:
    #                     prev_page_text = current_page_text
    #                     current_page_text = next_page_text
    #                     next_page_text = pdf.pages[i + 1].extract_text(layout = True, x_tolerance = 2)

    #                     buffer_page_text += prev_page_text[-buffer_size:]
    #                     buffer_page_text += "\n"
    #                     buffer_page_text += current_page_text
    #                     buffer_page_text += "\n"
    #                     buffer_page_text += next_page_text[:buffer_size]
    #                     buffer_page_text += "\n"
    #                     pages.append(buffer_page_text)
    #         text = openai_rag_pipeline(pages, extraction_type)
    #         cleaned_text = FileParser.remove_newlines(text)
    #         return cleaned_text
    #     else:
    #         pages = []
    #         with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
    #             for page in pdf.pages:
    #                 pages.append(page.extract_text(layout = True, x_tolerance = 2))
    #         text = openai_rag_pipeline(pages, extraction_type)
    #         cleaned_text = FileParser.remove_newlines(text)
    #         return cleaned_text
