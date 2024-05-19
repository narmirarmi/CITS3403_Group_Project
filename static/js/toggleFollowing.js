function toggleFollow(userid){



    var formData = {
      userid: userid,
    };

    console.log("Making request to follow id " + formData.userid);

    $.ajax({
        type: 'POST',
        url: '../user/follow',
        data: formData,
        success: function(response) {
            console.log(response)
            if(response.status=="followed"){
                $("#follow-button").text("Following")
            } else {
                $("#follow-button").text("Follow")
            }
            $("#followers-count").text(response.follower_count);
            $("#following-count").text(response.following_count);
        }
    });
}