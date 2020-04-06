movie = document.getElementsByClassName('clickable');

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

$('#genre-menu').click(function () {
    $('#genre-filter').show();
});

$('#exit-filter').click(function () {
    $('#genre-filter').hide();
})

var button = document.getElementsByClassName("menu");

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

fav_add = document.getElementsByClassName("fav-add");

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