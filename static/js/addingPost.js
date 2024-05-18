$(document).ready(function () {
  $("#addListingForm").on("submit", function (event) {
    event.preventDefault();

    var formData = new FormData(this);

    $.ajax({
      type: "POST",
      url: "/post",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        $("#addListingModal").modal("hide");
        location.reload();
      },
      error: function (response) {
        alert("Failed to add listing");
      },
    });
  });
});
