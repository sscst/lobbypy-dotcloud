<script id="lobby-template" type="text/x-handlebars-template">
  <div class="row">
    <div class="span6">
      <h2>{{name}}</h2>
      <div class="span3">
        <img src="/static/images/map_placeholder.png" class="map-img" />
      </div>
      <div class="span2">
        <div class="map-details">
          <p class="map-name">{{game_map}}</p>
        </div>
      </div>
      <div class="span1"></div>
    </div>
    <div class="span6">
      <div id="class-selection">
        <img src="/static/images/scout.png" class="classicon" />
        <img src="/static/images/soldier.png" class="classicon" />
        <img src="/static/images/pyro.png" class="classicon" />
        <img src="/static/images/demoman.png" class="classicon" />
        <img src="/static/images/heavy.png" class="classicon" />
        <img src="/static/images/engineer.png" class="classicon" />
        <img src="/static/images/medic.png" class="classicon" />
        <img src="/static/images/sniper.png" class="classicon" />
        <img src="/static/images/spy.png" class="classicon" />
      </div>
      <table class="lobbytable">
        <thead>
          <tr>
            {{#each teams}}
            <th class="{{name}}h" id="team-{{id}}">{{name}}</th>
            {{/each}}
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <ul id="bluteamlist" class="teamplayerlist">
                {{#each team.0.players}}
                <li>
                  <div class="playerinfo">
                    <div class="name">{{player.name}}</div>
                  </div>
                  <img class="classicon" src="/static/images/{{class_id}}.png" alt="?" />
                  <div class="clearfix"></div>
                </li>
                {{/each}}
              </ul>
            </td>
            <td>
              <ul id="redteamlist" class="teamplayerlist">
                {{#each team.1.players}}
                <li>
                  <div class="playerinfo">
                    <div class="name">{{player.name}}</div>
                  </div>
                  <img class="classicon" src="/static/images/{{class_id}}.png" alt="?" />
                  <div class="clearfix"></div>
                </li>
                {{/each}}
              </ul>
            </td>
          </tr>
          <tr>
            <td colspan="2">
            <div id="spectator-group">
              <div id="spectator-count">
              {{#if spectators.length}}
                Spectators ({{this.length}}):
              {{else}}
                No spectators.
              {/if}}
              </div>
              <ul id="specteamlist">
                <li>
                  {{#each spectators}}
                  <div class="name">{{player.name}}</div>
                  {{/each}}
                </li>
              </ul>
            </div>
            </td>
          </tr>
        </tbody>
      </table>
      </div>
    </div>
  </div>
</script>
