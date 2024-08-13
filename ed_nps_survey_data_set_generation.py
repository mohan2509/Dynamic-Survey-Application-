import openai 
import random
import json
import time

# Set your OpenAI API key
openai.api_key = 'sk-None-R3Yu2PVASyczaqQOUV3jT3BlbkFJFEh4sarmA9x02cklEKQr'

def generate_questions(prompt, num_samples=10):
    questions = []
    for _ in range(num_samples):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    n=1
                )
                questions.append(response['choices'][0]['message']['content'].strip())
                break
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Waiting for 60 seconds...")
                time.sleep(60)
    return questions

def generate_answers(question, num_samples=3):
    answers = []
    prompt = f"Provide three plausible answers for the survey question: {question}"
    for _ in range(num_samples):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=50,
                    n=1
                )
                answers.append(response['choices'][0]['message']['content'].strip())
                break
            except openai.error.RateLimitError:
                print("Rate limit exceeded. Waiting for 60 seconds...")
                time.sleep(60)
    return answers

categories = {
    "Satisfaction": "Generate a question related to the overall satisfaction of the students with the course.",
    "Learning Outcomes": "Generate a question related to the learning outcomes of the course.",
    "Course Content": "Generate a question related to the content of the course.",
    "Instructor Effectiveness": "Generate a question related to the effectiveness of the instructor.",
    "Technical Support": "Generate a question related to the technical support provided during the course.",
    "Platform": "Generate a question related to the platform used for delivering the course.",
    "Referral": "Generate a question related to the likelihood of recommending the course to others.",
    "Gamification": "Generate a question related to the gamification elements in the course.",
    "Job Support": "Generate a question related to the job support provided after the course.",
    "Infrastructure": "Generate a question related to the infrastructure provided for the course.",
    "Duration": "Generate a question related to the duration of the course.",
    "Classroom Support": "Generate a question related to the classroom support provided during the course.",
    "Pre-Classroom Support": "Generate a question related to the support provided before the classroom sessions.",
    "Post-Classroom Support": "Generate a question related to the support provided after the classroom sessions.",
    "Resume Assistance": "Generate a question related to the resume assistance provided by the course.",
    "Interview Assistance": "Generate a question related to the interview assistance provided by the course.",
    "Overall Rating": "Generate a question related to the overall rating of the course."
}

# Generate questions for each category
survey_data = []
for category, prompt in categories.items():
    print(f"Generating questions for category: {category}")
    questions = generate_questions(prompt, num_samples=5)  # Reduced number of samples
    for question in questions:
        answers = generate_answers(question, num_samples=2)  # Reduced number of samples
        survey_data.append({'category': category, 'question': question, 'answers': answers})

# Shuffle the survey data to ensure randomness
random.shuffle(survey_data)

# Output a sample of the generated data
for data in survey_data[:10]:  
    print(f"Category: {data['category']}")
    print(f"Question: {data['question']}")
    for i, answer in enumerate(data['answers'], 1):
        print(f"Answer {i}: {answer}")
    print("-" * 50)

# Save the generated data to a file
with open('survey_data.json', 'w') as f:
    json.dump(survey_data, f, indent=4)