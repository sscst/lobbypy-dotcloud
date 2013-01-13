function mouseHandler(e) {
	$(".picked").removeClass('picked');
	$(this).addClass('picked');	
};

function start() {
	$('#admin-lobby-list-container li').bind('click', mouseHandler);
	$('.admin-lobbyplayers').mousedown(function (evt) {
	  evt.stopImmediatePropagation();
	  return false;
	});
	$('.admin-lobbyplayers').selectable(); 
};
$(document).ready(start);

function GetCurrentLobbies() {
	
};

function GetCurrentPlayers() {

};