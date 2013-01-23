<script id="admin-lobby-listing-template" type="text/x-handlebars-template">
    {{#if lobbies}}
        <ul id="admin-lobby-list">
        {{#each lobbies}}
            <li class="admin-lobbyitem" id="lobby-{{id}}">
                <span class="title">{{name}}</span>
            </li>
        {{/each}}
	</ul>
    {{else}}
        <span class="admin-noitems">No lobbies</span>
    {{/if}}
</script>
