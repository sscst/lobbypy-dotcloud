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
  <%include file="handlebars.mako"/>
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
