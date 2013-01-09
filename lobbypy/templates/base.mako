<%namespace name="utils" file="utils.mako"/>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="utf-8" />
  ${utils.socketio_link()}
  ${utils.jquery_link()}
  ${utils.js_link("bootstrap.min.js")}
  ${utils.js_link("handlebars.js")}
  ${utils.css_link("bootstrap.min.css")}
  ${utils.css_link("default.css")}
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
  ## ${next.css() | trim}
  <title>LobbyPy</title>
</head>
<body data-spy="scroll" data-target=".subnav" data-offset="50">
  <%include file="navbar.mako"/>
  <div class="container">
    <div class="row">
      <div class="span12 row-white">
        ${next.main_content() | trim}
      </div> <!-- div span12 -->
    </div> <!-- div row -->
  </div> <!-- div container -->
</body>
</html>
