/*
  This javascript file handles click events from the client
  It will send requests to the server and will receive json response

*/
$(document).ready(function() {

  $("#search").click(function() {
    var checked = $("#check_box_value").is(":checked");
    var searchReq = ""; 
    var locality;
    var region; 
    var postal_code;
    var lat;
    var lng;

    if (checked) {
      if(navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(function(position) {

          locality = "using latlong";
          lat = position.coords.latitude;
          lng = position.coords.longitude;
          region = lat;
          postal_code = lng;
          console.log(region);
          searchReq = $.get("/sendRequest/" + locality + "," + region + "," + postal_code);
          build(searchReq, checked, lat, lng);
        });        
      };
    }
    else {
      locality = $("#locality").val();
      region = $("#region").val();
      postal_code = $("#postal_code").val();
      searchReq = $.get("/sendRequest/" + locality + ","+ region + ","+ postal_code);
      build(searchReq, checked, 0, 0);
    };
    // recieves the parameters from the website and sends them to the python server
    //var searchReq = $.get("/sendRequest/" + $("#locality").val() + ","+ $("#region").val() + ","+ $("#postal_code").val());
    
  });
  function build(searchReq, isChecked, latitude, longitude) {
    var map;
    searchReq.done(function(data) {
      var json = JSON.parse(data);
      console.log(json);
      var listLength = json['objects'].length;
      console.log(listLength);
      var myLatLng;
      for (var i = 0; i < listLength; ++i) {
        if (isChecked && i == 0) {
          myLatLng = {lat: latitude, lng: longitude};
        }
        else {
          myLatLng = {lat: json['objects'][i].lat, lng: json['objects'][i].long};
        };
        if (i == 0) {
          map = new google.maps.Map(document.getElementById('map'), {
            zoom: 13,
            center: myLatLng
          });
        };
        var marker = new google.maps.Marker({
            position: myLatLng,
            locality: json['objects'][i].locality,
            region: json['objects'][i].region,
            street_address: json['objects'][i].street_address,
            map: map,
            title: json['objects'][i].name
        });
        google.maps.event.addListener(marker,'click', function() {
          var title = this.title;
          var local = this.locality;
          var markerReq = $.get("/sendMarker/" + title + ","+ local);
          var businessId;
          
          markerReq.done(function(data) {
            var json = JSON.parse(data);
            console.log(json);
            businessId = json['businesses'][0].id;
            var s = document.createElement("script");
            s.async = true;
            s.onload = s.onreadystatechange = function(){
              getYelpWidget(businessId,"300","BLK","y","y","3");
            };
            s.src='http://chrisawren.com/widgets/yelp/yelpv2.js' ;
            var x = document.getElementsByTagName('script')[0];
            x.parentNode.insertBefore(s, x);
          });
        });
      };
    });
  }
});


