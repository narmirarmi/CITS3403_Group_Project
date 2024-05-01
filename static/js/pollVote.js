function onPollVote(vote, image) {
  //handle empty input
  if (vote != "yes" && vote != "no") {
    console.log("Error: Empty vote invalid.");
    return;
  }

  //POST vote request
  console.log(image);
  $.ajax({
    type: "POST",
    url: "/vote",
    data: { choice: vote, image: image },
    success: function (response) {
      if (response.success) {
        console.log("Vote successfully submitted");
      } else {
        console.log("Error:", response.error);
      }
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function updateResults(formId) {
  $.getJSON("/vote", function (data) {
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
