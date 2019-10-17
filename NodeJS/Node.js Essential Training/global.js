//display full path of file and the directory containing it
console.log(__dirname);
console.log(__filename);

//include the path modules that ships with Node.js using require function
const PATH = require("path");
console.log(`\nThe filename is: ${PATH.basename(__filename)}`);

//console object is a global object and accessible from everywhere
global.console.log(`\nThe filename is: ${PATH.basename(__filename)}`);