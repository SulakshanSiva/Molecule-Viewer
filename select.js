// start jquery
$(document).ready( 
    //function to call when server is created
    function(){
        // GET request to get molecule data
        $.ajax({
            url: 'getMol',
            type: 'GET',
            dataType: 'json',
            success: function(response) {
                var table = response
                // If there are no molecules in the table
                if(table.length === 0){
                    // display statement to user
                    str = "<h1>No Molecules exist in the table.</h1>"
                    str += "<h3>Populate the table</h3>"
                    $('#table').append(str);
                } else {
                    // create table
                    str = ""
                    for(let i = 0; i < table.length; i++){
                        var molName = table[i].name
                        var atomNum = table[i].atomNum
                        var bondNum = table[i].bondNum

                        str += `<div class="tableRow" id="row">
                                    <div id="${molName}">
                                        <p>${molName} | </p>
                                        <p>Atoms: ${atomNum} | </p>
                                        <p>Bonds: ${bondNum}</p>
                                    </div>
                                </div>`
                    }
                    //display table in div
                    $('#table').append(str);
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                alert("Error. Unable to load table.");
            },
        });

        // Check if table rows were clicked
        $(document).on('click', '.tableRow', function() {
            var molName = $(this).find('div').attr('id');
            // POST request to move to new html page
            $.ajax({
                url: '/display', 
                type: 'POST',
                data: {
                    name: molName
                }, success: function (response) {
                    // redirect to new html page
                    window.location.href = '/display.html'; 
                  },
                  error: function (xhr, textStatus, errorThrown) {
                    console.log("Error.");
                  }
            });
        })
    }
)
