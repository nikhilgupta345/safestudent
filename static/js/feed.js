var id_list = [];
var eventDict = {};

$(document).ready(function() {
	Promise.resolve($.ajax("/api/v1/event/all"))
	.then(function(response) {
		if (response.status == "success") {
			var data = response.data;
			for (var i = 0; i < data.length; i++) {
				eventDict[data[i].event_id] = data[i].time;
			}
		}
	})
})

function updateTable() {
	Promise.resolve($.ajax("/api/v1/event/all"))
	.then(function(response) {
		if (response.status == "success") {
			var data = response.data;

			for (var i = 0; i < data.length; i++) {

				var name = data[i].student_first_name + " " + data[i].student_last_name;
				var scanner = data[i].scanner_name;
				var time = data[i].time;

				// If we don't already have the event, put it in the list
				var event_id = data[i].event_id;
				if (!(event_id in eventDict)) {
					var human = moment.utc(time).fromNow();

					var filled = "<tr><td>" + name + "</td><td>" + scanner + "</td><td " + "data-time=\"" + time + "\">" + human + "</td></tr>";
					$("#table-feed tbody").prepend(filled);
					eventDict[event_id] = time;
				}
			}
		}

		// Refresh times for all rows
		var tdList = $("#table-feed").find("td");
		tdList.each(function() {
			if ($(this).attr("data-time") !== undefined) {
				var time = $(this).attr("data-time");
				var human = moment.utc(time).fromNow();
				$(this).text(human);
			}
		});
	})
}

window.setInterval(function(){
	updateTable()
}, 2000);
