<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="main_content()" filter="trim">
    % if hellouser == 'Hello Anonymous!':
        <%
            loginorout = '/login'
            signinout = 'Sign in.'
        %>
    % else:
        <%
            loginorout = '/logout'
            signinout = 'Sign out.'
        %>
    % endif

    <p>${hellouser} <a href="${loginorout}">${signinout}</a></p>
</%def>
