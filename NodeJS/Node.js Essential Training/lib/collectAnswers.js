/* eslint-disable no-undef */
// include the readline module using require function
const readLine = require("readline");

const rl = readLine.createInterface({
    input: process.stdin,
    output: process.stdout
});

module.exports = (questions, done = f => f) => {
    const answers = [];
    // destructuring the question from the array of questions
    const [firstQuestion] = questions;

    // function to be invoked upon answering the question...
    const questionAnswered = answer => {
        answers.push(answer);
        if (answers.length < questions.length) {
            rl.question(questions[answers.length], questionAnswered);
        } else {
            done(answers);
        }
    };
    
    rl.question(firstQuestion, questionAnswered);
};