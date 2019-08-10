
$(function() {
    $('.login').click(function() {
    	console.log("in login");
        $.ajax({
            url: 'http://127.0.0.1:5000/login',
            data: $('.form-signin').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('.register').click(function() {
    	console.log("in register");
        $.ajax({
            url: 'http://127.0.0.1:5000/registration',
            data: $('.form-signup').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});