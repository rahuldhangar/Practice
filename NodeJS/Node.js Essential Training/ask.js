/**
 * Collect information with readline
 */

//load the reaLine module using require...
const readLine = require("readline");

// create a readling interface... to ask questions and collect input from terminal
const rl = readLine.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question("How do you like Node? ", answer => {
    console.log(`Your answer: ${answer}`);
});
