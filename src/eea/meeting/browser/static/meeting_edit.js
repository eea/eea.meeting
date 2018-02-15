$(document).ready(function() {
  var body = $('body');
  var $location_field = $("#formfield-form-widgets-location");
  var $geolocation_field = $("#formfield-form-widgets-IGeolocatable-geolocation");
  var WEBMINAR = 'webminar';  // a meeting type value
  var default_event_location = '';

  function webminar_mode() {
    // Hide Event Location and Event location on map fields
    $location_field.find('input').val("");  // We need location field empty.
    $location_field.hide();
    $geolocation_field.hide();
  }

  function non_webminar_mode() {
    // Show Event Location and Event location on map fields
    $location_field.show();
    $location_field.find('input').val(default_event_location);  // Autofill
    $geolocation_field.show();

    // Fix design: look like a required field (the custom validator solves behaviour)
    if($("label[for=form-widgets-location] span.required").length < 1) {
      $("label[for=form-widgets-location] span.formHelp").before("<span class='required'></span>");
    }
  }

  if($(body).hasClass("portaltype-eea-meeting") && $(body).hasClass("template-edit")) {
    var $meeting_type = $("#form-widgets-meeting_type");
    default_event_location = $location_field.find('input').val();

    if($meeting_type.val() == WEBMINAR) {
      webminar_mode();
    } else {
      non_webminar_mode();
    }

    $meeting_type.on('change', function() {
      if(this.value == WEBMINAR) {
        webminar_mode();
      } else {
        non_webminar_mode();
      }
    });

    // Keep lastest value of Event location as default
    var $location_field_input = $location_field.find('input');
    $location_field_input.on('focusout', function() {
      default_event_location = $location_field_input.val();
    });
  }
});
