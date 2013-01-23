<script id="admin-player-listing-template" type="text/x-handlebars-template">
  <ul id="admin-player-list">
  {{#each players}}
    <li class="admin-playeritem" id="player-{{id}}">
        [{{id}}] {{steam_id}}: {{name}}
    </li>
  {{/each}}
  </ul>
</script>
