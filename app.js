/*
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
*/

$(document).ready(function () {
  $(".poll-form").submit(function (event) {
    event.preventDefault(); // Prevent default form submission
    var formData = $(this).serialize(); // Serialize form data
    var formId = $(this).attr("id"); // Get the ID of the submitted form
    $.ajax({
      type: "POST",
      url: "/vote",
      data: formData,
      success: function (response) {
        if (response.success) {
          updateResults(formId); // Update poll results for the specific element on successful vote
        } else {
          console.log("Error:", response.error);
        }
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
      },
    });
  });

  function updateResults(formId) {
    $.getJSON("/results", function (data) {
      // Update poll results for the specific element
      $("#" + formId)
        .siblings(".poll-results")
        .find(".yes-count")
        .text(data.yes);
      $("#" + formId)
        .siblings(".poll-results")
        .find(".no-count")
        .text(data.no);
    });
  }

  // Initial update of results when the page loads
  updateResults();
});
