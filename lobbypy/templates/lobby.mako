<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="main_content()" filter="trim">
    <div class="row">
      <div class="span6">
        <div class="lobbydetails">
          <div class="lobby-name"><h2>Who's world is this?</h2></div>
          <div class="map-name"><h4>cp_badlands</h4></div>
          <div class="map-img"><img src="/static/images/cp_badlands.jpg" /></div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="span6">
        <div class="lobbydetails">
          <div class="option">Game type:</div>
          <div class="option-value">Control Points</div>
          <div class="option">Time limit:</div>
          <div class="option-value">30 minutes</div>
          <div class="option">Win limit:</div>
          <div class="option-value">5 wins</div>
        </div>
      </div>
      <div class="span6">
      </div>
    </div>
</%def>
