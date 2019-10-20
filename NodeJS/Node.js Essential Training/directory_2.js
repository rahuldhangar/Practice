/* eslint-disable no-undef */
const fs = require("fs");

// rename /storage-files directory to /storage
fs.renameSync("./storage-files", "./storage");

fs.readdirSync("./storage").forEach(fileName => {
    fs.unlinkSync(`./storage/${fileName}`)
});

// remove directory asynchronously (ensure that this directory is empty before removing)
fs.rmdir("./storage", err => {
    if( err ) {
        throw err;
    }
    console.log("./storage directory removed");
});