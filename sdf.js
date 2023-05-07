$(document).ready( 
    function(){
        // Functionality to upload sdf
        $("#upload").click(function(){

            //Stay on the page
            $("form").submit(function(event) {
                event.preventDefault();
            })

            //Get molecule name and file
            var name = $('#mol-name').val().trim();
            var sdf= $('#sdf-file')[0].files[0];
            // Create a form with molecule name and file attached
            var formData = new FormData();
            formData.append('mol-name', name);
            formData.append('sdf-file', sdf);
            // POST request to save an uploaded sdf file
            $.ajax({
                    url: 'sdfUpload.html',
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function(response) {
                        alert("File uploaded!")
                    },
                    error: function(xhr, textStatus, errorThrown) {
                        alert("Error. File not uploaded.");
                    },
                });
                // clear form
                $("#uploadForm").trigger("reset")  
            }
        )
    }
)