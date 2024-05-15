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
}
