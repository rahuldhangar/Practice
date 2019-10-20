/* eslint-disable no-undef */

// process.stdout is a writable whcih means it has a write() method and we can use the write method to write data to a writable stream like this 
process.stdout.write("hello");
process.stdout.write(" world\n");

// now we can use the same interface to write a file. lets include fs module first
const fs = require("fs");

// create a writable file stram using fs.createWriteStream method
const writeStream = fs.createWriteStream("./assets/myFile.txt", "UTF-8");

writeStream.write("hello");
writeStream.write(" world\n");

// readable streams are made to work with writable streams.
process.stdin.on("data", data => {
    writeStream.write(data);
});

// now lets exemplify this by creating a readStream.
const readStream = fs.createReadStream("./assets/lorem-ipsum.md", "UTF-8");

// readable streams are made to work with writable streams, example:
readStream.on("data", data => {
    writeStream.write(data);
});

// another example:
process.stdin.pipe(writeStream);