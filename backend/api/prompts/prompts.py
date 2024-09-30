# Notes Prompt v1
# Pros: Can extract good notes 
# Cons/Issues: Cannot extract images, 
# Todo: Test run times, potentially separate prompts into retrieval and JSON conversion 
notes_prompt = """
: this is text containing notes about a college course lecture. Extract and summarize the key information and concepts from the college course lecture slides in an organized and comprehensive manner. These are the things that you should be looking for: 

1. Course Title and Instructor Name: Start the summary by mentioning the course title and the name of the instructor.

2. Main Topics: Identify the main topics covered in the lecture.
- List each main topic in bullet points.
- For each main topic, provide a concise high-level overview highlighting the key concepts or ideas discussed.

3. Subtopics: For each main topic, extract the following subtopics:
- Subtopic Title: List the subtopics covered under each main topic.
- Explanation: Provide a brief explanation, definition, or additional information for each subtopic.

4. Examples and Illustrations: If the lecture slides contain any examples, illustrations, diagrams, or visuals, include them in the summary.
- Describe the examples and their relevance to the topic.
- Explain how they illustrate or clarify the concepts.
- Include as much information as you can about the example.

5. Key Terms and Definitions: Define and explain any important terms, concepts, theories, or models mentioned in the lecture.
- Create a glossary of key terms along with their definitions.

6. Conclusion: Summarize the main points and takeaways from the lecture.
- Recap the key concepts and highlight the significance of the material covered.

7. Additional Notes:
- Include any additional information or insights from the lecture slides that you believe are relevant and valuable.
- Highlight any important questions or points for further discussion.

8. References:
- Provide references to any external sources or materials mentioned in the lecture slides or used to create the summary.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized JSON format.
If you cannot find information on any of these categories, leave the list empty. If you cannot find information on any specific field, leave it as None. 
Remember to organize the summary in a logical and sequential manner, maintaining clarity and conciseness throughout. The goal is to provide a comprehensive and informative overview of the key information presented in the college course lecture slides.
Only return information you are confident about. If you cannot find information on anything, return an empty JSON. Thank you very much.
"""

# Course v2
# Pros: Can extract course information well, doesn't require GPT4 for accurate results at the moment (limited testing done), refined and cleaner, working with Pydantic Model
# Cons/Issues: 
# Todo: Test run times YAML vs JSON
course_prompt_v2 = """
: this text is from a pdf that contains information about a college course. Please extract information for the following categories:

1. Course name and number
  Provide the class abbreviation followed by the course number (e.g, "CS 381" or "MATH 210"). Don't include anything about the actual course name. 
2. Course description
  Provide a short summary of what the course is about.   
3. Professor name and email 
4. Course schedule
  Provide 
5. Grade weights
6. Grade scaling
7. Course objectives
8. Course materials

Here are some rules to follow: 
1. If there are lecture times that are not explicit such as "T, Th 9:30am-10:45am" or "M W F 10:00am-10:50am", interpret the individual days and separate them (e.g., ["Monday 10:00am-10:50am", "Wednesday 10:00am-10:50am", "Friday 10:00am-10:50am"] or ["Tuesday 9:30am-10:45am", "Thursday 9:30am-10:45am"]).  
2. For grade weights, have the number followed by the % symbol (e.g, "15%" or "75%").
3. For grade scaling, format the range with the lower bound followed by the upper bound with a - symbol in between (e.g, "90-100" or "70-80").

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Thank you.
"""

# Calendar v5
# Changes:
# (+) added class name extraction

calendar_prompt_v5 = """
: this text is from a pdf that contains information about a college course. Please extract the course number and the due dates for the following categories:

1. Homework assignment due dates
2. Midterm and Final Exams due dates
3. Lab due dates
4. Project due dates
5. Quiz due dates
6. Other if you find anything else

Here are the steps that you should take:
1. First, identify the number for the course. An example would be something like CS102 or MATH200.
2. Then, carefully read through the text to find mentions of assignments, exams, labs, projects, quizzes, or any other tasks with due dates. 
3. Then, for each assignment, identify the due date. If the date is not explicitly mentioned, use the provided context to deduce the date.
4. Additionally, capture any relevant information that is related to the assignment, whether that be the name of it or relative information to it.  
5. Return the assignment in "Name | Date: MM/DD/YYYY HH:MM:SS" format please. An example output would be "Name: HW 1 | Date: 01/22/2024 23:59:59". 

Take your time when taking these steps. 

Here are some examples of how the context of a date could be expressed:
1. "HW1 due Wednesday midnight 03/22/24-03/28/24".
2. "(4/15-4/21) English HW4 due Monday midnight".
3. "Exam 1 01/13/24 8AM-10AM". 

Pay close attention to the layout and formatting of the text, as it is crucial for understanding and accurately extracting the due dates. The context surrounding a date mention may include specific weeks, days of the week, or date ranges which will require you to calculate the exact due date.
Remember that we are looking specifically for due dates, not dates posted.
Make sure that the context you are using to interpret the assignments is the correctly associated one. We are in 2024.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Thank you.
"""


####################################################  DEVELOPMENT #########################################################################
####################################################  DEVELOPMENT #########################################################################
####################################################  DEVELOPMENT #########################################################################
####################################################  DEVELOPMENT #########################################################################
####################################################  DEVELOPMENT #########################################################################



# Course v3
# Changes: 
# (+) Major improvements in formatting and extraction of information. 
# (-) Removed objectives and materials for now, as we want to ensure everything else works before adding luxury. 
# Todo:
# - Decide whether or not to split the lecture times to invidual days (MWF --> Monday, Wednesday, Friday). Found this to be a little difficult and unsure whether the payoff is worth the increased complexity.
# - Additional formatting check, specifically with the course name and number.
# - checking for edge cases with formatting. 
# - testing with further models 
course_prompt_v3 = """
: this text is from a pdf that contains information about a college course. Please extract information for the following categories:

1. Course name and number
2. Course description
3. Professor(s)
  a. Name
    i) email
    ii) Lecture times only associated with specific professor
4. Grade weights
  a. Assignment Type
    i) Weight
5. Grade scaling
  a. Grade Type
    i) upper bound
    ii) lower bound

Here are some rules to follow: 
1. For lecture times, identify the day of the week, the start time of the lecture, and the end time of the lecture. If those fields are not explicit, such as "T, Th 9:30am-10:45am", infer using the surrounding context. 
2. For grade weights, only include the percentage value, not the symbol. 
3. For grade scaling, separate the upper bound and the lower bound. If the upper and lower bound aren't explicit, such as "A >= 90%", infer the upper and lower bound using the surrounding context. 
4. If there are multiple professors, separate them. And make sure that the lecture times are only associated per professor. 
5. For course name and number, ensure that it is in the following format: "course_abbreviation course_number". 
6. Ensure that the course description does not exceed more than 75 words. Less is more. 

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Additionally, avoid 
using special characters that may throw off YAML formatting like : or -.
"""


############################################################# OUTDATED ####################################################################
############################################################# OUTDATED ####################################################################
############################################################# OUTDATED ####################################################################
############################################################# OUTDATED ####################################################################
############################################################# OUTDATED ####################################################################
############################################################# OUTDATED ####################################################################


# Calendar v4
# Changes:
# (-) removed end date feature and only collects date once again, mainly because I was running into a lot of issues with output token space, 
# and end date was taking up a lot of space. also didn't think about how useful it would be, and on second thought, it isn't that useful.  
# focus on MVP first, don't go adding new features without thinking. 

calendar_prompt_v4 = """
: this text is from a pdf that contains information about a college course. Please extract due dates for the following categories:

1. Homework assignment due dates
2. Midterm and Final Exams due dates
3. Lab due dates
4. Project due dates
5. Quiz due dates
6. Other if you find anything else

Here are the steps that you should take:
1. First, carefully read through the text to find mentions of assignments, exams, labs, projects, quizzes, or any other tasks with due dates. 
2. Then, for each assignment, identify the due date. If the date is not explicitly mentioned, use the provided context to deduce the date.
3. Additionally, capture any relevant information that is related to the assignment, whether that be the name of it or relative information to it.  
4. Return the assignment in "Name | Date: MM/DD/YYYY HH:MM:SS" format please. An example output would be "Name: HW 1 | Date: 01/22/2024 23:59:59". 

Take your time when taking these steps. 

Here are some examples of how the context of a date could be expressed:
1. "HW1 due Wednesday midnight 03/22/24-03/28/24".
2. "(4/15-4/21) English HW4 due Monday midnight".
3. "Exam 1 01/13/24 8AM-10AM". 

Pay close attention to the layout and formatting of the text, as it is crucial for understanding and accurately extracting the due dates. The context surrounding a date mention may include specific weeks, days of the week, or date ranges which will require you to calculate the exact due date.
Remember that we are looking specifically for due dates, not dates posted.
Make sure that the context you are using to interpret the assignments is the correctly associated one. We are in 2024.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Thank you.
"""

# Calendar v3
# Changes: Attempts to now extract date spans, for example: March 7th, 2024 4PM-6PM before would capture just MM/DD/YYYY, now attempts to
# capture 2 separate dates: March 7th, 2024 4PM and March 7th, 2024 6PM for better accurate representation 

calendar_prompt_v3 = """
: this text is from a pdf that contains information about a college course. Please extract due dates for the following categories:

1. Homework assignment due dates
2. Midterm and Final Exams due dates
3. Lab due dates
4. Project due dates
5. Quiz due dates
6. Other if you find anything else

Here are the steps that you should take:
1. First, carefully read through the text to find mentions of assignments, exams, labs, projects, quizzes, or any other tasks with due dates. 
2. Then, for each assignment, identify the due date. If the date is not explicitly mentioned, use the provided context to deduce the date.
3. Additionally, capture any relevant information that is related to the assignment, whether that be the name of it or relative information to it.  
4. Return the assignment in "Name | Start: MM/DD/YYYY HH:MM:SS | End: MM/DD/YYYY HH:MM:SS" format please. If there does not exist an end date, set it to None. If there exists an end date, return both dates but separate them. An example input is: "02/22/24 8AM-10AM" and the valid output should look like: "Name: Exam 1 | Start Date: 02/22/24 08:00:00 | End Date: 02/22/24 10:00:00". 

Take your time when taking these steps. 

Here are some examples of how the context of a date could be expressed:
1. "HW1 due Wednesday midnight 03/22/24-03/28/24".
2. "(4/15-4/21) English HW4 due Monday midnight".
3. "Exam 1 01/13/24 8AM-10AM". 

Pay close attention to the layout and formatting of the text, as it is crucial for understanding and accurately extracting the due dates. The context surrounding a date mention may include specific weeks, days of the week, or date ranges which will require you to calculate the exact due date.
Remember that we are looking specifically for due dates, not dates posted.
Make sure that the context you are using to interpret the assignments is the correctly associated one. We are in 2024.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Thank you.
"""

# Calendar Prompt v1
# Can correctly extract explicit dates, has trouble interpreting context of dates and extracting it from context
calendar_prompt_v1 = """
: this text is from a pdf that contains information about a college course. I need you to extract important dates that are provided in the document. 
Specifically, look for these categories:

1. Homework assignment due dates
2. Midterm and Final Exams dates
3. Lab dates
4. Project due dates
5. Quiz dates
6. Other if you find anything else

Please ensure that the extracted information is accurate, comprehensive, and structured in the following JSON format:
{"Homework" : [{"name" : {"date" : date, "context" : context}}], "Exams" : [{"name" : {"date" : date, "context" : context}}], "Labs" : [{"name" : {"date" : date, "context" : context}}], "Projects" : [{"name" : {"date" : date, "context" : context}}], "Quizzes" : [{"name" : {"date" : date, "context" : context}}], "Other" : [{"name" : {"date" : date, "context" : context}}]}
Here's an example of what the JSON should look like:
{"Homework" : [{"Homework 1" : {"date" : "01/01/2022", "context" : "worth 15 points"}}], "Exams" : [{"Final Exam" : {"date" : "04/13/2022", "context" : "At the computer lab"}}], "Labs" : [{"Lab 13" : {"date" : "02/24/2022", "context" : "At room 202"}}], "Projects" : [{"Project 3" : {"date" : "05/03/2022", "context" : "None"}}], "Quizzes" : [{"Quiz 4" : {"date" : "03/01/2022", "context" : "last quiz of the year"}}], "Other" : [{"Martin Luther King" : {"date" : "01/17/2022", "context" : None}}]}

If the text mentions any deadlines or events without specific dates but gives enough context to infer a timeline/date (e.g., 'two weeks after the course starts'), please calculate and provide those dates.
If you cannot find information on any of these categories, leave the list empty. If you cannot find information on the date or content field, leave it as None.
Only return information you are confident about. If you cannot find information on anything, return an empty JSON. Thank you very much.
"""

# Calendar Prompt v1.1
# New pipeline that makes extracting information a lot easier. Separates information collection and information organization into two parts. Makes the 
# prompt simpler for the LLM to comprehend better. 

calendar_prompt_part1_yaml = """
: this text is from a pdf that contains information about a college course. I need you to extract important dates that are provided in the document. 
Specifically, look for these categories:

1. Homework assignment due dates
2. Midterm and Final Exams dates
3. Lab dates
4. Project due dates
5. Quiz dates
6. Other if you find anything else

Capture the context (any relevant information) for each of these categories as well.  

If the text mentions any deadlines or events without specific dates but gives enough context to infer a timeline/date (e.g., 'two weeks after the course starts'), please calculate and provide those dates.
Here's an example for that: "4/15-4/22 HW due Monday", you should the Monday of that week based on the current year calendar which is 2024.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion
"""

calendar_prompt_part2_yaml = """
: This text contains information about a college course. I need you to parse this text and convert it to the following YAML format:
Homework:
  - name:
      date: date
      context: context
Exams:
  - name: 
      date: date
      context: context
Labs:
  - name:
      date: date
      context: context
Projects:
  - name:
      date: date
      context: context
Quizzes:
  - name:
      date: date
      context: context
Other:
  - name:
      date: date
      context: context

Here's an example of what it should look like:

Homework:
  - "Homework 1":
      date: "01/02/23"
      context: "Worth 10 points"
  - "Homework 2":
      date: "12/14/24"
      context: "Worth 5 points"
Exams:
  - "Midterm": 
      date: "04/02/23"
      context: "4:00 PM at room 210"
  - "Final Exam": 
      date: "05/02/23"
      context: "4:00 PM at room 211"
Labs:
  - "Lab 1":
      date: "02/23/23"
      context: "Bring your safety goggles"
Projects:
  - "Project 2":
      date: "02/06/23"
      context: "must submit it online"
Quizzes:
  - "Quiz 1":
      date: "05/02/23"
      context: "Bring your pencil"
  - "Quiz 2":
      date: "05/09/23"
      context: "Bring your pencil"
Other:
  - "Christmas":
      date: "12/25/23"
      context: "No school"
  - "Spring Break":
      date: "05/02/23-08/23/23"
      context: "No school"

"""

calendar_prompt_part1_json = """
: this text is from a pdf that contains information about a college course. I need you to extract important dates that are provided in the document. 
Specifically, look for these categories:

1. Homework assignment due dates
2. Midterm and Final Exams dates
3. Lab dates
4. Project due dates
5. Quiz dates
6. Other if you find anything else

Capture the context (any relevant information) for each of these categories as well.  

If the text mentions any deadlines or events without specific dates but gives enough context to infer a timeline/date (e.g., 'two weeks after the course starts'), please calculate and provide those dates.
Here's an example for that: "4/15-4/22 HW due Monday", you should the Monday of that week based on the current year calendar which is 2024.

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion
"""

calendar_prompt_part2_json = """
: This text contains information about a college course. I need you to parse this text and convert it to the following JSON format:

{"Homework" : [{"name" : {"date" : date, "context" : context}}], "Exams" : [{"name" : {"date" : date, "context" : context}}], "Labs" : [{"name" : {"date" : date, "context" : context}}], "Projects" : [{"name" : {"date" : date, "context" : context}}], "Quizzes" : [{"name" : {"date" : date, "context" : context}}], "Other" : [{"name" : {"date" : date, "context" : context}}]}
Here's an example of what the JSON should look like:
{"Homework" : [{"Homework 1" : {"date" : "01/01/2022", "context" : "worth 15 points"}}], "Exams" : [{"Final Exam" : {"date" : "04/13/2022", "context" : "At the computer lab"}}], "Labs" : [{"Lab 13" : {"date" : "02/24/2022", "context" : "At room 202"}}], "Projects" : [{"Project 3" : {"date" : "05/03/2022", "context" : "None"}}], "Quizzes" : [{"Quiz 4" : {"date" : "03/01/2022", "context" : "last quiz of the year"}}], "Other" : [{"Martin Luther King" : {"date" : "01/17/2022", "context" : None}}]}
"""


course_prompt = """
: this text is from a pdf that contains information about a college course. Please extract information for the following categories:

1. Course name and number
2. Course description
3. Professor name and email 
4. Course schedule
5. Grade weights
6. Grade scaling
7. Course objectives
8. Course materials
9. Other (e.g., attendance policy, cheating policy)

Please ensure that the extracted information is accurate, comprehensive, and structured in the following JSON format:
{"name" : name, "description" : description, "professor" : {"name" : name, "email" : email, "lecture_location" : lecture_location, "lecture_times" : [lecture_times,...]},  "weights" : {"type" : weight, "type2" : weight2...}, "scaling" : {"grade" : range, "grade2" : range2...}, "objectives" : [objectives], "materials" : [materials], "other" : [other]}

Here's an example of what the JSON should look like:
{"name" : "MATH210", "description" : "Calculus III is a course where we observe and study multiple variables changing.", "Professor" : {"name" : "John Pork", "email" : None, "location" : "Academic Center Room 210", "times" : ["Monday 2pm-3pm", "Wednesday 2pm-3pm", "Friday 4pm-5pm"]}, "weights" : {"Exams" : "20%", "Homework" : "10%", "Projects" : "25%", "Labs" : "15%", "Attendance" : "10%", "Quizzes" : "20%"}, "scaling" : {"A" : "90-100%", "B" : "80-89%", "C" : "70-79%", "D" : "60-69%", "F" : "<60%"}, "objectives" : ["Develop problem solving skills", "Understand relationships between multiple variables", "Learn to communicate effectively."], "materials" : ["the textbook for this course can be found at www.getyourtextbookhere.com", "you must sign up for the online textbook at www.whydoweneedtobuytextbooks.com"]"other" : ["You can skip a total of 5 lectures and 5 labs during the course.", "Getting caught cheating is an automatic fail in the course."]}

Rules:
If there are lecture times that are not obvious such as "TTh 9:30am-10:45am" or "MWF 10:00am-10:50am", interpret that and separate it to separate days.
If you cannot find information on any of these categories, leave the list empty. If you cannot find information on any specific field, leave it as None. 
Only return information you are confident about. If you cannot find information on anything, return an empty JSON. 

Formatting:
lecture_times: ["day_of_week time_window", ...] (e.g., "Monday 9:30am-10:45am")
weights: "weight%" (e.g., "15%")
scaling: "lowerbound-upperbound%" (e.g., "90-100%")
Please format the information exactly as stated, even the littlest details. 

"""

calendar_prompt_json = """
: This text contains information about a college course. I need you to parse this text and convert it to the following JSON format:

{"Homework" : [{"name" : {"date" : date, "context" : context}}], "Exams" : [{"name" : {"date" : date, "context" : context}}], "Labs" : [{"name" : {"date" : date, "context" : context}}], "Projects" : [{"name" : {"date" : date, "context" : context}}], "Quizzes" : [{"name" : {"date" : date, "context" : context}}], "Other" : [{"name" : {"date" : date, "context" : context}}]}
Here's an example of what the JSON should look like:
{"Homework" : [{"Homework 1" : {"date" : "01/01/2022", "context" : "worth 15 points"}}], "Exams" : [{"Final Exam" : {"date" : "04/13/2022", "context" : "At the computer lab"}}], "Labs" : [{"Lab 13" : {"date" : "02/24/2022", "context" : "At room 202"}}], "Projects" : [{"Project 3" : {"date" : "05/03/2022", "context" : "None"}}], "Quizzes" : [{"Quiz 4" : {"date" : "03/01/2022", "context" : "last quiz of the year"}}], "Other" : [{"Martin Luther King" : {"date" : "01/17/2022", "context" : None}}]}
"""


# Calendar v2
# Pros: Can interpret date contexts better 
# Cons/Issues: Still has room to improve, may be overfitting on one format with the examples I provided, may not generalize to most 
# documents or models even. 
# Todo: Start implementing specific techniques (few shot, chain of thought...), we may not need the examples if we use a fine tuned model
calendar_prompt_v2 = """
: this text is from a pdf that contains information about a college course. Please extract due dates for the following categories:

1. Homework assignment due dates
2. Midterm and Final Exams due dates
3. Lab due dates
4. Project due dates
5. Quiz due dates
6. Other if you find anything else

Here are the steps that you should take:
1. First, carefully read through the text to find mentions of assignments, exams, labs, projects, quizzes, or any other tasks with due dates. 
2. Then, for each assignment identified, note the due date. If the date is not explicitly mentioned, use the provided context to deduce the date. 
3. Return the due date in MM/DD/YYY format please.

Take your time when taking these steps. 

Here are some examples of how the context of a date could be expressed:
1. "HW1 due Wednesday midnight 03/22/24-03/28/24".
2. "(4/15-4/21) English HW4 due Monday midnight".

Pay close attention to the layout and formatting of the text, as it is crucial for understanding and accurately extracting the due dates. The context surrounding a date mention may include specific weeks, days of the week, or date ranges which will require you to calculate the exact due date.
Remember that we are looking specifically for due dates, not dates posted.  
Make sure that the context you are using to interpret the assignments is the correctly associated one. We are in 2024.
If you can't find a date associated with an assignment, try to capture potential context about it and return that. 

Please ensure that the extracted information is accurate, comprehensive, and structured in an organized fashion. Thank you.
"""
