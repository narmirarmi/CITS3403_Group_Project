$(document).ready(function() {
    $('#loginForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = {
            username: $('#loginName').val(),
            password: $('#loginPassword').val(),
        };

        if (!formData.username || !formData.password) {
            alert('Please enter a username/email and password');
            return; // Stop the function if validation fails
        }

        // Send the data using AJAX
        $.ajax({
            type: 'POST',
            url: 'http://localhost:5000/loginuser',
            data: formData,
            success: function(response) {
                // Handle success
                console.log('Login successful', response);
                alert('Login successful', response);
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.log('Login error', error);
                alert('Login failed: ' + error);
            }
        });
    });
});
