<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="js()" filter="trim">
  ${utils.jqueryui_link()}
  ${utils.js_link("admin.js")}
</%def>

<%def name="main_content()" filter="trim">
  <div id="legend">
    <legend>Admin Dashboard</legend>
  </div>
  <div class="row">
    <div class="span6">
      <h3>Lobbies</h3>
      <button class="btn btn-info pull-right"><i class="icon-refresh"></i></button>
      <div class="span5">
        <div class="well" style="height: 200px; overflow: auto;">
          <ul id="admin-lobby-list">
            <li class="admin-lobbyitem" id="id">
              Hello world.
            </li>
            <li class="admin-lobbyitem" id="id">
              This is a lobby
            </li>
            <li class="admin-lobbyitem" id="id">
              Hello?
            </li>
          </ul>
        </div>
        <button class="btn btn-success"><i class="icon-plus"></i> New lobby</button>
        <button class="btn btn-danger"><i class="icon-bolt"></i> Delete selected lobby</button>
      </div>
    </div>
    <div class="span6">
      <h3>Players</h3>
      <button class="btn btn-info pull-right"><i class="icon-refresh"></i></button>
      <div class="span5">
        <div class="well" style="height: 200px; overflow: auto;">
        </div>
        <button class="btn btn-success"><i class="icon-plus"></i> New player</button>
        <button class="btn btn-danger"><i class="icon-bolt"></i> Delete selected player</button><br />
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
            <ul id="admin-blu-lobbyplayers">
              <li class="admin-blu-player">Player 1</li>
              <li class="admin-blu-player">Player 2</li>
              <li class="admin-blu-player">Player 3</li>
              <li class="admin-blu-player">Player 4</li>
              <li class="admin-blu-player">Player 5</li>
              <li class="admin-blu-player">Player 6</li>
            </ul>
          </td>
          <td class="redp">
            <ul id="admin-red-lobbyplayers">
              <li class="admin-red-player">Player 1</li>
              <li class="admin-red-player">Player 2</li>
              <li class="admin-red-player">Player 3</li>
              <li class="admin-red-player">Player 4</li>
              <li class="admin-red-player">Player 5</li>
              <li class="admin-red-player">Player 6</li>
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