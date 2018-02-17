// function getUpdatedComment(post) {
//     var list = $("#" + "post_" + post.id).find(".dropdown-menu");
//     var max_entry = list.data("max-entry");
//     $.get("/get-comment-changes/"+ post.id + "/" + max_entry).done(function(data) {
//         list.data('max-entry', data['max-entry']);
//         for (var i = 0; i < data.comments.length; i++) {
//             var comment = data.comments[i];
//             if (comment.deleted) {
//                 $("#comment_" + comment.id).remove();
//             } else {
//                 var new_comment = $(comment.html);
//                 new_comment.data("comment-id", comment.id);
//                 list.prepend(new_comment);
//             }
//         }
//     });
// }

function addComment(e) {
    console.log(e.data.id);
    var contentField = $("#" + "post_" + e.data.id).find("#new-comment");
    console.log(contentField.val());
    $.post("/add-comment/" + e.data.id, {comment: contentField.val()})
      .done(function(data) {
        getUpdatedPost();
        $("#new-comment").val("").focus()
      });
}

function addCommentToPost(post) {
    console.log(post.id)
    var postDiv = $("#" + "post_" + post.id);
    var list = postDiv.find("#comment-list");
    $.get("/get-comments/" + post.id).done(function(data) {
        list.data('max-time', data['max-time']);
        list.html('');
        for (var i = 0; i < data.comments.length; i++) {
            comment = data.comments[i];
            var new_comment = $(comment.html);
            new_comment.data("comment-id", comment.id);
            list.prepend(new_comment);
        }
    });
}

function populateList() {
    $.get("/get-follower-stream-posts").done(function(data) {
        var list = $("#post-list");
        list.data('max-time', data['max-time']);
        // console.log(data['max-time']);
        list.html('')
        for (var i = 0; i < data.posts.length; i++) {
            post = data.posts[i];
            var new_post = $(post.html);
            new_post.data("post-id", post.id);
            new_post.find("#comment-btn").click(post, addComment);
            list.prepend(new_post);
            addCommentToPost(post);
        }
    });
}

function addPost() {
    var contentField = $("#new_post");
    console.log(contentField.val());
    $.post("/add-post", {post: contentField.val()}).done(function(data) {
            getUpdatedPost();
            contentField.val("").focus();
    });
}

function getUpdatedPost() {
    var list = $("#post-list")
    var max_time = list.data("max-time")
    console.log(max_time);
    $.get("/get-follower-stream-changes/"+max_time)
      .done(function(data){
        list.data('max-time', data['max-time']);
        // console.log(data['max-time']);
        for (var i = 0; i < data.posts.length; i++) {
            var post = data.posts[i];
            if (post.deleted) {
                $("#post_" + post.id).remove();
            } else {
                var new_post = $(post.html);
                new_post.data("post-id", post.id);
                list.prepend(new_post);
                addCommentToPost(post);
            }
        }
    });
}

$(document).ready(function () {
    // TODO: add handler for the post button
    $("#post-btn").click(addPost);
    populateList();

    window.setInterval(getUpdatedPost, 5000);

    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
