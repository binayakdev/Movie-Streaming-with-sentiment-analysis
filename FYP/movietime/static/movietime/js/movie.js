movie = document.getElementsByClassName('clickable'); // Getting the movie card element in the page.

// Adding the clickable even listerner to every movie card element in the web page.
for (var i = 0; i < movie.length; i++) {
    (function (index) {
        movie[index].addEventListener('click', function () {
            video = document.getElementsByClassName('overview')[index];
            video.style.display = "block";
            document.getElementById('overlay').style.display = "block";
            youtube_token = document.getElementsByClassName('youtube-token')[index].innerHTML;
            document.getElementsByTagName('iframe')[index].src = 'https://www.youtube.com/embed/' + youtube_token + '?&autoplay=1&loop=1&rel=0&showinfo=0&color=white&iv_load_policy=3&controls=0&frameborder=0&mute=1&playlist=' + youtube_token;
        }, false);
    })(i)
}

// This shows the select genre form
$('#genre-menu').click(function () {
    $('#genre-filter').show();
});

// This hides the select  genre form
$('#exit-filter').click(function () {
    $('#genre-filter').hide();
})

var button = document.getElementsByClassName("menu"); // selecing the 'cross' button of the movie card element

// Adding the clickable event listender to every 'cross' button
// On clicking the  button the movie card element is hidden
for (var i = 0; i < button.length; i++) {
    (function (index) {
        button[index].addEventListener('click', function () {
            video = document.getElementsByClassName('overview')[index];
            video.style.display = "none";
            document.getElementById('overlay').style.display = "none";
            document.getElementsByTagName('iframe')[index].src = "";
        }, false);
    })(i)
};

var bookmark_icon = document.getElementsByClassName("fav-add-icon");
var bookmarked_icon = document.getElementsByClassName("bookmarked_icon")


/**
 * This loop adds clickable event listener to every 'bookmark' icon
 * The bookmark icon is toggled on clicking the icon.
 */
for (var i = 0; i < bookmark_icon.length; i++) {
    (function (index) {
        bookmark_icon[index].addEventListener('click', function () {
            if (bookmark_icon[index].classList.contains("far")) {
                bookmark_icon[index].classList.remove("far");
                bookmark_icon[index].classList.add("fas");
                bookmark_icon[index].setAttribute("title", "Remove from Favourites");
                if (bookmarked_icon != null) {
                    bookmarked_icon[index].classList.add("fa-bookmark");
                }
            }
            else {
                bookmark_icon[index].classList.add("far");
                bookmark_icon[index].classList.remove("fas");
                bookmark_icon[index].setAttribute("title", "Add to Favourites");
                if (bookmarked_icon != null) {
                    bookmarked_icon[index].classList.remove("fa-bookmark");
                }
                else {
                    console.log("This works")
                    document.getElementsByClassName("movie-container").style.display = "none";
                    document.getElementsByClassName("movie-container").style.display = "none";
                }
            }
        }, false);
    })(i)
}

fav_add = document.getElementsByClassName("fav-add"); // This is the bookmark icon element

/**
 * This is jQuery portion of the JavaScript 
 * When the user clicks the bookmark icon an AJAX request is sent to the backend
 * On sucess an message is displayed on the webpage.
 */
$('.fav-add-icon').click(function () {
    $.ajax({
        url: $(this).attr("data-href"),
        dataType: 'json',
        success: function (data) {
            if (data.success) {
                $('#fav-notify-msg').html(data.message);
                $('#fav-notify').show();
                setTimeout(function () { $("#fav-notify").fadeOut(); }, 3000);
            }
        }
    });
});