/* eslint-disable no-undef */
// consume the exported value from myModule...
// under require function, we have to specify the file path to the module
const counter = require("./myModule");

// use inc() function to increment the counter value
counter.inc();
counter.inc();
counter.inc();

// log the value of counter in console
console.log(counter.getCount());