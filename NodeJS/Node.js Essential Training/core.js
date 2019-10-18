/* eslint-disable no-undef */
// path module is a core module available by default with node.js
const path = require("path");
// load another core module: utility
//const util = require("util");
// we can destructure the functions out of their modules
const { log } = require("util");
//load v8 module
//const v8 = require("v8");
const { getHeapStatistics } = require("v8");

// example of core path module to create a directory uploads path
const dirUploads = path.join(__dirname, "www", "files", "uploads");
console.log(dirUploads);

// use log() function of util module which is another powerful logging function
// util.log( path.basename(__filename) );
// util.log(" ^ The name of the current file");
log( path.basename(__filename) );
log(" ^ The name of the current file");

// take a look at memory usage, etc using v8 module
//util.log(v8.getHeapStatistics());
log( getHeapStatistics() )
