$(document).ready(function() {
  var body = $('body');
  var $location_field = $("#formfield-form-widgets-location");
  var $geolocation_field = $("#formfield-form-widgets-IGeolocatable-geolocation");

  function webminar_mode() {
    // Hide Event Location and Event location on map fields
    $location_field.hide();
    $geolocation_field.hide();
  }

  function non_webminar_mode() {
    // Show Event Location and Event location on map fields
    $location_field.show();
    $geolocation_field.show();
  }

  if($(body).hasClass("portaltype-eea-meeting") && $(body).hasClass("template-edit")) {
    var $meeting_type = $("#form-widgets-meeting_type");

    if($meeting_type.val() == 'webminar') {
      webminar_mode();
    } else {
      non_webminar_mode();
    }

    $meeting_type.on('change', function() {
      if(this.value == 'webminar') {
        webminar_mode();
      } else {
        non_webminar_mode();
      }
    });
  }
});
