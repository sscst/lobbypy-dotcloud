<script id="lobbies_view" type="text/x-handlebars-template">
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
