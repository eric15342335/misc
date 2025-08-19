/**
 * @param {integer} init
 * @return { increment: Function, decrement: Function, reset: Function }
 */
var createCounter = function(init) {
    let counter = init;
    function increment() {
        return ++counter;
    }
    function reset() {
        counter = init;
        return counter;
    }
    function decrement() {
        return --counter;
    }
    return {increment, reset, decrement};
};


const counter = createCounter(5)
console.log(counter.increment()); // 6
console.log(counter.reset()); // 5
console.log(counter.decrement()); // 4
