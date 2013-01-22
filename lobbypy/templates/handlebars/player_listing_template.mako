<script id="player-listing-template" type="text/x-handlebars-template">
  {{#each players}}
    [{{this.id}}] {{this.steam_id}}: {{this.name}}
  {{/each}}
</script>
