// start jquery
$(document).ready( 
    //function to call when server is created
    function(){
        //functionality for add Element button on click
        $("#addElementBtn").click(
            function() 
            {
                // Stay on page
                $("form").submit(function(event) {
                    event.preventDefault();
                })
                
                // Check if input is valid
                if($("#elementNum").val() >= 0 
                    && $("#radius").val() >= 0 
                    && ($("#elementCode").val()).length <= 3 
                    && ($("#elementName").val()).length <= 32
                    )
                    {
                        //POST request to store element
                        $.post("/elementHandler",
                        //pass a dictionary of element table values
                        {
                            elementNum: $("#elementNum").val(),
                            elementCode: $("#elementCode").val(),
                            elementName: $("#elementName").val(),
                            colOne: $("#colOne").val(),
                            colTwo: $("#colTwo").val(),
                            colThree: $("#colThree").val(),
                            radius: $("#radius").val()
                        }
                    )   
                    alert("Added elements.")
                } else {
                    alert("Error. Please enter valid inputs to add an element.")
                }
                // clear form
                $("#elementForm").trigger("reset")
            }
        );

        // Functionality for delete element button
        $("#deleteElementBtn").click(
            function() 
            {
                // Stay on page
                $("form").submit(function(event) {
                    event.preventDefault();
                })
                
                // DELETE request to delete element
                $.ajax({
                    url: "/rmvElementHandler",
                    type: 'DELETE',
                    data: {
                        elementDel: $("#rmvElement").val()
                    },success: function(data, textStatus, xhr) {
                        alert("Element deleted successfully.");
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        alert("Element not found.");
                    },    
                })
                // clear form
                $("#rmvElementForm").trigger("reset")            
            }
        );
    }

);


