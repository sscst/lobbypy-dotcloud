$(document).ready(function() {
    var lobby_listing_template = Handlebars.compile($("#admin-lobby-listing-template").html());
    var player_listing_template = Handlebars.compile($("#admin-player-listing-template").html());
    $("#get-lobbies").click(function() {
        updateLobbies();
    });
    $("#get-players").click(function() {
        updatePlayers();
    });
    var updateLobbies = function() {
        $.getJSON("/admin/rest/lobbies", function(data) {
            $("#admin-lobby-list-container").html(lobby_listing_template(data));
        });
    };

    var updatePlayers = function() {
        $.getJSON("/admin/rest/players", function(data) {
            $("#admin-player-list-container").html(player_listing_template(data));
        });
    };
    updateLobbies();
    updatePlayers();
});
