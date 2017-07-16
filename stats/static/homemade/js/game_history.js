// The data should come in formatted the same way as the table will look
// The first row is the header
// The rest is the actual data
// The only formatting that really happens is that the date played comes in as
// POSIX timestamp, so it needs to be converted to a human readable date
function createGameHistoryTable(game_history) {

    var body = document.getElementById('stats');
    var table = document.createElement('table');

    // Get the header first
    var header = table.createTHead();
    var headerRow = header.insertRow(0);

    for (var i = 0; i < game_history[0].length; i++) {
        cell = headerRow.insertCell();
        cell.innerHTML = game_history[0][i];
    }

    // Now that the headers are set up, let's do each row
    for (var i = 1; i < game_history.length; i++) {
        var row = table.insertRow(i);
        for (var j = 0; j < game_history[i].length; j++) {
            var cell = row.insertCell(j);

            value = game_history[i][j];

            // If this is the date, it's a POSIX time stamp so format it
            if (j == 0) {
                // Server sends in seconds, javascript takes millis
                // Conversion is necessary
                var date = new Date(value * 1000);
                // Add one to month since it are 0 indexed
                var date_str = (date.getMonth() + 1) + "/" + date.getDate()
                        + "/" + date.getFullYear();
                value = date_str;
            }

            cell.innerHTML = value;
        }
    }

    body.appendChild(table);
}

createGameHistoryTable(game_history);