<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="js()" filter="trim">
</%def>

<%def name="main_content()" filter="trim">
<form class="form-horizontal" action='/admin' method="POST">
  <fieldset>
    <div id="legend" style="margin: 0px 20px 0px 20px">
      <legend>Admin Login</legend>
    </div>
    <div class="control-group">
      <p class="control-label">Username</p>
      <div class="controls">
        <strong style="position: relative; bottom: -6px">${g.player.name}</strong>
      </div>
    </div>

    <div class="control-group">
      <label class="control-label" for="password">Password</label>
      <div class="controls">
        <input type="password" id="password" name="password" placeholder="" class="input-xlarge">
      </div>
    </div>

    <div class="control-group">
      <div class="controls">
        <button class="btn btn-success">Login</button>
      </div>
    </div>
  </fieldset>
</form>
</%def>
