from ..prompts.prompts import calendar_prompt_v5
from langchain.output_parsers import YamlOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import PydanticOutputParser
from ..models.calendar import Calendar
from langchain.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException

def calendar_pipeline(model, text : str) -> Calendar:
    """
    Langchain pipeline for calendar information extraction. 

    model (Langchain LLM model) : Any langchain LLM model 
    text (str) : Text used for extraction

    Returns: 
    calendar_obj (Calendar) : Calendar object of assignment dates, refer to ./models for data structure 
    """
    try:
        parser = PydanticOutputParser(pydantic_object=Calendar)

        prompt = PromptTemplate(
            template="{format_instructions}\n{text}\n{prompt}",
            input_variables=["text", "prompt"],
            partial_variables={"format_instructions": parser.get_format_instructions()})

        chain = prompt | model | parser

        calendar_obj = chain.invoke({"text" : text, "prompt" : calendar_prompt_v5})

        return calendar_obj

    except OutputParserException as e:
        print(e)
        calendar_obj = Calendar()
        return calendar_obj
    
    except Exception as e:
        print("ran into error", e)
        calendar_obj = Calendar()
        return calendar_obj
