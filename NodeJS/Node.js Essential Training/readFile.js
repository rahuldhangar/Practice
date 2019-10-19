/**
 * We can also use fs module to read content of a file.
 */
const fs = require("fs");

// // This function below will read file synchronously
// const text = fs.readFileSync("./assets/Readme.md", "UTF-8");

// This function below will read file asynchronously
fs.readFile("./assets/Readme.md", "UTF-8", (err, text) => {
    console.log("file contents read");
    console.log(text);
});
