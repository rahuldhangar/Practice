/**
 * Move, rename remove files
 * rename method has both synchronous & asynchronous versions: renameSync & rename
 */
const fs = require("fs");

// rename a file synchronously
fs.renameSync("./assets/colors.json", "./assets/colorData.json");

// move file from /assets to /storage-files using rename() (asynchronously)
fs.rename("./assets/notes.md", "./storage-files/notes.md", err => {
    if( err ) {
        throw err;
    }
});

// delete alex.jpg file after 4 seconds of delay...
setTimeout(() => {
    fs.unlinkSync("./assets/alex.jpg");
}, 4000);