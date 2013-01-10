/*
 * Lobbypy
 *
 * Namespace: /lobby/
 * create(lobby_item_info)
 * - Create event for lobby listing
 * - Parameters:
 *   - lobby_item_info (see schema)
 * update(lobby_item_info)
 * - Update event for lobby listing
 * - Parameters:
 *   - lobby_item_info (see schema)
 * delete(lobby_id)
 * - Delete event for lobby listing
 * - Parameters:
 *   - lobby_id:
 *     - id of lobby deleted
 *
 * Namespace: /lobby/<lobby_id>
 * update(lobby_info)
 * - Update event for lobby
 * - Parameters:
 *   - lobby_info (see schema)
 * leave()
 * - Leave event for lobby.  Player has left lobby and will not
 *   recieve any more updates for the lobby.
 * delete()
 * - Delete event for lobby.  Lobby has been deleted.
 */
WEB_SOCKET_SWF_LOCATION = "/static/WebSocketMain.swf";
WEB_SOCKET_DEBUG = true;

$(document).ready(function() {
    var lobby_listing_socket = io.connect('/lobbies');
    var lobby_socket = io.connect('/lobby');

    var LobbyModel = Backbone.Model.extend({});
    var LobbyView = Backbone.View.extend({
        initialize: function() {
            var me = this;
            lobby_socket.on("update", function(lobby_info) {
                me.model = lobby_info;
                me.render();
            });
            lobby_socket.on("leave", function() {
                alert("You have left the lobby.");
            });
            lobby_socket.on("destroy", function() {
                alert("The lobby has been deleted.");
            });
        },

        render: function() {
            var template = Handlebars.compile($("#lobby_template").html());
            $(this.el).html(template(this.model));
            return this;
        }
    });

    var LobbyItemModel = Backbone.Model.extend({});
    var LobbyItemCollection = Backbone.Collection.extend({
        model: LobbyItemModel
    });
    var LobbyItemCollectionView = Backbone.View.extend({
        initialize: function() {
            var me = this;
            lobby_listing_socket.on("create", function(lobby_info) {
                // Insert lobby into collection
                me.collection.unshift(lobby_info);
                me.render();
            });
            lobby_listing_socket.on("update", function(lobby_info) {
                // Find lobby w/ matching id
                lobby_old = me.collection.filter(function(lobby_old) {
                    lobby_old.id === lobby.id;
                })[0];
                lobby_old = lobby_info;
                me.render();
            });
            lobby_listing_socket.on("delete", function(lobby_id) {
                // Find lobby w/ matching id
                lobby_old = me.collection.filter(function(lobby_old) {
                    lobby_old.id === lobby_id;
                })[0];
                me.collection.pop(lobby_old);
                me.render();
            });
        },

        render: function() {
            var template = Handlebars.compile($("#lobby_listing_template").html());
            $(this.el).html(template(this.collection));
            return this;
        }
    });

    var Router = Backbone.Router.extend({
        routes: {
            "": "lobby_listing",
            "lobby/:lobby_id": "lobby"
        },

        lobby_listing: function() {
            // TODO: Until lobby listing is retrieved show loading icon
            // Get lobby listing and on callback make lobby listing view
            lobby_listing_socket.emit("subscribe",
                function(success, lobby_listing) {
                    if (success) {
                        var view = new LobbyItemCollectionView({
                            el: $("#app-container"),
                            collection: lobby_listing,
                        });
                        view.render();
                    }
            });
        },

        lobby: function() {
            lobby_socket.emit("join",
                function(success, lobby_info) {
                    if (success) {
                        var view = new LobbyView({
                            el: $("#app-container"),
                            model: lobby_info,
                        });
                        view.render();
                    }
            });
        }
    });

    var app = new Router();
    Backbone.history.start({pushState: true, hashChange: false});
});
