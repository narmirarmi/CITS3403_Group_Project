$(document).ready(function () {
  // login handling
  $("#loginForm").submit(function (event) {
    event.preventDefault(); // Prevent the default form submission

    var formData = {
      email: $("#loginName").val(),
      password: $("#loginPassword").val(),
    };

    if (!formData.email || !formData.password) {
      alert("Please enter an email and password");
      return; // Stop the function if validation fails
    }

    // Send the data using AJAX
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/auth/login",
      data: formData,
      success: function (response) {
        // Handle success
        console.log("Login successful", response.message);
        localStorage.setItem(
          "should_i_buy_it.current_session",
          response.session_token
        );
        console.log("Successfully wrote session token");
        window.location.replace("../");
      },
      error: function (xhr, status, error) {
        // Handle errors
        console.log("Login error", error);
        alert("Login failed: " + error);
      },
    });
  });

  //registration handling
  $("#registrationForm").submit(function (event) {
    event.preventDefault(); // Prevent the default form submission

    var formData = {
      name: $("#registerName").val(),
      username: $("#registerUsername").val(),
      email: $("#registerEmail").val(),
      password: $("#registerPassword").val(),
      repeatPassword: $("#registerRepeatPassword").val(),
      termsAgreed: $("#registerCheck").is(":checked"),
    };

    if (!formData.email || !formData.password) {
      alert("Email and password are required!");
      return; // Stop the function if validation fails
    }

    // Send the data using AJAX
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/auth/register",
      data: formData,
      success: function (response) {
        // Handle success
        console.log("Registration successful", response);
        alert("Registration successful!");
      },
      error: function (xhr, status, error) {
        // Handle errors
        console.log("Error in registration", error);
        alert("Registration failed: " + error);
      },
    });
  });
});
