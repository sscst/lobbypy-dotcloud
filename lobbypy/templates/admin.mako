<%inherit file="base.mako"/>
<%namespace name="utils" file="utils.mako"/>

<%def name="js()" filter="trim">
</%def>

<%def name="main_content()" filter="trim">
<div id="legend" style="margin: 0px 20px 0px 20px">
  <legend>Admin Dashboard</legend>
</div>
<div class="row">
  <div class="span6">
    <div class="accordion" id="accordion2">
      <div class="accordion-group">
        <div class="accordion-heading">
          <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
            Lobby
          </a>
        </div>
        <div id="collapseOne" class="accordion-body collapse in">
          <div class="accordion-inner">
            Lobby data
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</%def>
