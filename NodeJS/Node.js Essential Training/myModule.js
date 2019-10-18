/* eslint-disable no-undef */

/**
 * In Node.js every JS file is its own module. We've seen loading modules with require function.
 * The require() function is a part of Node.js module pattern but only represents half of the pattern;
 * the half that loads the module. The other half of the pattern is module.exports
 * where the mechanism that we use to export data and functinality from a module.
 * Below here, we are exporting the name so that it can be used in another file named app.js
 */
module.exports = "Rahul";