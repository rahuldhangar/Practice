/* eslint-disable no-undef */
// consume the exported value from myModule...
// under require function, we have to specify the file path to the module
const { inc, dec, getCount } = require("./myModule");

// Use inc(), dec() function to change the counter value without the need of prefixing counter (as done in last commit)
inc();
inc();
inc();
dec();

// log the value of counter in console
console.log(getCount());