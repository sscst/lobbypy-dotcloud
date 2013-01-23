<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="js()" filter="trim">
  ${utils.jqueryui_link()}
  ${utils.js_link("admin.js")}
</%def>

<%def name="hb()" filter="trim">
  <%include file="handlebars/admin_lobby_listing.mako"/>
  <%include file="handlebars/admin_player_listing.mako"/>
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
        <a href="#addPlayer" data-toggle="modal"><button class="btn btn-success"><i class="icon-plus"></i> New player</button></a>
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
            <button id="create-player" class="btn btn-primary" data-dismiss="modal">Create Lobby</button>
            <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
          </div>
        </div>
        <button id="delete-player" class="btn btn-danger"><i class="icon-bolt"></i> Delete selected player</button><br/>
      </div>
    </div>
  </div>
  <div class="row">
    <div class="span3">
      <h3>Lobby details</h3>
      <strong>Lobby name</strong>
      <p>Lobby ID: </p>
      <p>Owner: </p>
      <p>Game map: </p>
      <p>Players: 9 / 18</p>
    </div>
    <div class="span3">
      <h3>Teams</h3>
      <table class="admin-lobbytable">
        <tr>
          <td class="bluh">BLU</td><td class="redh">RED</td>
        </tr>
        <tr>
          <td class="blup">
            <ul class="admin-lobbyplayers">
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b1"><label class="lpt-label" for="b1">Player 1</label></li>
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b2"><label class="lpt-label" for="b2">Player 2</label></li>
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b3"><label class="lpt-label" for="b3">Player 3</label></li>
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b4"><label class="lpt-label" for="b4">Player 4</label></li>
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b5"><label class="lpt-label" for="b5">Player 5</label></li>
              <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="b6"><label class="lpt-label" for="b6">Player 6</label></li>
            </ul>
          </td>
          <td class="redp">
            <ul class="admin-lobbyplayers">
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r1"><label class="lpt-label" for="r1">Player 1</label></li>
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r2"><label class="lpt-label" for="r2">Player 2</label></li>
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r3"><label class="lpt-label" for="r3">Player 3</label></li>
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r4"><label class="lpt-label" for="r4">Player 4</label></li>
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r5"><label class="lpt-label" for="r5">Player 5</label></li>
              <li class="admin-red-player"><input type="checkbox" name="red-lobbyplayers" id="r6"><label class="lpt-label" for="r6">Player 6</label></li>
            </ul>
          </td>
        </tr>
      </table>
      <p>Spectators: </p>
    </div>
    <div class="span6">
      <h3>Player details</h3>
      <strong>Player name</strong>
      <p>Player ID: </p>
      <p>Current lobby: </p>
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
