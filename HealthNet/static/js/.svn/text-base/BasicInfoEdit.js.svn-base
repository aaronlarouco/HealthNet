$(document).ready(function() {
  setupBasicInfoEdit();
});

function setupBasicInfoEdit() {
  var token = $('input[name=\"csrfmiddlewaretoken\"]');
  var userHolder = document.getElementById('username-holder');
  var username = userHolder.getAttribute("username");

  $("#basic-info-edit-button").click(function(e) {
    $.ajax({
        url: "/profiles/" + username + "/editbasicinfo",
        type: "POST",
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#basic-form-content').html(data.html);
          forceInputSetup(document.getElementById("basic-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#basic-info-submit").click(function(e) {
    if ($('#edit-basic-info-form')[0].checkValidity() == true) {
      e.preventDefault();

      var phoneNumber = $('#phoneNumber-field');
      var heightFeet = $('#heightFeet-field');
      var heightInches = $('#heightInches-field');
      var weight = $('#weight-field');
      var street = $('#street-field');
      var city = $('#city-field');
      var state = $('#state-field');
      var zipcode = $('#zipcode-field');
      $.ajax({
          url: "/profiles/" + username + "/savebasicinfo",
          type: "POST",
          data: {
              client_response: "",
              csrfmiddlewaretoken: token.val(),
              phoneNumber: phoneNumber.val(),
              heightFeet: heightFeet.val(),
              heightInches: heightInches.val(),
              weight: weight.val(),
              street: street.val(),
              city: city.val(),
              state: state.val(),
              zipcode: zipcode.val()
          },
          success: function (data) {
            document.getElementById("basic-info-content").innerHTML = "";
            $('#basic-info-content').html(data.html);
            $('#jpop-faded-bg').click();

            setTimeout(function() {
              document.getElementById('basic-form-content').innerHTML = "";
            }, 200);
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });

  $("#medical-info-edit-button").click(function(e) {
    $.ajax({
        url: "/profiles/" + username + "/editmedicalinfo",
        type: "POST",
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#medical-form-content').html(data.html);
          forceInputSetup(document.getElementById("medical-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#medical-info-submit").click(function(e) {
    if ($('#edit-medical-info-form')[0].checkValidity() == true) {
      e.preventDefault();

      var insuranceCompany = $('#insuranceCompany-field');
      var insuranceId = $('#insuranceId-field');
      var hospitalPref = $('#hospitalPref-field');
      $.ajax({
          url: "/profiles/" + username + "/savemedicalinfo",
          type: "POST",
          data: {
              client_response: "",
              csrfmiddlewaretoken: token.val(),
              insuranceCompany: insuranceCompany.val(),
              insuranceId: insuranceId.val(),
              hospitalPref: hospitalPref.val()
          },
          success: function (data) {
            document.getElementById("medical-info-content").innerHTML = "";
            $('#medical-info-content').html(data.html);
            $('#jpop-faded-bg').click();

            setTimeout(function() {
              document.getElementById('medical-form-content').innerHTML = "";
            }, 200);
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });
}

function setupBasicInfoEditPeek() {
  var token = $('input[name=\"csrfmiddlewaretoken\"]');
  var userHolder = document.getElementById('peek-username');
  var username = userHolder.getAttribute("username");

  $("#basic-info-edit-button").click(function(e) {
    $.ajax({
        url: "/profiles/" + username + "/editbasicinfo",
        type: "POST",
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#basic-form-content').html(data.html);
          forceInputSetup(document.getElementById("basic-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#basic-info-submit").click(function(e) {
    if ($('#edit-basic-info-form')[0].checkValidity() == true) {
      e.preventDefault();

      var phoneNumber = $('#phoneNumber-field');
      var heightFeet = $('#heightFeet-field');
      var heightInches = $('#heightInches-field');
      var weight = $('#weight-field');
      var street = $('#street-field');
      var city = $('#city-field');
      var state = $('#state-field');
      var zipcode = $('#zipcode-field');
      $.ajax({
          url: "/profiles/" + username + "/savebasicinfo",
          type: "POST",
          data: {
              client_response: "",
              csrfmiddlewaretoken: token.val(),
              phoneNumber: phoneNumber.val(),
              heightFeet: heightFeet.val(),
              heightInches: heightInches.val(),
              weight: weight.val(),
              street: street.val(),
              city: city.val(),
              state: state.val(),
              zipcode: zipcode.val()
          },
          success: function (data) {
            document.getElementById("basic-info-content").innerHTML = "";
            $('#basic-info-content').html(data.html);
            $('#jpop-faded-bg').click();

            setTimeout(function() {
              document.getElementById('basic-form-content').innerHTML = "";
            }, 200);
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });

  $("#medical-info-edit-button").click(function(e) {
    $.ajax({
        url: "/profiles/" + username + "/editmedicalinfo",
        type: "POST",
        data: {
            client_response: "",
            csrfmiddlewaretoken: token.val()
        },
        success: function (data) {
          $('#medical-form-content').html(data.html);
          forceInputSetup(document.getElementById("medical-form-content"));
        },
        error: function (jqXHR, textStatus, errorThrown) {
        }
    });
  });
  $("#medical-info-submit").click(function(e) {
    if ($('#edit-medical-info-form')[0].checkValidity() == true) {
      e.preventDefault();

      var insuranceCompany = $('#insuranceCompany-field');
      var insuranceId = $('#insuranceId-field');
      var hospitalPref = $('#hospitalPref-field');
      $.ajax({
          url: "/profiles/" + username + "/savemedicalinfo",
          type: "POST",
          data: {
              client_response: "",
              csrfmiddlewaretoken: token.val(),
              insuranceCompany: insuranceCompany.val(),
              insuranceId: insuranceId.val(),
              hospitalPref: hospitalPref.val()
          },
          success: function (data) {
            document.getElementById("medical-info-content").innerHTML = "";
            $('#medical-info-content').html(data.html);
            $('#jpop-faded-bg').click();

            setTimeout(function() {
              document.getElementById('medical-form-content').innerHTML = "";
            }, 200);
          },
          error: function (jqXHR, textStatus, errorThrown) {
          }
      });
    }
  });
}
