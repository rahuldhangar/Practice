/* eslint-disable no-undef */
// include the fs by requiring it...
const fs = require("fs");

// No need to use filesystem (fs) to read json document. It can be done by simply requiring it like this:
const colorData = require("./assets/colors.json");

// this will read colorList property from colors.json file and append the color & hex codes to a file under /storage-files/colors.md
colorData.colorList.forEach( c => {
    fs.appendFile("./storage-files/colors.md", `${c.color}: ${c.hex} \n`, err => {
        if ( err ) {
            throw err;
        }
    });
});