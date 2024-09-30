from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string

# the higher the threshold, the less documents passed. 
calendar_threshold = .3
course_threshold = .2

def preprocess_text(text : str) -> str:
    """
    Preprocessing of page text before vectorization for page filtration model (punctuation removal, stop words removeal, lemmatization)

    text (str) : text of pdf page 

    Returns:
    str : cleaned text of page 
    """
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Convert tokens back to string
    text = ' '.join(tokens)
    
    return text

def custom_predict(input, model, threshold):
    """
    Helper function for ML model to predict custom threshold 

    input (str) : input after text preprocessing and vectorization 
    model : ML model used for prediction 
    threshold (float) : threshold of true or false 

    Returns:
    boolean : True if document contains any date information
    """
    probs = model.predict_proba(input)
    if((probs[:, 1] > threshold).astype(int)[0] == 1):
        return True
    return False

def ml_pipeline(pages : list, extraction_type : str, model, vectorizer_model) -> str:
    """
    Uses ML to filter out pages

    pages (list) : list of page text to iterate and filter 
    extraction_type (str) : extraction type ('calendar', 'course')
    model : logistic regression model
    vectorizer_model : model for vectorizing plain text

    Returns
    str : string of pdf without irrelevant pages 
    """
    text = ""
    if extraction_type == 'calendar':
        threshold = calendar_threshold
    elif extraction_type == 'course':
        threshold = course_threshold
    else:
        print("Invalid extraction type found: ", extraction_type, ". Should be either 'calendar' or 'course'")
        return ""
    page_num = 1
    for page in pages:
        preprocessed_text = preprocess_text(page)
        vectorized_text = vectorizer_model.transform([preprocessed_text])
        if custom_predict(vectorized_text, model, threshold):
            text += page
        else:
            print("skipped page number " + str(page_num))
        page_num += 1

    return text

