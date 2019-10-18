const waitTime = 5000;
const waitInterval = 500;
let currentTime = 0;

//
const incTime = () => {
    currentTime += waitInterval;
    // create a var to calculate percentage for progress
    const p = Math.floor((currentTime / waitTime) * 100);
    // clear the last line...
    process.stdout.clearLine();
    // move cursor back to start position...
    process.stdout.cursorTo(0);
    // write our message using process
    process.stdout.write(`waiting ... ${p}% `);
};

console.log(`setting a ${waitTime / 1000} second delay`);

// function to clear the interval and display finished message
const timerFinished = () => {
    clearInterval(interval);
    // clear the last line and move cursor back to start position...
    process.stdout.clearLine();
    process.stdout.cursorTo(0);
    console.log("done");
};

//setInterval function actually returns the interval itself so that we can clear it later
const interval = setInterval(incTime, waitInterval);
setTimeout(timerFinished, waitTime);
