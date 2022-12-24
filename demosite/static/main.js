//NavBar
function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:none;");
    navigation.classList.remove("hide");
}

function showIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:block;");
    navigation.classList.add("hide");
}

//Comment
function showComment(){
    var commentArea = document.getElementById("comment-area");
    if (commentArea.style.display === "none") {
        commentArea.style.display = "block";
      } else {
        commentArea.style.display = "none";
      }
}

//Reply
function showReplies(id){
    var replyArea = document.getElementById(id);
    if (replyArea.style.display === "none") {
        replyArea.style.display = "block";
    } else {
        replyArea.style.display = "none";
      }
}