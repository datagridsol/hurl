(function ($) {
    $.fn.buttonLoader = function (action) {
        var self = $(this);
        //start loading animation
        if (action == 'start') {
            if ($(self).attr("disabled") == "disabled") {
                e.preventDefault();
            }
            //disable buttons when loading state
            $('.has-spinner').attr("disabled", "disabled");
            $(self).attr('data-btn-text', $(self).text());
            //binding spinner element to button and changing button text
            $(self).html('<span class="spinner"><i class="fas fa-spinner fa-spin"></i></span>Loading');
            $(self).addClass('active');
        }
        //stop loading animation
        if (action == 'stop') {
            $(self).html($(self).attr('data-btn-text'));
            $(self).removeClass('active');
            //enable buttons after finish loading
            $('.has-spinner').removeAttr("disabled");
        }
    }
})(jQuery);

$(document).ready(function(){
  toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }
  $("#signinForm").validate({
    rules: {
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true
      },
      password: {
        required: true,
      }
    },
    messages: {
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      password: {
        required: "Please provide a password",
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    submitHandler: function() {
        var btn = $('#submitBtn');
        $(btn).buttonLoader('start');
        $.ajax({
          'method':'POST',
          'url':'/user_login/',
          'data': $('#signinForm').serialize(),
          success: function(response){
            if(response.status=='success')
            {
              $(btn).buttonLoader('stop')
              toastr.success('Login successfully.')
              window.location.href="/dashboard/";
            }
            else
            {
              $(btn).buttonLoader('stop')
              toastr.error(response.msg)
            }

          },
          error: function(xhr,status,errorThrown){
            toastr.error(xhr.responseText)
            $(btn).buttonLoader('stop')
          },
        });
      return false;
    }
  });

  $("#userForm").validate({
    rules: {
      user_type: {
        required: true,
        
      },
      name: {
        required: true,
      },
      username: {
        required: true,
      },
      aadhar_no: {
        required: true,
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      }
    },
    messages: {
      user_type: {
        required: "Please enter a user type",
      },
      name: {
        required: "Please enter a name",
      },
      username: {
        required: "Please enter a mobile number",
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    errorPlacement: function(error, element) {
      error.appendTo(element.parent("div"));
    },
    // submitHandler: function() {
    //     $.ajax({
    //       'method':'POST',
    //       'url':'/hurlapp/add_user/',
    //       'data': $('#userForm').serialize(),
    //       success: function(response){
    //         if(response.status=='success')
    //         {
    //           window.location.href="/hurlapp/add_user/";
    //         }
    //         else
    //         {
    //           alert(response.msg);
    //         }

    //       },
    //       error: function(xhr,status,errorThrown){
    //         alert(xhr.responseText)
    //       },
    //     });
    //   return false;
    // }
  });
      
});