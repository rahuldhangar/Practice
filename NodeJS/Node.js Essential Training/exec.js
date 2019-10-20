/* eslint-disable no-undef */

// include child process module
const cp = require("child_process");

// console the output of ls command and catch the node.js error
cp.exec("ls", (err, data) => {
    if ( err ) {
        throw err;
    }
    console.log(data);
});

// to see the error returned from the command when we execute it, we can use the third argument like this:
cp.exec("lsd", (err, data, stderr) => {
    console.log(stderr);
});

// we can use exec command to execute any synchronous processes like this
cp.exec("node readStream", (err, data, stderr) => {
    console.log(data);
});