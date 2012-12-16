<%namespace name="utils" file="utils.mako"/>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  ${utils.socketio_link()}
  ## ${utils.css_link("styles.css")}
  ## ${next.css() | trim}
  <title>LobbyPy</title>
</head>
<body>
  <div id="container">
    <div id="body">
      ## nav bar i guess
      <div id="main_content">
        ${next.main_content() | trim}
      </div> <!-- div main_content -->
    </div> <!-- div body -->
  </div> <!-- div container -->
</body>
</html>
