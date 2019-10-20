/* eslint-disable no-undef */
const fs = require("fs");

const readStream = fs.createReadStream("./assets/lorem-ipsum.md", "UTF-8");

let fileTxt = "";

// readStream can be used to read the data bit by bit or chunk by chunk
// replacing process.stdin.on with our readStream variable...
// so that just like process.stdin is used to read data events, readStream can be used to read a text file chunk by chunk
readStream.on("data", data => {
    console.log(`I read ${data.length -1} characters of text`);
    // lets collect all the data chunks in a variable fileTxt
    fileTxt += data;
});

//we can use it to raise events... for instance, listen for data events, attach a handler like this
readStream.once("data", data => {
    console.log(data);
});

// we can add a lot of events when the data is being read. We can also add an end event:
readStream.on("end", () => {
    console.log("finished reading file");
    console.log(`In total I read ${fileTxt.length - 1} characters of text`)
});