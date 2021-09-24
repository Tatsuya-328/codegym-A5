/* Google Maps API繧ｵ繝ｳ繝励Ν */

function initialize() {
    var latlng = new google.maps.LatLng(35.630442,139.882951);
    var opts = {
      zoom: 14,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map_canvas"), opts);
  
    var m_latlng1 = new google.maps.LatLng(35.632605,139.88132);
    var marker1 = new google.maps.Marker({
      position: m_latlng1,
      map: map,
      icon: "./img/car.png"
    });
  
    var m_latlng2 = new google.maps.LatLng(35.625663,139.884238);
    var marker2 = new google.maps.Marker({
      position: m_latlng2,
      map: map
    });
  }