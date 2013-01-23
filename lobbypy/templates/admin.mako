<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="js()" filter="trim">
  ${utils.jqueryui_link()}
  ${utils.js_link("admin.js")}
</%def>

<%def name="hb()" filter="trim">
  <%include file="handlebars/admin_lobby_listing.mako"/>
  <%include file="handlebars/admin_lobby_details.mako"/>
  <%include file="handlebars/admin_player_listing.mako"/>
  <%include file="handlebars/admin_player_details.mako"/>
</%def>

<%def name="main_content()" filter="trim">
  <div id="legend">
    <legend>Admin Dashboard</legend>
  </div>
  <div class="row">
    <div class="span6">
      <h3>Lobbies</h3>
      <button id="get-lobbies" class="btn btn-info pull-right"><i class="icon-refresh"></i></button>
      <div class="span5">
        <div class="well" style="height: 200px; overflow: auto;">
          <div id="admin-lobby-list-container">
	  </div>
        </div>
        <button class="btn btn-success" href="#addLobby" data-toggle="modal"><i class="icon-plus"></i> New lobby</button>
        <div id="addLobby" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="addLobbyLabel" aria-hidden="true">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="addLobbyLabel">Create Lobby</h3>
          </div>
          <div class="modal-body">
            <form id="create-lobby-form">
              Name: <input type="text" name="name"/><br/>
              Owner: <input type="text" name="owner_id"/><br/>
              Server: <input type="text" name="server_address"/><br/>
              Password: <input type="password" name="password"/><br/>
              Map: <input type="text" name="game_map"/><br/>
            </form>
          </div>
          <div class="modal-footer">
            <button id="create-lobby" class="btn btn-primary" data-dismiss="modal">Create Lobby</button>
            <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
          </div>
        </div>
        <button id="delete-lobby" href="#deleteLobby" class="btn btn-danger"><i class="icon-bolt"></i> Delete selected lobby</a>
      </div>
    </div>
    <div class="span6">
      <h3>Players</h3>
      <button id="get-players" class="btn btn-info pull-right"><i class="icon-refresh"></i></button>
      <div class="span5">
        <div class="well" style="height: 200px; overflow: auto;">
          <div id="admin-player-list-container">
	  </div>
        </div>
        <button class="btn btn-success" href="#addPlayer" data-toggle="modal"><i class="icon-plus"></i> New player</button></a>
        <div id="addPlayer" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="addPlayerLabel" aria-hidden="true">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="addPlayerLabel">Create Lobby</h3>
          </div>
          <div class="modal-body">
            <form id="create-player-form">
              64bit SteamID: <input type="text" name="steam_id"/><br/>
            </form>
          </div>
          <div class="modal-footer">
            <button id="create-player" class="btn btn-primary" data-dismiss="modal">Create Player</button>
            <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
          </div>
        </div>
        <button id="delete-player" class="btn btn-danger"><i class="icon-bolt"></i> Delete selected player</button><br/>
      </div>
    </div>
  </div>
  <div class="row">
    <div id="admin-lobby-details-container">
    </div>
    <div class="span6">
      <h3>Player details</h3>
      <div id="admin-player-details-container">
      </div>
    </div>
  </div>
  <div class="row">
    <div class="span3">
      <button class="btn btn-warning"><i class="icon-random"></i> Change owner</button>
    </div>
    <div class="span3">
      <button class="btn btn-danger"><i class="icon-trash"></i> Kick player(s)</button>
    </div>
  </div>
</%def>
