/* eslint-disable no-undef */
// include the readline module using require function
const readLine = require("readline");

// create a readline interface for answering questions...
const rl = readLine.createInterface({
    input: process.stdin,
    output: process.stdout
});

// create an array of questions...
const questions = [
    "What is your name? ",
    "Where do you live? ",
    "What are you going to do with node js? "
];

// create a function to simply send an array of questions and a callback to handle once we have all of the answers
const collectAnswers = (questions, done) => {
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
    }
    
    rl.question(firstQuestion, questionAnswered);
}

// call the function to collect the answers and callback which displays the thank you message...
collectAnswers(questions, answers => {
    console.log("Thank you for your answers. ");
    console.log(answers);
    process.exit();
});