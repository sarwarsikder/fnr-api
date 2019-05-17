// var base_url = "http://127.0.0.1:8000";
var base_url = "http://192.168.1.10:8080";
$(function () {

    $('body').on("change", "#id_avatar", function () {
        if ($('#id_avatar').val() != "") {
            $('#temp_image').show('slow');
        }
        else {
            $('#temp_image').hide('slow');
        }
        readURL(this);
    });

});

function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#temp_image').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function requiredFieldValidator(requiredFields) {
    var message = '';
    for (var i = 0; i < requiredFields.length; i++) {
        var Id = requiredFields[i].fieldId;
        clog($('#' + Id).attr('type'))
        if ($('#' + Id).val() == '' || $('#' + Id).val() == null || $('#' + Id).val() == undefined) {
            message += "*" + requiredFields[i].message + " can't be blank" + "<br>";
            // valid = false;
        }
    }
    return message;
}

function clog(message) {
    console.log(message);
}

function isNotEmpty(value) {
    if (value != '' && value != null && value != undefined && value != 0) {
        return true;
    }
    return false;
}

function capitalize(text){
    return text.charAt(0).toUpperCase() + text.slice(1);
}