import pytest

from flask import Flask, request, render_template, session

from getflix.repository.memory_repo import MemoryRepo
from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie
from getflix.domainmodel.review import Review
from getflix.domainmodel.user import User
from getflix.domainmodel.watchlist import Watchlist

from getflix import create_app


def get_auth_status(responseData):
    try:
        html = str(responseData)
        statusTag = '<span id="AuthStatus" style="display:none;">'
        statusStart = html.index(statusTag) + len(statusTag)
        statusEnd = statusStart
        while html[statusEnd] != "<":
            statusEnd += 1
        status = html[statusStart:statusEnd].replace("&#39;" , "'")
        return status
    except ValueError:
        raise ValueError("AuthStatus html tag edited without updating test file!")

def get_auth_message(responseData):
    try:
        html = str(responseData)
        messageTag = '<p id="AuthMessage">'
        messageStart = html.index(messageTag) + len(messageTag)
        messageEnd = messageStart
        while html[messageEnd] != "<":
            messageEnd += 1
        message = html[messageStart:messageEnd].replace("&#39;" , "'")
        return message
    except ValueError:
        raise ValueError("AuthMessage html tags edited without updating test file!")

def get_watchlist_size(responseData):
    try:
        html = str(responseData)
        sizeTag = '<span id="WatchlistSize" style="display:none;">'
        sizeStart = html.index(sizeTag) + len(sizeTag)
        sizeEnd = sizeStart
        while html[sizeEnd] != "<":
            sizeEnd += 1
        size = html[sizeStart:sizeEnd].replace("&#39;" , "'")
        return size
    except ValueError:
        raise ValueError("WatchlistSize html tag edited without updating test file!")

def get_movie_list_size(responseData):
    try:
        html = str(responseData)
        sizeTag = '<span id="MovieListSize" style="display:none;">'
        sizeStart = html.index(sizeTag) + len(sizeTag)
        sizeEnd = sizeStart
        while html[sizeEnd] != "<":
            sizeEnd += 1
        size = html[sizeStart:sizeEnd].replace("&#39;" , "'")
        return size
    except ValueError:
        raise ValueError("MovieListSize html tag edited without updating test file!")


@pytest.fixture
def client():
    test_app = create_app()
    test_app.testing = True
    return test_app.test_client()


def test_register(client):
    response = client.get("/register?RegUsername=&RegPassword1=Mypassword1&RegPassword2=Mypassword1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "registering"
    assert authMessage == "Please enter a valid username"
    response = client.get("/register?RegUsername=bob&RegPassword1=MYpassword1&RegPassword2=myPASSWORD2")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "registering"
    assert authMessage == "Passwords don't match - please try again"
    response = client.get("/register?RegUsername=bob&RegPassword1=mypassword&RegPassword2=mypassword")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "registering"
    assert authMessage == "Passwords must contain at least 8 characters (including upper/lower-case letters and digits)"
    response = client.get("/register?RegUsername=bob&RegPassword1=Pass1&RegPassword2=Pass1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "registering"
    assert authMessage == "Passwords must contain at least 8 characters (including upper/lower-case letters and digits)"
    response = client.get("/register?RegUsername=bob&RegPassword1=Mypassword1&RegPassword2=Mypassword1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "logged in"
    assert authMessage == ""
    response = client.get("/register?RegUsername=bob&RegPassword1=Mypassword1&RegPassword2=Mypassword1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "registering"
    assert authMessage == "Username already taken - please try again"

def test_login(client):
    response = client.get("/register?RegUsername=bob&RegPassword1=Mypassword1&RegPassword2=Mypassword1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "logged in"
    assert authMessage == ""
    response = client.get("/logout")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "logged out"
    assert authMessage == ""
    response = client.get("/login?LoginUsername=bob&LoginPassword=Mypassword1")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    assert authStatus == "logged in"
    assert authMessage == ""

def test_browse(client):
    response = client.get("/browse?BrowseCategory=TitleChar&BrowseQuery=0-9")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "22"
    response = client.get("/browse?BrowseCategory=TitleChar&BrowseQuery=K")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "17"
    response = client.get("/browse?BrowseCategory=Genre&BrowseQuery=Crime")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "150"
    response = client.get("/browse?BrowseCategory=Genre&BrowseQuery=Music")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "21"
    response = client.get("/browse?BrowseCategory=Director&BrowseQuery=Christopher+Nolan")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "5"
    response = client.get("/browse?BrowseCategory=Director&BrowseQuery=Mel+Gibson")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "2"
    response = client.get("/browse?BrowseCategory=Actor&BrowseQuery=Adrien+Brody")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "2"
    response = client.get("/browse?BrowseCategory=Actor&BrowseQuery=Scarlett+Johansson")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "12"

def test_search(client):
    response = client.get("/search?SearchCategory=title&SearchQuery=light")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "11"
    response = client.get("/search?SearchCategory=title&SearchQuery=top")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "4"
    response = client.get("/search?SearchCategory=Genre&SearchQuery=roman")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "141"
    response = client.get("/search?SearchCategory=Genre&SearchQuery=horror")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "119"
    response = client.get("/search?SearchCategory=Director&SearchQuery=ste")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "37"
    response = client.get("/search?SearchCategory=Director&SearchQuery=smith")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "6"
    response = client.get("/search?SearchCategory=Actor&SearchQuery=michael")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "74"
    response = client.get("/search?SearchCategory=Actor&SearchQuery=leonardo+d")
    movieListSize = get_movie_list_size(response.data)
    assert movieListSize == "10"

def test_watchlist(client):
    response = client.get("/add_movie?MovieTitle=Inception")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    watchlistSize = get_watchlist_size(response.data)
    assert authStatus == "logging in"
    assert authMessage == "You must be logged in to update your watchlist"
    assert watchlistSize == "0"
    client.get("/register?RegUsername=bob&RegPassword1=Mypassword1&RegPassword2=Mypassword1")
    response = client.get("/add_movie?MovieTitle=Inception")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    watchlistSize = get_watchlist_size(response.data)
    assert authStatus == "logged in"
    assert authMessage == ""
    assert watchlistSize == "1"
    response = client.get("/remove_movie?MovieTitle=Inception")
    authStatus = get_auth_status(response.data)
    authMessage = get_auth_message(response.data)
    watchlistSize = get_watchlist_size(response.data)
    assert authStatus == "logged in"
    assert authMessage == ""
    assert watchlistSize == "0"