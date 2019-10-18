/*
Process object is available globally and it contains information about 
the current process as well as the tools to allow us to interact with that process.
*/

//To get the current process ID
console.log(process.pid);

//To get the current version of Node.js which is being used to run that process
console.log(process.versions.node);

//To collect information from the terminal when we load the application
//Argument variable that is sent to the process when we run it.
//argv contains everything that we typed to run the process in array form.
console.log(process.argv);

//destructuring the array...
const [, , firstName, lastName] = process.argv; //run this in command line: node globalProcess Rahul Dhangar
console.log(`Your name is ${firstName} ${lastName}`);

//create a function to grab the variable flags from command line
const grab = flag => {
    let indexAfterFlag = process.argv.indexOf(flag) + 1;
    return process.argv[indexAfterFlag];
};

//provide flags to give names to variables we are passing:
//node globalProcess --user Rahul --greeting "Welcome to Node world!"
const greeting = grab("--greeting");
const user = grab("--user");

console.log(`${greeting} ${user}`);