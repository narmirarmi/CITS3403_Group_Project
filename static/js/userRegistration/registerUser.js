$(document).ready(function() {
    $('#registrationForm').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = {
            name: $('#registerName').val(),
            username: $('#registerUsername').val(),
            email: $('#registerEmail').val(),
            password: $('#registerPassword').val(),
            repeatPassword: $('#registerRepeatPassword').val(),
            termsAgreed: $('#registerCheck').is(':checked')
        };

        if (!formData.email || !formData.password) {
            alert('Email and password are required!');
            return; // Stop the function if validation fails
        }

        // Send the data using AJAX
        $.ajax({
            type: 'POST',
            url: '/register',
            data: formData,
            success: function(response) {
                // Handle success
                console.log('Registration successful', response);
                alert('Registration successful!');
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.log('Error in registration', error);
                alert('Registration failed: ' + error);
            }
        });
    });
});
