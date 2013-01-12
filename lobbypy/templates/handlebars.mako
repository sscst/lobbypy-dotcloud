<script id="lobby_listing_template" type="text/x-handlebars-template">
  <div class="row">
    <div class="span12">
      <div class="lobbylist-box">
        <ul id="lobbylist">
        {{#each lobbyitem}}
          <a href="{{lobbyurl}}">
            <li class="lobbyitem" id="{{id}}">
              {{! <img src="{{map_img}}" class="map-img" /> }}
              {{! <img src="{{region}}" class="region-img" /> }}
              {{! <img src="{{classes_left}}" class="classes-img" /> }}
              {{! <span class="spectators">{{spectator_count}}</span> }}
              <span class="title">{{name}}</span>
              <span class="map">{{game_map}}</span>
              <span class="players">{{player_count}} / {{max_players}}</span>
            </li>
          </a>
          {{/each}}
        </ul>
      </div>
    </div>
  </div>
</script>
<script id="lobby_template" type="text/x-handlebars-template">
  <div class="row">
    <div class="span6">
      <h2>{{title}}</h2>
      <div class="span3">
        <div class="map-img"></div>
      </div>
      <div class="span2">
        <div class="map-details">
          <p class="map-name">{{game_map}}</p>
          <p class="option-value">Control Points</p>
          <p class="option-value">30 minutes</p>
          <p class="option-value">5 wins</p>
        </div>
      </div>
    </div>
    <div class="row">
      <table class="lobbytable">
        <tr>
          <th class="bluh">BLU</th>
          <th class="cih" width="25"></th>
          <th class="redh">RED</th>
        </tr>
      </table>
    </div>
  </div>
</script>