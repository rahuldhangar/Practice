const waitTime = 3000;
const waitInterval = 500;
let currentTime = 0;

//
const incTime = () => {
    currentTime += waitInterval;
    console.log(`waiting ${currentTime / 1000} seconds`);
};

console.log(`setting a ${waitTime / 1000} second delay`);

const timerFinished = () => {
    clearInterval(interval);
};

//setInterval function actually returns the interval itself so that we can clear it later
const interval = setInterval(incTime, waitInterval);
setTimeout(timerFinished, waitTime);
