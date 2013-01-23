$(document).ready(function() {
    /* Templates */
    var lobby_listing_template = Handlebars.compile($("#admin-lobby-listing-template").html());
    var lobby_details_template = Handlebars.compile($("#admin-lobby-details-template").html());
    var player_listing_template = Handlebars.compile($("#admin-player-listing-template").html());
    var player_details_template = Handlebars.compile($("#admin-player-details-template").html());

    /* Backbone */
    var LobbyModel = Backbone.Model.extend({
        idAttribute: "id"
    });
    var LobbyCollection = Backbone.Collection.extend({
        model: LobbyModel
    });
    var LobbyListingView = Backbone.View.extend({
        events: {
            "click .admin-lobbyitem": "select"
        },
        select: function(evt) {
            this.deselect();
            $(evt.currentTarget).addClass("selected");
            var id = getDbIdFromId($(evt.currentTarget).attr('id'));
            lobbyDetails.model = this.collection.get(id)
            lobbyDetails.render();
        },
        deselect: function() {
            $(this.el).children(".admin-lobbyitem").removeClass("selected");
        },
        update: function() {
            var me = this;
            this.deselect();
            $.getJSON("/admin/rest/lobbies", function(data) {
                me.collection.reset(data['lobbies']);
                me.render();
            });
        },
        render: function() {
            $(this.el).html(lobby_listing_template({lobbies: this.collection.toJSON()}));
            return this;
        }
    });
    var LobbyDetailsView = Backbone.View.extend({
        render: function() {
            $(this.el).html(lobby_details_template(this.model.toJSON()));
            return this;
        }
    });
    var lobbyCollection = new LobbyCollection({});
    var lobbyModel = new LobbyModel({});
    var lobbyListing = new LobbyListingView({
        el: $("#admin-lobby-list-container"),
        collection: lobbyCollection
    });
    var lobbyDetails = new LobbyDetailsView({
        el: $("#admin-lobby-details-container"),
        model: lobbyModel
    });

    var PlayerModel = Backbone.Model.extend({
        idAttribute: "id"
    });
    var PlayerCollection = Backbone.Collection.extend({
        model: PlayerModel
    });
    var PlayerListingView = Backbone.View.extend({
        events: {
            "click .admin-playeritem": "select"
        },
        select: function(evt) {
            this.deselect();
            $(evt.currentTarget).addClass("selected");
            var id = getDbIdFromId($(evt.currentTarget).attr('id'));
            playerDetails.model = this.collection.get(id)
            playerDetails.render();
        },
        deselect: function() {
            $(this.el).children(".admin-playeritem").removeClass("selected");
        },
        update: function() {
            var me = this;
            this.deselect();
            $.getJSON("/admin/rest/players", function(data) {
                me.collection.reset(data['players']);
                me.render();
            });
        },
        render: function() {
            $(this.el).html(player_listing_template({players: this.collection.toJSON()}));
            return this;
        }
    });
    var PlayerDetailsView = Backbone.View.extend({
        render: function() {
            $(this.el).html(player_details_template(this.model.toJSON()));
            return this;
        }
    });
    var playerCollection = new PlayerCollection({});
    var playerModel = new PlayerModel({});
    var playerListing = new PlayerListingView({
        el: $("#admin-player-list-container"),
        collection: playerCollection
    });
    var playerDetails = new PlayerDetailsView({
        el: $("#admin-player-details-container"),
        model: playerModel
    });

    /* jQuery */
    $("#get-lobbies").click(function() {
        lobbyListing.update();
    });
    $("#get-players").click(function() {
        playerListing.update();
    });
    $("#create-lobby").click(function() {
        createLobby();
        lobbyListing.update();
    });
    $("#create-player").click(function() {
        createPlayer();
        playerListing.update();
    });
    $("#delete-player").click(function() {
        var playerElements = $(".admin-playeritem.selected");
        if (playerElements.length == 1) {
            var id = getDbIdFromId($(playerElements[0]).attr('id'));
            deletePlayer(id);
        } else if (playerElements.length > 1) {
            playerListing.deselect();
        }
        playerListing.update();
    });
    $("#delete-lobby").click(function() {
        var lobbyElements = $(".admin-lobbyitem.selected");
        if (lobbyElements.length == 1) {
            var id = getDbIdFromId($(lobbyElements[0]).attr('id'));
            deleteLobby(id);
        } else if (lobbyElements.length > 1) {
            lobbyListing.deselect();
        }
        lobbyListing.update();
    });

    /* Functions */
    var getDbIdFromId = function(id) {
        return id.slice(id.indexOf('-') - id.length + 1);
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
    };
    var deleteLobby = function(id) {
        $.ajax("/admin/rest/lobbies/" + id, {
            type: "DELETE"
        });
    };
    var createPlayer = function() {
        var form = $("#create-player-form");
        $.post("/admin/rest/players", {
            steam_id: form.children("[name=steam_id]").val()
        });
        form.children().val('');
    };
    var deletePlayer = function(id) {
        $.ajax("/admin/rest/players/" + id, {
            type: "DELETE"
        });
    };

    /* Startup */
    lobbyListing.update();
    playerListing.update();
});
