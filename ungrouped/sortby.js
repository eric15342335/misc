/**
 * @param {Array} arr
 * @param {Function} fn
 * @return {Array}
 */
var sortBy = function(arr, fn) {
    //console.log("received: " + arr)
    let len = arr.length
    if (len <= 1) {
        return arr
    }
    let pivot = fn(arr[0])
    let smaller_than_pivot = -1
    let greater_than_pivot = len
    while (true) {
        do {
            smaller_than_pivot++;
        } while (smaller_than_pivot < len && fn(arr[smaller_than_pivot]) < pivot);
        
        do {
            greater_than_pivot--;
        } while (greater_than_pivot >= 0 && fn(arr[greater_than_pivot]) > pivot);        
        //console.log("leftright: " + smaller_than_pivot + " " + greater_than_pivot)
        if (smaller_than_pivot < greater_than_pivot) {
            let temp = arr[smaller_than_pivot]
            arr[smaller_than_pivot] = arr[greater_than_pivot]
            arr[greater_than_pivot] = temp
            //console.log("arr: " + arr)
        }
        else {
            break
        }
    }
    let new_arr = sortBy(arr.slice(0, greater_than_pivot+1), fn)
    new_arr = new_arr.concat(sortBy(arr.slice(greater_than_pivot+1), fn))
    //console.log("new_arr: " + new_arr)
    return new_arr
};

toBeSorted = [{"x":2},{"x":1}]
sortingFunction = function (element) {
    return element.x
}
console.log(sortBy(toBeSorted, sortingFunction))