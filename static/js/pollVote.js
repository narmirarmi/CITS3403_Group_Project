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
  // Remove previous fill classes from thumbs-up and thumbs-down icons
  $("." + image + "1").removeClass("bi-hand-thumbs-up-fill");
  $("." + image + "2").removeClass("bi-hand-thumbs-down-fill");

  console.log(data.vote_type);
  // Add appropriate fill class based on vote type
  if (data.vote_type === "like") {
    console.log("Tried fill");
    $("." + image + "1").removeClass("bi-hand-thumbs-up");
    $("." + image + "1").addClass("bi-hand-thumbs-up-fill");
    $("." + image + "2").addClass("bi-hand-thumbs-down");
  } else if (data.vote_type === "dislike") {
    $("." + image + "2").removeClass("bi-hand-thumbs-down");
    $("." + image + "2").addClass("bi-hand-thumbs-down-fill");
    $("." + image + "1").addClass("bi-hand-thumbs-up");
  }
}
