function mouseHandler(e) {
	$(".picked").removeClass('picked');
	$(this).addClass('picked');	
};

function start() {
	$('#admin-lobby-list-container li').bind('click', mouseHandler);
};
$(document).ready(start);

function GetCurrentLobbies() {
	
};

function GetCurrentPlayers() {

};