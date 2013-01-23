<script id="admin-lobby-details-template" type="text/x-handlebars-template">
    {{#if this}}
        <div class="span3">
          <h3>Lobby details</h3>
          <strong>{{name}}</strong>
          <p>Lobby ID: {{id}}</p>
          <p>Owner: {{owner.name}}</p>
          <p>Game map: {{game_map}}</p>
          <p>Players: {{player_count}} / 18</p>
        </div>
        <div class="span3">
          <h3>Teams</h3>
          <table class="admin-lobbytable">
            <tr>
	      {{#each teams}}
                <td class="bluh">{{name}}</td>
              {{/each}}
	      <td class="spech">Spectators</td>
            </tr>
            <tr>
              {{#each teams}}
                <td class="blup">
		  {{#if players}}
                  <ul class="admin-lobbyplayers">
		    {{#each players}}
                      <li class="admin-blu-player"><input type="checkbox" name="blu-lobbyplayers" id="admin-lobbyplayer-{{id}}"><label class="lpt-label" for="admin-lobbyplayer-{{id}}">{{player.name}}</label></li>
		    {{/each}}
                  </ul>
		  {{else}}
		    No Players.
		  {{/if}}
                </td>
              {{/each}}
	      <td class="specp">
	        {{#if spectators}}
		  {{#each spectators}}
		    {{name}}
		  {{/each}}
		{{else}}
		  No Spectators.
		{{/if}}
	      </td>
            </tr>
          </table>
    {{else}}
        <div class="span6">
          <span class="admin-noitem">No lobby selected</span>
	</div>
    {{/if}}
</script>
