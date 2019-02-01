$(document).ready(function() {
  var body = $('body');
  var $location_field = $("#formfield-form-widgets-location");
  var $geolocation_field = $("#formfield-form-widgets-IGeolocatable-geolocation");
  var WEBMINAR = 'webinar';  // a meeting type value
  var default_event_location = '';

  var $allow_register_start_field = $("#formfield-form-widgets-allow_register_start");
  var $allow_register_end_field = $("#formfield-form-widgets-allow_register_end");
  var $epass_required_field = $("#form-widgets-need_e_pass input");

  function allow_register_mode() {
    $allow_register_start_field.show();
    $allow_register_end_field.show();
  }

  function non_allow_register_mode() {
    $allow_register_start_field.hide();
    $allow_register_end_field.hide();
  }

  function webinar_mode() {
    // Hide Event Location and Event location on map fields
    $location_field.find('input').val("");  // We need location field empty.
    $location_field.hide();
    $geolocation_field.hide();
    $epass_required_field.attr("checked", false);
    $epass_required_field.attr("disabled", true);
  }

  function non_webinar_mode() {
    // Show Event Location and Event location on map fields
    $location_field.show();
    $location_field.find('input').val(default_event_location);  // Autofill
    $geolocation_field.show();
    $epass_required_field.attr("disabled", false);

    // Fix design: look like a required field (the custom validator solves behaviour)
    if($("label[for=form-widgets-location] span.required").length < 1) {
      $("label[for=form-widgets-location] span.formHelp").before("<span class='required'></span>");
    }
  }

  if(($(body).hasClass("portaltype-eea-meeting") && $(body).hasClass("template-edit")) ||
     ($(body).hasClass("portaltype-folder") && $(body).hasClass("template-eea-meeting"))) {
    var $meeting_type = $("#form-widgets-meeting_type");
    default_event_location = $location_field.find('input').val();

    if($meeting_type.val() == WEBMINAR) {
      webinar_mode();
    } else {
      non_webinar_mode();
    }

    $meeting_type.on('change', function() {
      if(this.value == WEBMINAR) {
        webinar_mode();
      } else {
        non_webinar_mode();
      }
    });

    // Keep latest value of Event location as default
    var $location_field_input = $location_field.find('input');
    $location_field_input.on('focusout', function() {
      default_event_location = $location_field_input.val();
    });

    // Show From and To only if Allow registration is checked
    var $allow_register = $("input#form-widgets-allow_register-0");
    if($allow_register.prop("checked")) {
      allow_register_mode();
    } else {
      non_allow_register_mode();
    }

    $allow_register.on("change", function() {
      if($(this).prop("checked")) {
        allow_register_mode();
      } else {
        non_allow_register_mode();
      }
    });
  }
});
