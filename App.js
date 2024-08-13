import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [question, setQuestion] = useState('');
  const [answers, setAnswers] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState('');
  const [askedQuestions, setAskedQuestions] = useState([]);
  const [mainQuestionsCount, setMainQuestionsCount] = useState(0);
  const [surveyCompleted, setSurveyCompleted] = useState(false);
  const [selectedAnswerIndex, setSelectedAnswerIndex] = useState(null);

  useEffect(() => {
    // Fetch the initial question
    axios.get('http://127.0.0.1:5000/survey/start')
      .then(response => {
        setQuestion(response.data.question);
        setAnswers(response.data.answers);
        setCurrentQuestion(response.data.question);
      })
      .catch(error => {
        console.error("There was an error fetching the question!", error);
      });
  }, []);

  const handleAnswer = (answer, index) => {
    if (surveyCompleted) return;

    setSelectedAnswerIndex(index);

    const data = {
      current_question: currentQuestion,
      answer: answer,
      asked_questions: [...askedQuestions, currentQuestion]
    };

    axios.post('http://127.0.0.1:5000/survey/answer', data)
      .then(response => {
        setQuestion(response.data.question);
        setAnswers(response.data.answers);
        setCurrentQuestion(response.data.question);
        setAskedQuestions([...askedQuestions, currentQuestion]);
        setSelectedAnswerIndex(null);  // Reset the selected answer index

        // Check if it's a main question or a follow-up question
        if (!response.data.is_follow_up) {
          setMainQuestionsCount(mainQuestionsCount + 1);
        }

        // End the survey if 10 main questions have been asked
        if (mainQuestionsCount + 1 >= 10) {
          setSurveyCompleted(true);
        }
      })
      .catch(error => {
        console.error("There was an error submitting the answer!", error);
      });
  };

  if (surveyCompleted) {
    return (
      <div className="survey-container">
        <h1 className="title">Survey Completed</h1>
        <p>Thank you for your participation!</p>
      </div>
    );
  }

  return (
    <div className="survey-container">
      <header>
        <h1>Survey Personalization Based on Dynamic Responses</h1>
        <p>Author: Mohan Raja (SVCE - 2025)</p>
        <table className="tech-stack-table">
          <thead>
            <tr>
              <th>Component</th>
              <th>Technology</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Frontend</td>
              <td>React.js</td>
            </tr>
            <tr>
              <td>Backend</td>
              <td>Flask</td>
            </tr>
            <tr>
              <td>ML Algorithm</td>
              <td>Random Forest Classifier</td>
            </tr>
            <tr>
              <td>API Communication</td>
              <td>Axios</td>
            </tr>
            <tr>
              <td>Styling</td>
              <td>CSS</td>
            </tr>
            <tr>
              <td>Cloud</td>
              <td>Azure</td>
            </tr>
          </tbody>
        </table>
      </header>
      <h2 className="title">Survey</h2>
      <h3 className="question">Question {mainQuestionsCount + 1}: {question}</h3>
      <form className="form">
        {answers.map((answer, index) => (
          <div key={index} className="answer-container">
            <input
              type="radio"
              id={`answer${index}`}
              name="answer"
              value={answer}
              checked={selectedAnswerIndex === index}
              onChange={() => handleAnswer(answer, index)}
              className="radio-button"
            />
            <label htmlFor={`answer${index}`} className="answer-label">{answer}</label>
          </div>
        ))}
      </form>
    </div>
  );
};

export default App;

