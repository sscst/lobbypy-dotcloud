<%def name="static_link(x)" filter="trim">
    ${url_for("static", filename=x)}
</%def>

<%def name="image_link(x)" filter="trim">
    ${static_link("/".join(("images", x)))}
</%def>

<%def name="css_link(x)" filter="trim">
    <link rel="stylesheet"
          type="text/css"
          href="${static_link("/".join(("styles", x)))}" />
</%def>

<%def name="js_link(x)" filter="trim">
    <script type="text/javascript" src="${static_link("/".join(("js", x)))}">
    </script>
</%def>

<%def name="jquery_link()" filter="trim">
    <script
     type="text/javascript"
     src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js">
    </script>
</%def>
