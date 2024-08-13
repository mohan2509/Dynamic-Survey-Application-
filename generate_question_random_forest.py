import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Define the expanded lists of negative, positive, and neutral responses
negative_responses = [
    'Dissatisfied', 'Very dissatisfied', 'Poor', 'Very poor', 'Poorly', 'Very poorly', 
    'Ineffective', 'Very ineffective', 'Irrelevant', 'Very irrelevant', 'Outdated', 
    'Very outdated', 'Unclear', 'Very unclear', 'Unapproachable', 'Very unapproachable', 
    'Unknowledgeable', 'Very unknowledgeable', 'Unresponsive', 'Very unresponsive', 
    'Boring', 'Very boring', 'Lacking', 'Very lacking', 'Not very applicable', 
    'Not applicable at all', 'Less', 'Much less', 'Average'
]

positive_responses = [
    'Very satisfied', 'Satisfied', 'Excellent', 'Good', 'Very effective', 'Effective', 
    'Very comprehensive', 'Comprehensive', 'Very responsive', 'Responsive', 'Very engaging', 
    'Engaging', 'Very knowledgeable', 'Knowledgeable', 'Very approachable', 'Approachable', 
    'Very clear', 'Clear', 'Very up-to-date', 'Up-to-date', 'Very relevant', 'Relevant', 
    'Very well', 'Well', 'Highly applicable', 'Applicable', 'Much more', 'More'
]

neutral_responses = ['Neutral', 'As expected', 'Somewhat applicable']

# Define templates for follow-up questions
follow_up_templates = {
    "Dissatisfied": "What specifically caused your dissatisfaction with the {category}?",
    "Very dissatisfied": "What specifically caused your dissatisfaction with the {category}?",
    "Poor": "What aspects of the {category} did not meet your expectations?",
    "Very poor": "What aspects of the {category} did not meet your expectations?",
    "Poorly": "What aspects of the {category} did not meet your expectations?",
    "Very poorly": "What aspects of the {category} did not meet your expectations?",
    "Ineffective": "How could the {category} be improved?",
    "Very ineffective": "How could the {category} be improved?",
    "Neutral": "What is the one thing that you would like us to improve on this {category}?",
    "Irrelevant": "Why do you feel the course content was irrelevant?",
    "Very irrelevant": "Why do you feel the course content was very irrelevant?",
    "Outdated": "Why do you feel the content was outdated?",
    "Very outdated": "Why do you feel the content was very outdated?",
    "Unclear": "What aspects of the {category} were unclear?",
    "Very unclear": "What aspects of the {category} were very unclear?",
    "Unapproachable": "Why did you find the {category} unapproachable?",
    "Very unapproachable": "Why did you find the {category} very unapproachable?",
    "Unknowledgeable": "Why did you find the {category} unknowledgeable?",
    "Very unknowledgeable": "Why did you find the {category} very unknowledgeable?",
    "Unresponsive": "What aspects of the {category} were unresponsive?",
    "Very unresponsive": "What aspects of the {category} were very unresponsive?",
    "Boring": "Why did you find the {category} boring?",
    "Very boring": "Why did you find the {category} very boring?",
    "Lacking": "What aspects of the {category} were lacking?",
    "Very lacking": "What aspects of the {category} were very lacking?",
    "Not very applicable": "Why did you find the {category} not very applicable?",
    "Not applicable at all": "Why did you find the {category} not applicable at all?",
    "Less": "Why do you feel the learning from the course was less than expected?",
    "Much less": "Why do you feel the learning from the course was much less than expected?",
    "Average": "What aspects of the {category} were average?"
}

# Define a pool of potential follow-up answers for each category and response
follow_up_answers_pool = {
    "Overall Quality": {
        "Dissatisfied": ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"],
        "Very dissatisfied": ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"]
    },
    "Course Content": {
        "Dissatisfied": ["Not enough depth", "Too broad", "Not relevant", "Outdated", "Other"],
        "Very dissatisfied": ["Not enough depth", "Too broad", "Not relevant", "Outdated", "Other"]
    },
    "Course Material": {
        "Dissatisfied": ["Low quality", "Not enough examples", "Too theoretical", "Too complex", "Other"],
        "Very dissatisfied": ["Low quality", "Not enough examples", "Too theoretical", "Too complex", "Other"]
    },
    "Learning Experience": {
        "Poor": ["Boring sessions", "Repetitive content", "Lack of hands-on activities", "Other"],
        "Very poor": ["Boring sessions", "Repetitive content", "Lack of hands-on activities", "Other"]
    },
    "Pricing": {
        "Dissatisfied": ["Too expensive", "Not worth the price", "Hidden costs", "Other"],
        "Very dissatisfied": ["Too expensive", "Not worth the price", "Hidden costs", "Other"]
    },
    "Learning Outcomes": {
        "Ineffective": ["Did not meet expectations", "Too basic", "Not applicable", "Other"],
        "Very ineffective": ["Did not meet expectations", "Too basic", "Not applicable", "Other"]
    },
    "Expectations": {
        "Less": ["Fell short", "Partially met", "Unclear goals", "Other"],
        "Much less": ["Fell short", "Partially met", "Unclear goals", "Other"]
    },
    "Skills": {
        "Ineffective": ["Not relevant", "Outdated", "Too basic", "Other"],
        "Very ineffective": ["Not relevant", "Outdated", "Too basic", "Other"]
    },
    "Job": {
        "Not very applicable": ["Skills not applicable", "Outdated skills", "Too basic", "Other"],
        "Not applicable at all": ["Skills not applicable", "Outdated skills", "Too basic", "Other"]
    },
    "Learning Goals": {
        "Poorly": ["Unmet expectations", "Not clear", "Partially met", "Other"],
        "Very poorly": ["Unmet expectations", "Not clear", "Partially met", "Other"]
    },
    "Relevance": {
        "Irrelevant": ["Not relevant", "Outdated", "Too basic", "Other"],
        "Very irrelevant": ["Not relevant", "Outdated", "Too basic", "Other"]
    },
    "Course Coverage": {
        "Lacking": ["Not comprehensive", "Too basic", "Outdated", "Other"],
        "Very lacking": ["Not comprehensive", "Too basic", "Outdated", "Other"]
    },
    "Engagement": {
        "Boring": ["Not engaging", "Too repetitive", "Lack of practical exercises", "Other"],
        "Very boring": ["Not engaging", "Too repetitive", "Lack of practical exercises", "Other"]
    },
    "Industry Matches": {
        "Outdated": ["Not up-to-date", "Not relevant", "Too basic", "Other"],
        "Very outdated": ["Not up-to-date", "Not relevant", "Too basic", "Other"]
    },
    "Subject Knowledge": {
        "Poorly": ["Shallow knowledge", "Outdated information", "Too basic", "Other"],
        "Very poorly": ["Shallow knowledge", "Outdated information", "Too basic", "Other"]
    },
    "Instructor Effectiveness": {
        "Unclear": ["Poor delivery", "Not engaging", "Too fast", "Other"],
        "Very unclear": ["Poor delivery", "Not engaging", "Too fast", "Other"]
    },
    "Instructor Cooperation": {
        "Unapproachable": ["Not supportive", "Unresponsive", "Other"],
        "Very unapproachable": ["Not supportive", "Unresponsive", "Other"]
    },
    "Instructor Skills": {
        "Unknowledgeable": ["Lack of knowledge", "Not engaging", "Too fast", "Other"],
        "Very unknowledgeable": ["Lack of knowledge", "Not engaging", "Too fast", "Other"]
    },
    "Instructor Engagement": {
        "Ineffective": ["Not engaging", "Too fast", "Too slow", "Other"],
        "Very ineffective": ["Not engaging", "Too fast", "Too slow", "Other"]
    },
    "Instructor Responses": {
        "Poorly": ["Poor responses", "Not engaging", "Too fast", "Other"],
        "Very poorly": ["Poor responses", "Not engaging", "Too fast", "Other"]
    },
    "Technical Support": {
        "Dissatisfied": ["Unresponsive", "Not helpful", "Slow response", "Other"],
        "Very dissatisfied": ["Unresponsive", "Not helpful", "Slow response", "Other"]
    },
    "Technical Response Speed": {
        "Unresponsive": ["Slow response", "Not helpful", "Other"],
        "Very unresponsive": ["Slow response", "Not helpful", "Other"]
    },
    "Technical Support Usefulness": {
        "Ineffective": ["Not helpful", "Unresponsive", "Slow response", "Other"],
        "Very ineffective": ["Not helpful", "Unresponsive", "Slow response", "Other"]
    },
    "Technical Support Hours": {
        "Dissatisfied": ["Not available", "Limited hours", "Unresponsive", "Other"],
        "Very dissatisfied": ["Not available", "Limited hours", "Unresponsive", "Other"]
    },
    "Technical Support Assistance": {
        "Poorly": ["Poor assistance", "Not helpful", "Slow response", "Other"],
        "Very poorly": ["Poor assistance", "Not helpful", "Slow response", "Other"]
    }
}

# Load the dataset
df = pd.read_csv('survey_data.csv')

# Define categories
categories = ["Overall Quality", "Course Content", "Course Material", "Learning Experience", "Pricing", "Learning Outcomes", "Expectations", "Skills", "Job", "Learning Goals", "Relevance", "Course Coverage", "Engagement", "Industry Matches", "Subject Knowledge", "Instructor Effectiveness", "Instructor Cooperation", "Instructor Skills", "Instructor Engagement", "Instructor Responses", "Technical Support", "Technical Response Speed", "Technical Support Usefulness", "Technical Support Hours", "Technical Support Assistance"]

# Generate follow-up questions dictionary
follow_up_questions = {category: {response: template.format(category=category.lower()) 
                                  for response, template in follow_up_templates.items()} 
                       for category in categories}

# Encode categorical variables
le_question = LabelEncoder()
le_answer = LabelEncoder()

# Collect all unique follow-up answers from the follow-up answers pool
all_follow_up_answers = set()
for category_answers in follow_up_answers_pool.values():
    for answers in category_answers.values():
        all_follow_up_answers.update(answers)

# Generate a list of all questions, including follow-up questions
all_questions = list(df['question'].unique())
for category, questions in follow_up_questions.items():
    all_questions.extend(questions.values())

# Fit the LabelEncoders on the complete set of questions and answers
le_question.fit(all_questions)
all_answers = set()
df['answers'].apply(lambda x: all_answers.update(eval(x)))
all_answers.update(all_follow_up_answers) 
all_answers = list(all_answers)
le_answer.fit(all_answers)

# Transform questions and answers
df['question_encoded'] = le_question.transform(df['question'])
df['answers_encoded'] = df['answers'].apply(lambda x: [le_answer.transform([i])[0] for i in eval(x)])
df = df.explode('answers_encoded')

# Separate follow-up questions into a different dataframe
follow_up_rows = []
for category, questions in follow_up_questions.items():
    for response, question in questions.items():
        follow_up_answers = follow_up_answers_pool.get(category, {}).get(response, ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"])
        #print(f"Creating follow-up row - Category: {category}, Response: {response}, Follow-up Question: {question}, Follow-up Answers: {follow_up_answers}")
        follow_up_rows.append({
            'category': category,
            'question': question,
            'answers': str(follow_up_answers),
            'is_follow_up': True
        })




follow_up_df = pd.DataFrame(follow_up_rows)

# Re-encode the new follow-up questions
follow_up_df['question_encoded'] = le_question.transform(follow_up_df['question'])
follow_up_df['answers_encoded'] = follow_up_df['answers'].apply(lambda x: [le_answer.transform([i])[0] for i in eval(x)])
follow_up_df = follow_up_df.explode('answers_encoded')

# Ensure the follow-up questions have the correct answers
for idx, row in follow_up_df.iterrows():
    question = row['question']
    if question in follow_up_questions[row['category']].values():
        specific_answers = follow_up_answers_pool.get(row['category'], {}).get(row['answers'], ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"])
        #print(f"Updating follow-up DataFrame - Category: {row['category']}, Response: {row['answers']}, Specific Answers: {specific_answers}")
        follow_up_df.at[idx, 'answers'] = str(specific_answers)




# Create a dataset for the decision tree for main questions
data_main = df[['question_encoded', 'answers_encoded']]

# Define features and target for main questions
X_main = data_main[['question_encoded', 'answers_encoded']]
y_main = df['question_encoded']

# Train Random Forest Classifier for main questions
clf_main = RandomForestClassifier()
clf_main.fit(X_main, y_main)

# Function to get the next main question based on the current question and answer
def get_next_main_question(current_question, answer, asked_questions):
    current_question_encoded = le_question.transform([current_question])[0]
    answer_encoded = le_answer.transform([answer])[0]
    
    next_question_encoded = clf_main.predict(np.array([[current_question_encoded, answer_encoded]]))[0]
    next_question = le_question.inverse_transform([next_question_encoded])[0]
    
    # Ensure the next question is not the same as the current question and has not been asked already
    while next_question in asked_questions:
        next_question_idx = (np.random.randint(0, len(df))) % len(df)
        next_question = le_question.inverse_transform([df.iloc[next_question_idx]['question_encoded']])[0]
    
    next_answers = eval(df[df['question'] == next_question]['answers'].values[0])
    
    #print(f"Main Question - Current: {current_question}, Answer: {answer}, Next: {next_question}, Next Answers: {next_answers}")
    return next_question, next_answers

# Function to get the follow-up question based on the user's negative response
def get_follow_up_question(current_question, user_answer):
    # Check if the current question is in the main dataframe
    if current_question in df['question'].values:
        category = df[df['question'] == current_question]['category'].values[0]
    else:
        # If not found in the main dataframe, look in the follow-up dataframe
        category = follow_up_df[follow_up_df['question'] == current_question]['category'].values[0]
    
    follow_up_question = follow_up_questions[category][user_answer]
    follow_up_answers = follow_up_answers_pool.get(category, {}).get(user_answer, ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"])
    #print(f"Follow-up Question - Category: {category}, User Answer: {user_answer}, Follow-up Question: {follow_up_question}, Follow-up Answers: {follow_up_answers}")
    return follow_up_question, follow_up_answers

# Interactive survey
current_question = "How satisfied are you with the overall quality of the course?"
questions_asked = 0
minimum_questions = 10
asked_questions = set()

while questions_asked < minimum_questions:
    if current_question in df['question'].values:
        answers = eval(df[df['question'] == current_question]['answers'].values[0])
    else:
        row = follow_up_df[follow_up_df['question'] == current_question]
        if row.empty:
            answers = ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"]
            #print(f"Fallback to default follow-up answers for {current_question}: {answers}")

    print(f"\nCurrent Question: {current_question}")
    for i, ans in enumerate(answers):
        print(f"{i + 1}. {ans}")

    try:
        user_answer_idx = int(input("Select an answer (by number): ")) - 1
        if user_answer_idx < 0 or user_answer_idx >= len(answers):
            raise IndexError("Invalid selection")
        user_answer = answers[user_answer_idx]
        #print(f"User selected: {user_answer}")
    except (ValueError, IndexError) as e:
        print("Invalid input. Please select a valid option.")
        continue

    # Determine if the response is positive, negative, or neutral
    is_negative = user_answer in negative_responses
    is_neutral = user_answer in neutral_responses
    is_positive = user_answer in positive_responses

    #print(f"Is negative: {is_negative}, Is neutral: {is_neutral}, Is positive: {is_positive}")

    asked_questions.add(current_question)
    should_follow_up = is_negative #or is_neutral
    #print(f"Should follow up: {should_follow_up}")

    if should_follow_up:
        current_question, answers = get_follow_up_question(current_question, user_answer)
        #print(f"Transitioning to follow-up question: {current_question} with answers: {answers}")
    else:
        questions_asked += 1;
        current_question, answers = get_next_main_question(current_question, user_answer, asked_questions)
        #print(f"Transitioning to next main question: {current_question} with answers: {answers}")

    # Print debug information
    #print(f"Next Question: {current_question}")
    #print(f"Asked Questions: {asked_questions}")
    print(f"questions_asked : {questions_asked}")

print("\nEnd of survey. Thank you for your participation!")
