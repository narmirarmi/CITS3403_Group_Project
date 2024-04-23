function onPollVote(vote){

    //handle empty input
    if( vote != "yes" || vote != "no" ){
        console.log("Error: Empty vote invalid.")
    }

    //POST vote request
    $.ajax({
          type: "POST",
          url: "/vote",
          data: vote,
          success: function (response) {
            if (response.success) {
              console.log("Vote successfully submitted")
            } else {
              console.log("Error:", response.error);
            }
          },
          error: function (xhr, status, error) {
            console.error("Error:", error);
          },
        });
}