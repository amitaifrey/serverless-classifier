// ImageLoaded updates the image on the page, and posts it to the classifier.
// Once a result is returned from the classifier, it presents it to the user.
function imageLoaded(e) {
    // Load the image on the page and change the text
    list_title = document.getElementById("list_title");
    list_title.innerHTML = "Classifying...";
                    for (let i = 0; i < 5; i++) {
                    document.getElementById("pred"+i).innerHTML = "";
                }
    preview = document.getElementById("preview");
    preview.setAttribute('src', e.target.result);

    // Remove the prefix to only keep data, and change to base64 url safe encoding
    var data = e.target.result.replace("data:image/jpeg;base64,", '').replaceAll("+", "-").replaceAll("/", "_");

    // Start timing the classification
    var start = Date.now();

    // Calls the classifier asynchronously
    $.ajax({
            type: "POST",
            url: 'https://89b097d7.eu-gb.apigw.appdomain.cloud/classify/classify',
            crossDomain: true,
            headers: {
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'authorization,x-ibmcloud-sdk-analytics,x-watson-learning-opt-out,user-agent'
            },
            data: {
                "image": data
            },
            success: function(data) {
                // Present the overall time the classification took, how much it took in the python script
                // and the predicitions themselves on the page
                var end = Date.now();
                var elapsed = end - start;
                var seconds = parseInt(Math.abs(elapsed) / (1000) % 60);
                var ms = elapsed - seconds*1000;
                list_title.innerHTML = "Classifying took " + seconds + "." + ms + "s overall, " + data["duration"] + "s in the python script.<br/><br/>Predictions:";
                result = data["result"]
                for (let i = 0; i < result.length; i++) {
                    document.getElementById("pred"+i).innerHTML = Object.keys(result[i]) + ": " + Object.values(result[i]);
                }
            }
        })
        .fail(function(xhr, textStatus, errorThrown) {
            // Present the error on the page
            list_title.innerHTML = "Error:" + xhr.responseText;
        });
}

// Classify loads the image and sets a callback to run once it's loaded
function classify() {
    var reader = new FileReader();
    customFile = document.getElementById("customFile");

    if (customFile.files && customFile.files[0]) {
        reader.onload = imageLoaded;

        reader.readAsDataURL(customFile.files[0]);
    }
}