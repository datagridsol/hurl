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
        number: true,
        minlength: 10,
        maxlength: 10
        
      },
      password: {
        required: true,
      }
    },
    messages: {
      mobile_number: {
        required: "Please enter a mobile number",
        number: "Please enter valid mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits"
       
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
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
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
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('userForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_user/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            alert("response")
            alert(response)
            if(response.status=='success')
            {
              toastr.success('user Created successfully.').delay(10000)
              window.location.href="/get_user/";
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

  $("#edituserForm").validate({
   
    rules: {
      user_type: {
        required: true,
        
      },
      name: {
        required: true,
      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
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
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
         minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('userForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/edit_user/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            alert("response")
            alert(response)
            if(response.status=='success')
            {
              toastr.success('user Created successfully.').delay(10000)
              window.location.href="/get_user/";
            }
            else
            {
              alert(response.msg);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });
   
   $("#productForm").validate({
    rules: {
      product_name: {
        required: true,
        
      },
      product_price: {
        required: true,
        number: true
      }
    },
    messages: {
      product_name: {
        required: "Please enter a name",
      },
      product_price: {
        required: "Please enter a price",
        number: "Please enter valid price"
      }
    },
<<<<<<< HEAD
    submitHandler: function() {
       var productForm=document.getElementById('productForm');
       var formData = new FormData(productForm);
        $.ajax({
          'method':'POST',
          'url':'/add_product/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
           success: function(response){
            if(response.status=='success')
            {
              toastr.success('Product Add successfully.').delay(10000)
              window.location.href="/get_product/";
            }
            else
            {
              alert(response.msg);
            }
=======
    // submitHandler: function() {
    //     $.ajax({
    //       'method':'POST',
    //       'url':'/add_user/',
    //       'data': $('#userForm').serialize(),
    //       success: function(response){
    //         if(response.status=='success')
    //         {
    //           window.location.href="/add_user/";
    //         }
    //         else
    //         {
    //           alert(response.msg);
    //         }
>>>>>>> 445bd947136d1b34093e0704878db473e79ba5ee

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });

});