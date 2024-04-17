$(document).ready(function () {
  $("#poll-form").submit(function (event) {
    event.preventDefault(); // Prevent default form submission
    var formData = $(this).serialize(); // Serialize form data
    $.ajax({
      type: "POST",
      url: "/vote",
      data: formData,
      success: function (response) {
        if (response.success) {
          updateResults(); // Update poll results on successful vote
        } else {
          console.log("Error:", response.error);
        }
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });

  function updateResults() {
    $.getJSON("/results", function (data) {
      $("#yes-count").text(data.yes); // Update yes count
      $("#no-count").text(data.no); // Update no count
    });
  }

  // Initial update of results when the page loads
  updateResults();
});
