$(document).ready(function() {

    let url = window.location.href.slice(0,-5);

    if(localStorage.getItem("should_i_buy_it.current_session") != null){

        var formData = {
            session_token: localStorage.getItem("should_i_buy_it.current_session"),
        };

        $.ajax({
            type: 'POST',
            url: url+'/auth',
            data: formData,

            success: function(response) {
                // Show user page if successful
                console.log(response.message);
                window.location.replace(url + 'user?username=' + response.user);
            },
            error: function(xhr, status, error) {
                // Redirect to login page
                console.log(response.message, response.error);
                window.location.replace(url + 'login');
                localStorage.removeItem("should_i_buy_it.current_session")
            }

        });
    } else {
        console.log('No token found')
        window.location.replace(url + 'login');
    }

});