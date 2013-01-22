<script id="admin-lobby-listing-template" type="text/x-handlebars-template">
    {{#if lobbies}}
        <ul id="admin-lobby-list">
        {{#each lobbies}}
            <li class="admin-lobbyitem" id="{{id}}">
                {{! <img src="{{map_img}}" class="map-img" /> }}
                {{! <img src="{{region}}" class="region-img" /> }}
                {{! <img src="{{classes_left}}" class="classes-img" /> }}
                {{! <span class="spectators">{{spectator_count}}</span> }}
                <span class="title">{{name}}</span>
                <span class="map">{{game_map}}</span>
                <span class="players">{{player_count}} / {{max_players}}</span>
            </li>
        {{/each}}
	</ul>
    {{else}}
        <span class="admin-noitems">No lobbies</span>
    {{/if}}
</script>
