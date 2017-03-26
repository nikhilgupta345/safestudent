var selectedInfoWindow;

function initMap() {
	var data = {};
	if (typeof student_id !== "undefined") {
		data["student_id"] = student_id;
	}

	console.log(data);
	var ajaxURL = "/api/v1/get_student_info";
	Promise.resolve($.get(ajaxURL, data))
	.then(function(res) {
		if (res.status === "error") {
			return Promise.reject(res.message);
		}

		console.log(res);
		var map = new google.maps.Map(document.getElementById('map'));

		//create empty LatLngBounds object
		var bounds = new google.maps.LatLngBounds();
		var infowindow = new google.maps.InfoWindow();    

		var colors = ["red", "blue", "darkgreen", "orange", "paleblue", "pink", "purple", "yellow", "green", "brown"];
		var colorHex = ["#ff0000", "#0000ff", "#1a5101", "#e29506", "#06a3e2", "#f23cd6", "#6c0f91", "#f2eb1f", "#51352c"]
		var markerBaseURL = "/media/images/markers/";

		for (var i in res.data.students) {
			var student = res.data.students[i];
			var eventTraceCoordinates = [];
			for (var j in student.events) {
				var event = student.events[j];

				var marker = new google.maps.Marker({
				    position: new google.maps.LatLng(event.latitude, event.longitude),
				    map: map,
				    animation: google.maps.Animation.DROP,
				    icon: markerBaseURL + colors[i % colors.length] + "_Marker" + student.name[0].toUpperCase() + ".png"
				});

				eventTraceCoordinates.push(new google.maps.LatLng(event.latitude, event.longitude));
				addInfoWindow(marker, student, event)
				//extend the bounds to include each marker's position
				bounds.extend(marker.position);
			}

			var flightPath = new google.maps.Polyline({
				path: eventTraceCoordinates,
				strokeColor: colorHex[i % colors.length],
				strokeOpacity: 1.0,
				strokeWeight: 2
			});
			flightPath.setMap(map);
		}

		//now fit the map to the newly inclusive bounds
		map.fitBounds(bounds);

		//(optional) restore the zoom level after the map is done scaling
		/*var listener = google.maps.event.addListener(map, "idle", function () {
		    map.setZoom(12);
		    google.maps.event.removeListener(listener);
		});*/

	})
	.catch(function(e) {
		console.error(e);
	})
}

function addInfoWindow(marker, student, event) {
	var d = Date(event.timestamp);
	var infowindow = new google.maps.InfoWindow({
		content: "<b>" + student.name + "</b> checked in to <b>" + event.name + "</b> at <b>" + d + "</b>"
	});

	marker.addListener('click', function() {
		if (typeof selectedInfoWindow !== 'undefined') {
			selectedInfoWindow.close();
		}
		
		infowindow.open(marker.get('map'), marker);
		selectedInfoWindow = infowindow;
	});
}