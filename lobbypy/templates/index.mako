<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="main_content()" filter="trim">
    <div class="row">
      <div class="span12">
        <div class="lobbylist">
          <div data-spy="scroll" data-target="#lobbylist" data-offset="0" class="lobbylist-scrollspy">
            <a href="/lobby">
            <div class="lobbyitem" id="butts">
              <span class="name">Hello world!</span>
              <span class="map">cp_badlands</span>
              <span class="players">6 / 12</span>
            </a>
            </div>
          </div>
        </div>
      </div>
    </div>
</%def>
