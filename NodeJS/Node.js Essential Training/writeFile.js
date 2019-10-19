/**
 * fs module can also be used to create new files and write data into the file
 */

const fs = require("fs");

// create some markdown text for writing into the file
const md = `
 #This is a new file
 
 We can write text to a file with fs.writeFile
 
 * fs.readdir
 * fs.readFile
 * fs.writeFile
 
 `;

fs.writeFile("./assets/notes.md", md.trim(), err => {
    if ( err ) {
        throw err;
    }
    console.log("file saved");
});