import re


calendar_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}' \
        r'|(?:January|February|March|April|May|June|July|August|September|October|November|December)' \
        r'\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{2,4}' \
        r'|(?:\d{1,2}\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)' \
        r'\s+\d{2,4}' \
        r'|\d{1,2}/\d{1,2}' \
        r'|(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+\d{1,2}\s+' \
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)' \
        r'|(?:\d{1,2} )?(?:January|February|March|April|May|June|July|August|September|October|November|December)' \
        r' \d{1,2}(?:st|nd|rd|th)?(?:, \d{2,4})?' \
        r'|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)' \
        r'(?:\s|,|\.)+\d{1,2}(?:st|nd|rd|th)?(?:,|\.)+\s\d{2,4}' \
        r'|(?:\d{1,2}/\d{1,2}-)?(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)' \
        r' \d{1,2}(?:st|nd|rd|th)?- \d{1,2}(?:st|nd|rd|th)?(?:,|\.)+\s\d{2,4}' \
        r'|\d{1,2}/\d{1,2}-\d{1,2}/\d{1,2}(?:,|\.)+\s\d{2,4}' \
        r'|\d{1,2}/\d{1,2} @ \d{1,2}:\d{2}(?:am|pm)' \
        r'|\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)' \
        r'\s+\d{1,2}(?:st|nd|rd|th)?\b' \
        r'|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)' \
        r'\s+\d{1,2}(?:st|nd|rd|th)?\b' \
        r')\b'

def regex_pipeline(pages : list, extraction_type : str) -> str:
    """
    Uses regex to filter out pages without specified information according to the inputted pattern.
    
    pages (list) : list of page text to iterate and check over 

    Returns:
    str : string of pdf without irrelevant pages 
    """
    text = ""
    page_num = 1
    if extraction_type == 'calendar':
        pattern = calendar_pattern
    elif extraction_type == 'course':
        pattern = ""
        return # further implementation needed 
    else:
        print("no valid extraction type found, following are valid: 'calendar', 'course'")
        return ""
    
    for page in pages:
        if re.search(pattern, page):
            text += page
        else:
            print("skipped: ", page_num)
        page_num += 1
    return text
