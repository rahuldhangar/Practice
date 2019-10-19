/* eslint-disable no-undef */

//load the fs module using require() function
const fs = require("fs");

// console.log("started reading files");
// //function to read all files in a directory synchronously (blocking code)
// const files = fs.readdirSync("./assets");
// console.log("complete");

// console.log(files);

/**
 * Above code from line #6 to #11 an example of reading files synchronously which blocks the code.
 * Below mentioned code reads the files asynchronously.
*/

// using readdir() function in place of readdirSync() for asynchronously reading the directory content
fs.readdir("./assets", (err, files) => {
    if( err ) {
        throw err;
    }
    console.log("complete");
    console.log(files);
});

console.log("started reading files");

/**
 * Notice that the line 27 still gets displayed on console first because message on line 23
 * only gets displayed once the files in the directory are read. So this is being done asynchronously
 */