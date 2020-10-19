

function show(ID) {
    document.getElementById(ID).style.display = "block";
}
function hide(ID) {
    document.getElementById(ID).style.display = "none";
}
function toggle(ID) {
    if (document.getElementById(ID).style.display != "block") {
        show(ID);
    } else {
        hide(ID);
    }
}


function showMainWindow() {
    show("MainWindow");
    hide("LoginWindow");
    hide("RegisterWindow");
}
function showLoginWindow() {
    hide("MainWindow");
    show("LoginWindow");
    hide("RegisterWindow");
}
function showRegisterWindow() {
    hide("MainWindow");
    hide("LoginWindow");
    show("RegisterWindow");
}


function loginUser() {
    showMainWindow()
    hide("LoginButton");
    show("LogoutButton");
    hide("RegisterButton");
}
function logoutUser() {
    show("LoginButton");
    hide("LogoutButton");
    show("RegisterButton");
}


function toggleBrowseTitles() {
    if (document.getElementById("BrowseTitles").style.display != "block") {
        show("BrowseTitles");
        document.getElementById("titlesHeading").innerHTML = "&#8595 Titles";
        hide("BrowseGenres");
        document.getElementById("genresHeading").innerHTML = "&#8594 Genres";
        hide("BrowseDirectors");
        document.getElementById("directorsHeading").innerHTML = "&#8594 Directors";
        hide("BrowseActors");
        document.getElementById("actorsHeading").innerHTML = "&#8594 Actors";
    } else {
        hide("BrowseTitles");
        document.getElementById("titlesHeading").innerHTML = "&#8594 Titles";
    }
}
function toggleBrowseGenres() {
    if (document.getElementById("BrowseGenres").style.display != "block") {
        hide("BrowseTitles");
        document.getElementById("titlesHeading").innerHTML = "&#8594 Titles";
        show("BrowseGenres");
        document.getElementById("genresHeading").innerHTML = "&#8595 Genres";
        hide("BrowseDirectors");
        document.getElementById("directorsHeading").innerHTML = "&#8594 Directors";
        hide("BrowseActors");
        document.getElementById("actorsHeading").innerHTML = "&#8594 Actors";
    } else {
        hide("BrowseGenres");
        document.getElementById("genresHeading").innerHTML = "&#8594 Genres";
    }
}
function toggleBrowseDirectors() {
    if (document.getElementById("BrowseDirectors").style.display != "block") {
        hide("BrowseTitles");
        document.getElementById("titlesHeading").innerHTML = "&#8594 Titles";
        hide("BrowseGenres");
        document.getElementById("genresHeading").innerHTML = "&#8594 Genres";
        show("BrowseDirectors");
        document.getElementById("directorsHeading").innerHTML = "&#8595 Directors";
        hide("BrowseActors");
        document.getElementById("actorsHeading").innerHTML = "&#8594 Actors";
    } else {
        hide("BrowseDirectors");
        document.getElementById("directorsHeading").innerHTML = "&#8594 Directors";
    }
}
function toggleBrowseActors() {
    if (document.getElementById("BrowseActors").style.display != "block") {
        hide("BrowseTitles");
        document.getElementById("titlesHeading").innerHTML = "&#8594 Titles";
        hide("BrowseGenres");
        document.getElementById("genresHeading").innerHTML = "&#8594 Genres";
        hide("BrowseDirectors");
        document.getElementById("directorsHeading").innerHTML = "&#8594 Directors";
        show("BrowseActors");
        document.getElementById("actorsHeading").innerHTML = "&#8595 Actors";
    } else {
        hide("BrowseActors");
        document.getElementById("actorsHeading").innerHTML = "&#8594 Actors";
    }
}

function toggleReviewsButton(ID) {
    if (document.getElementById(ID).value === "Show Reviews") {
        document.getElementById(ID).value = "Hide Reviews"
    } else {
        document.getElementById(ID).value = "Show Reviews"
    }
}
function toggleDetailsButton(ID) {
    if (document.getElementById(ID).value === "Show Details") {
        document.getElementById(ID).value = "Hide Details"
    } else {
        document.getElementById(ID).value = "Show Details"
    }
}


switch(document.getElementById("AuthStatus").innerHTML) {
    case "logged in":
        loginUser();
        break;
    case "logged out":
        logoutUser();
        break;
    case "logging in":
        showLoginWindow();
        break;
    case "registering":
        showRegisterWindow();
        break;
    default:  // This case shouldn't be reached
        showMainWindow();
        console.log("WARNING: Invalid AuthStatus Value");
}