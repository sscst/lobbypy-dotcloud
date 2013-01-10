<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="main_content()" filter="trim">
<form class="form-horizontal" action='/admin' method="POST">
  <fieldset>
    <div id="legend">
      <legend class="">Admin Login</legend>
    </div>
    <div class="control-group">
      <label class="control-label" for="username">Username</label>
      <div class="controls">
        <strong>${g.player.name}</strong>
      </div>
    </div>

    <div class="control-group">
      <!-- Password-->
      <label class="control-label" for="password">Password</label>
      <div class="controls">
        <input type="password" id="password" name="password" placeholder="" class="input-xlarge">
      </div>
    </div>

    <div class="control-group">
      <!-- Button -->
      <div class="controls">
        <button class="btn btn-success">Login</button>
      </div>
    </div>
  </fieldset>
</form>
</%def>
