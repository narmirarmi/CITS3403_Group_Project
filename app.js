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

// This section recalculates and sizes the numbers of images and rows to fit window
$(document).ready(function () {
  adjustItemsPerRow();

  $(window).resize(function () {
    adjustItemsPerRow();
  });

  function adjustItemsPerRow() {
    var screenWidth = $(window).width();
    var itemsPerRow;

    if (screenWidth >= 992) {
      itemsPerRow = 3; // Large screens (lg)
    } else if (screenWidth >= 768) {
      itemsPerRow = 2; // Medium screens (md)
    } else {
      itemsPerRow = 1; // Small screens (sm) and below
    }

    var $row = $("#image-row");
    var $items = $row.children(".col-lg-4");

    $items.removeClass("col-lg-4 col-md-6 col-sm-12");
    $items.addClass("col-lg-" + 12 / itemsPerRow);
    $items.addClass("col-md-" + 12 / itemsPerRow);
    $items.addClass("col-sm-12");
  }
});
