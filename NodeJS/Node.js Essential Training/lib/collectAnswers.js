/* eslint-disable no-undef */
// include the readline module using require function
const readLine = require("readline");

const { EventEmitter } = require("events");
const emitter = new EventEmitter();

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
        emitter.emit("answer", answer);
        answers.push(answer);
        if (answers.length < questions.length) {
            rl.question(questions[answers.length], questionAnswered);
        } else {
            emitter.emit("complete", answers);
            done(answers);
        }
    };
    
    rl.question(firstQuestion, questionAnswered);

    return emitter;
};