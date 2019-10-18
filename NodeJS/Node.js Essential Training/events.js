/* eslint-disable no-undef */

/**
 * Events Emitter is Node.js's implementation of Pub/Sub design pattern and
 * it gives a mechanism for emitting custom events and wiring up listeners and heandlers for those events
 */

// get events module (no need to put the file path because its a core module)
const events = require("events");

// create instance of the eventsEmitter
const emitter = new events.EventEmitter();

// emitter.on() function to handle these custom events
emitter.on("customEvent", (message, user) => {
    console.log(`${user}: ${message}`);
});

// // Raise two custom events... by emitter.emit() function
// emitter.emit("customEvent", "Hello World", "Computer");
// emitter.emit("customEvent", "That's pretty cool huh?", "Rahul");


// EventEmitter's emited events are asynchronous; they are raised when they happen. example: 
process.stdin.on("data", data => {
    const input = data.toString().trim();
    if( input == "exit") {
        emitter.emit("customEvent", "Goodbye!", "process");
        process.exit();
    }
    emitter.emit("customEvent", input, "terminal");
});