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
      /* Updates the UI with the new votes */
      let imageName = image.split("/").pop();
      updateResults(response, imageName);
      console.log("Vote successfully submitted");
    },
    error: function (xhr, status, error) {
      console.error("Error:", error);
    },
  });
}

function updateResults(data, image) {
  console.log("IMMMMMAAAGGEEE");
  console.log(image);
  $("#yes-votes-" + image).text(data[image].yes);
  $("#no-votes-" + image).text(data[image].no);
}
