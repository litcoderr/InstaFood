var iter_interval = 3000;
var iter_threshold = 10;
var iter_idx = 1;

var iterator = setInterval(check_task, iter_interval);

var result = [
    {
        "is_done" : false,
        "have_fetched" : false,
        "html" : ""
    }
];

function fetch(){
    // Do fetching here (ajax code)
    //ajax to get response
    var request = new XMLHttpRequest();
    request.open('GET', 'http://127.0.0.1:5000/api/fetch/?request_id='+request_id, true);
    request.onload = function(){
        // play around with data
        var data = JSON.parse(request.responseText);
        var valid = data[0]["valid"];

        if(valid){ // valid data has been fetched
            result[0]["have_fetched"] = true;
            result[0]["is_done"] = true;
            // ** update result json with data json **
            result[0]["html"] = data[0]["html"]
        }
    };
    request.send();

    if(iter_idx==iter_threshold){ // after 30 seconds of try or have fetched --> finish
        result[0]["is_done"] = true; // check done to true
    }
    return result;
}

function check_task(){
    // checking and fetching main stream
    var result  = fetch();
    iter_idx += 1; // count iterations
    if(result[0]["is_done"]){ // if result says done -> stop
        clearInterval(iterator);
        if(result[0]["have_fetched"]){ // fetched successfully -> render output
            console.log(result);
            document.getElementById("response").innerHTML = result[0]["html"]
        }else{ // wasn't successfull -> render error message
            console.log("wasn't successfull");
        }
    }
}
