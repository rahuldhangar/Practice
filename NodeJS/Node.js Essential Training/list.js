/* eslint-disable no-undef */

//load the fs module using require() function
const fs = require("fs");

console.log("started reading files");
//function to read all files in a directory synchronously (blocking code)
const files = fs.readdirSync("./assets");
console.log("complete");

console.log(files);

/**
 * Notice that the line #8 is blocking the code because the files are read synchronously this way.
 * In the next commit, we will see how can we read files asynchronously.
*/