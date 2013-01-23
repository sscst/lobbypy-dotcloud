<script id="admin-player-details-template" type="text/x-handlebars-template">
  {{#if this}}
      Player ID: {{id}}<br/>
      Steam ID: {{steam_id}}<br/>
      Name: {{name}}<br/>
  {{else}}
      No player selected.
  {{/if}}
</script>
