<div class="navbar navbar-fixed-top" id="#navbar" style="z-index: 1000">
  <div class="navbar-inner">
    <div class="container">
      <div style="position: relative;">
        <div style="position:absolute; top: 0px; left: 30px">
          <a href="/" class="brand">LobbyPy</a>
        </div>
      </div>
      <ul class="nav" style="margin-left: 135px">
        <li class="dropdown">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="icon-user"></i> Players <b class="caret"></b></a>
          <ul class="dropdown-menu">
            <li><a href="#"><i class="icon-group"></i> Recent Players</a></li>
            <li><a href="#"><i class="icon-heart"></i> Favor Player</a></li>
            <li><a href="#"><i class="icon-remove"></i> Avoid Player</a></li>
            <li class="divider"></li>
            <li><a href="#"><i class="icon-legal"></i> Report Player</a></li>
          </ul>
        </li>
        % if g.admin_authed:
        <li><a href="/admin"><i class="icon-cog"></i> Admin Dashboard</a></li>
        % endif
      </ul>
      <%include file="user_box.mako"/>
    </div>
  </div>
</div>
