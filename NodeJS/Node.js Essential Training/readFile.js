/**
 * We can also use fs module to read content of a file.
 */
const fs = require("fs");

// // This function below will read file synchronously
// const text = fs.readFileSync("./assets/Readme.md", "UTF-8");

// // This function below will read file asynchronously
// fs.readFile("./assets/Readme.md", "UTF-8", (err, text) => {
//     console.log("file contents read");
//     console.log(text);
// });

// This function below will read a binary file asynchronously in the buffer
fs.readFile("./assets/alex.jpg", (err, img) => {
    if( err ) {
        console.log(`An error has occured: ${err.message}`);
    }
    console.log("binary file contents read");
    console.log(img);
});
