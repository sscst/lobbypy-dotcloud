<script id="admin-player-listing-template" type="text/x-handlebars-template">
  <ul id="admin-player-list">
  {{#each players}}
    <li class="admin-playeritem">
        [{{this.id}}] {{this.steam_id}}: {{this.name}}
    </li>
  {{/each}}
  </ul>
</script>
