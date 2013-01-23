$(document).ready(function() {
    var lobby_listing_template = Handlebars.compile($("#admin-lobby-listing-template").html());
    var player_listing_template = Handlebars.compile($("#admin-player-listing-template").html());
    $("#get-lobbies").click(function() {
        updateLobbies();
    });
    $("#get-players").click(function() {
        updatePlayers();
    });
    $("#create-lobby").click(function() {
        createLobby();
    });
    $("#create-player").click(function() {
        createPlayer();
    });
    $("#delete-player").click(function() {
        var playerElements = $(".admin-playeritem.selected");
        if (playerElements.length == 1) {
            var id = getDbIdFromId($(playerElements[0]).attr('id'));
            deletePlayer(id);
        } else if (playerElements.length > 1) {
            deselectPlayers();
        }
    });
    $("#delete-lobby").click(function() {
        var lobbyElements = $(".admin-lobbyitem.selected");
        if (lobbyElements.length == 1) {
            var id = getDbIdFromId($(lobbyElements[0]).attr('id'));
            deleteLobby(id);
        } else if (lobbyElements.length > 1) {
            deselectLobbies();
        }
    });
    $("#admin-lobby-list-container").on("click", ".admin-lobbyitem", function() {
        deselectLobbies();
        $(this).addClass("selected");
    });
    $("#admin-player-list-container").on("click", ".admin-playeritem", function() {
        deselectPlayers();
        $(this).addClass("selected");
    });
    var getDbIdFromId = function(id) {
        return id.slice(id.indexOf('-') - id.length + 1);
    };
    var deselectLobbies = function() {
        $(".admin-lobbyitem").removeClass("selected");
    };
    var deselectPlayers = function() {
        $(".admin-playeritem").removeClass("selected");
    };
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
    var createLobby = function() {
        var form = $("#create-lobby-form");
        $.post("/admin/rest/lobbies", {
            name: form.children("[name=name]").val(),
            owner_id: form.children("[name=owner_id]").val(),
            server_address: form.children("[name=server_address]").val(),
            game_map: form.children("[name=game_map]").val(),
            password: form.children("[name=password]").val()
        });
        form.children().val('');
        updateLobbies();
    };
    var deleteLobby = function(id) {
        $.ajax("/admin/rest/lobbies/" + id, {
            type: "DELETE"
        });
        updateLobbies();
    };
    var createPlayer = function() {
        var form = $("#create-player-form");
        $.post("/admin/rest/players", {
            steam_id: form.children("[name=steam_id]").val()
        });
        form.children().val('');
        updatePlayers();
    };
    var deletePlayer = function(id) {
        $.ajax("/admin/rest/players/" + id, {
            type: "DELETE"
        });
        updatePlayers();
    };
    updateLobbies();
    updatePlayers();
});
