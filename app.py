from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from survey_config import negative_responses, positive_responses, neutral_responses, follow_up_templates, follow_up_answers_pool

app = Flask(__name__)
CORS(app)

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
    
    while next_question in asked_questions:
        next_question_idx = (np.random.randint(0, len(df))) % len(df)
        next_question = le_question.inverse_transform([df.iloc[next_question_idx]['question_encoded']])[0]
    
    next_answers = eval(df[df['question'] == next_question]['answers'].values[0])
    return next_question, next_answers

# Function to get the follow-up question based on the user's negative response
def get_follow_up_question(current_question, user_answer):
    if current_question in df['question'].values:
        category = df[df['question'] == current_question]['category'].values[0]
    else:
        category = follow_up_df[follow_up_df['question'] == current_question]['category'].values[0]
    
    follow_up_question = follow_up_questions[category][user_answer]
    follow_up_answers = follow_up_answers_pool.get(category, {}).get(user_answer, ["Lack of clarity", "Too fast", "Too slow", "Lack of interaction", "Other"])
    return follow_up_question, follow_up_answers

# Endpoint to start the survey
@app.route('/survey/start', methods=['GET'])
def start_survey():
    initial_question = "How satisfied are you with the overall quality of the course?"
    answers = eval(df[df['question'] == initial_question]['answers'].values[0])
    return jsonify({"question": initial_question, "answers": answers})

# Endpoint to handle user answers and get the next question
@app.route('/survey/answer', methods=['POST'])
def answer_question():
    data = request.json
    current_question = data['current_question']
    user_answer = data['answer']
    asked_questions = set(data['asked_questions'])
    
    is_negative = user_answer in negative_responses
    is_neutral = user_answer in neutral_responses
    
    should_follow_up = is_negative or is_neutral
    
    if should_follow_up:
        next_question, answers = get_follow_up_question(current_question, user_answer)
    else:
        asked_questions.add(current_question)
        next_question, answers = get_next_main_question(current_question, user_answer, asked_questions)
    
    return jsonify({"question": next_question, "answers": answers})

# Endpoint to end the survey
@app.route('/survey/end', methods=['GET'])
def end_survey():
    return jsonify({"message": "Thank you for your participation!"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

