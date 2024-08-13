# survey_config.py

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

