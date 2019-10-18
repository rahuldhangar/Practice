/* Simple question and answer app that runs in terminal */

//create an array of questions
const ques = [
    "What is your name?",
    "What would you rather be doing?",
    "What is your preferred programming language?"
];

//declare ask() function to show the questions on screen
const ask = (i = 0) => {
    process.stdout.write(`\n ${ques[i]}`);
    process.stdout.write(` > `);

};

//invoke the ask() function
ask();

//create an aray for storing answers
const ans = [];

//get answers to questions from stdin object
process.stdin.on('data', d => {
    ans.push(d.toString().trim());
    if(ans.length < ques.length) {
        ask(ans.length);
    } else {
        process.exit();
    }
});

//handle the process exit
process.on('exit', () => {
    //destructuring the array and create variables
    const [name, activity, lang] = ans;

    //showing the output on screen based on the answers
    console.log(`
    
    Thank you for answers.

    Go ${activity} ${name} you can write ${lang} later!!!
    `);

});
