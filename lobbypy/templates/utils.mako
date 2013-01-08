<%def name="static_link(x)" filter="trim">
    ${url_for("static", filename=x)}
</%def>

<%def name="image_link(x)" filter="trim">
    ${static_link("/".join(("images", x)))}
</%def>

<%def name="css_link(x)" filter="trim">
    <link rel="stylesheet"
          type="text/css"
          href="${static_link(x)}" />
</%def>

<%def name="js_link(x)" filter="trim">
    <script type="text/javascript" src="${static_link(x)}">
    </script>
</%def>

<%def name="jquery_link()" filter="trim">
    <script
     type="text/javascript"
     src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js">
    </script>
</%def>

<%def name="socketio_link()" filter="trim">
    <script
     type="text/javascript"
     src="/static/socket.io.min.js">
    </script>
</%def>
