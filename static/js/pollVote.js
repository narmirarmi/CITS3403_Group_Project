function onPollVote(vote, image) {
  //handle empty input
  if (vote != "like" && vote != "dislike") {
    console.log("Error: Empty vote invalid.");
    return;
  }

  //POST vote request
  $.ajax({
    type: "POST",
    url: "/vote",
    data: { choice: vote, image: image }, // Adjusted data parameters
    success: function (response) {
      /* Updates the UI with the new votes */
      image = image.split("/").pop();
      image = image.split(".")[0];
      updateResults(response, image);
      console.log("Vote successfully submitted");
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function updateResults(data, image) {
  console.log(image);
  $("#yes-votes-" + image).text(data.likes_count);
  $("#no-votes-" + image).text(data.dislikes_count);
  // Remove previous classes from thumbs-up and thumbs-down icons
  $("#" + image + " .thumbs-up, #" + image + " .thumbs-down").removeClass(
    "bi-hand-thumbs-up-fill bi-hand-thumbs-down-fill"
  );

  // Add appropriate class based on vote type
  if (data.vote_type === "like") {
    $("#" + image + " .bi-hand-thumbs-up").addClass("bi-hand-thumbs-up-fill");
  } else if (data.vote_type === "dislike") {
    $("#" + image + " .bi-hand-thumbs-down").addClass(
      "bi-hand-thumbs-down-fill"
    );
  }
}
