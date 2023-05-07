// start jquery
$(document).ready( 
    //function to call when server is created
    function(){
        
    // GET request to display molecule on screen
    $.ajax({
        url: "/createMol",
        type: "GET",
        dataType: "text",
        success: function(data, status, xhr){
            //clear div
            $("#display-container").empty()
            //resize svg
            data = data.replace('width="1000"', 'width="500"');
            data = data.replace('height="1000"', 'height="400"');
            data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
            //add svg to div
            $("#display-container").append(data)
        }
    });

    //if rotate x was clicked
    $("#rotateX").click(function(){
        //call rotate method
        var dimension = "x";
        rotate(dimension)
        // GET request to display molecule on screen
        {
            $.ajax({
                url: "/createMol",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //clear div
                    $("#display-container").empty()
                    //resize svg
                    data = data.replace('width="1000"', 'width="500"');
                    data = data.replace('height="1000"', 'height="400"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add svg to div
                    $("#display-container").append(data)
                }
            });
        }
    }),

    //if rotate y was clicked
    $("#rotateY").click(function(){
        //call rotate method
        var dimension = "y";
        rotate(dimension)
        // GET request to display molecule on screen
        {
            $.ajax({
                url: "/createMol",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //clear div
                    $("#display-container").empty()
                    //resize svg
                    data = data.replace('width="1000"', 'width="500"');
                    data = data.replace('height="1000"', 'height="400"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add svg to div
                    $("#display-container").append(data)
                }
            });
        }
    }),

    //if rotate z was clicked
    $("#rotateZ").click(function(){
        //call rotate method
        var dimension = "z";
        rotate(dimension)
        // GET request to display molecule on screen
        {
            $.ajax({
                url: "/createMol",
                type: "GET",
                dataType: "text",
                success: function(data, status, xhr){
                    //clear div
                    $("#display-container").empty()
                    //resize svg
                    data = data.replace('width="1000"', 'width="500"');
                    data = data.replace('height="1000"', 'height="400"');
                    data = data.replace('<svg ', '<svg version="1.1" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid meet" ');
                    //add svg to div
                    $("#display-container").append(data)
                }
            });
        }
    })

    }
)

// POST request to send rotate dimension data
function rotate(dimension){
    $.ajax({
        url: '/rotate', 
        type: 'POST',
        data: {'dimension': dimension},
        success: function (response) {
            console.log("Rotated.");
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("Rotation Error.");
        }
    });
}

