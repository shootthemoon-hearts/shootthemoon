function createGameHistoryTable(game_history){

    var body = document.getElementById('stats');
    var table  = document.createElement('table');

    // Get the header first
    var header = table.createTHead();
    var headerRow = header.insertRow(0);

    // Get first item of history to see what the headers should be
    var item0 = game_history[0];
    var i = 0;
    for (var key in item0) {
    	var cell = headerRow.insertCell(i);
    	cell.innerHTML = key;

    	i++;
    }
    
    // Now that the headers are set up, let's do each row
    for (var i = 0; i < game_history.length; i++) {
    	// i + 1 since the header row already exists
    	var row = table.insertRow(-1);
    	var j = 0;
    	for (var key in game_history[i]) {
    		var cell = row.insertCell(j);
    		cell.innerHTML = game_history[i][key];
    		j++;
    	}
    	i++;
    }

    body.appendChild(table);
}
createGameHistoryTable(game_history);