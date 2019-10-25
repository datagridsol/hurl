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

$(document).on('change','#user_type',function(){
    var user=$(this).val();
    if(user=='3')
    {
      $('#show_farmer').show();
    }
    else
    {
      $('#show_farmer').hide();
    }
  });
  $(document).on('change','.custom-file-input',function(){
    var img=$(this).val();
    $(this).next('.custom-file-label').html(img);
  });
  $(document).on('change','#state',function(){
    var state_id=$(this).val();
    var select_state='';
   
    if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length)
    {
      var select_state=$('#district_selct').val();;
    }
    if(state_id!='')
    {
      $.ajax({
        'method':'POST',
        'url':'/get_district/',
        'data': {'state_id':state_id},
        success: function(response){
          console.log(response);
          if(response.status=='success')
          {
            $('#district').prop('disabled',true);
            $('#district').html('<option  value="" selected="selected">---select---</option>');
            $.each(response.district_data, function (i, item) {
              if(select_state!='')
              {
                var selected=false;
                if(select_state==item.id)
                {
                  selected=true;
                }
                $('#district').append($('<option>', { 
                    value: item.id,
                    text : item.name,
                    selected:selected
                }));
              }
              else
              {
                $('#district').append($('<option>', { 
                    value: item.id,
                    text : item.name,
                    //selected:true
                }));
              }
                
            });
            $('#district').prop('disabled',false);
          }

        },
        error: function(xhr,status,errorThrown){
          toastr.error(xhr.responseText)
        },
      });
    }
  });

$(document).ready(function(){
  if($('#edituserForm').length || $('#editretailerForm').length || $('#editfarmerForm').length || $('#editwholeselerForm').length)
  {
    $('#state').trigger('change');
  }
  
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
    ignore: ":hidden",
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
        number: true,
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
      },
      email: {
        email: true,
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
        remote: {
          url: "/check_aadhar_card/",
          type: "post",
          data: {
            aadhar_no: function() {
              return $( "#aadhar_no" ).val();
            }
          }
        }
      },
      state: {
        required: true,
      },
      district: {
        required: true,
      },
      soil_card: {
        required: true,
      },
      land_area: {
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
      email: {
        email: "Please enter valid email address",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
        minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
        remote: "Aadhar card no already exists"
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please select a image",
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
            
            if(response.status=='success')
            {
              toastr.success('User added successfully').delay(10000);
              setTimeout(function(){  window.location.href="/get_user/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000);
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
    ignore: ":hidden",
    rules: {
      user_type: {
        required: true,
        
      },
      name: {
        required: true,
      },
      email: {
        email: true,
      },
      mobile_number: {
        required: true,
        minlength: 10,
        maxlength: 10,
        number: true,
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            },
            user_id: function() {
              return $( "#user_id_pk" ).val();
            }
          }
        }
      },
      aadhar_no: {
        required: true,
        minlength: 12,
        maxlength: 12,
        aadhar_no: {
          required: true,
          minlength: 12,
          maxlength: 12,
          remote: {
            url: "/check_aadhar_card/",
            type: "post",
            data: {
              aadhar_no: function() {
                return $( "#aadhar_no" ).val();
              },
              user_id: function() {
                return $( "#user_id_pk" ).val();
              }
            }
          }
        },
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
      email: {
        email: "Please enter valid email address",
      },
      mobile_number: {
        required: "Please enter a mobile number",
        minlength: "Your mobile number must consist of at least 10 digits",
        maxlength: "Your mobile number must consist of at max 10 digits",
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
      },
      aadhar_no: {
        required: "Please enter a aadhar no",
        minlength: "Your aadhar number must consist of at least 12 digits",
        maxlength: "Your aadhar number must consist of at max 12 digits",
        remote: "Aadhar card no already exists"
      },
      state: {
        required: "Please enter a state",
      },
      district: {
        required: "Please enter a district",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('edituserForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_user/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
           
            if(response.status=='success')
            {
              toastr.success('User updated successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_user/"; }, 2000);
              
            }
            else
            {
              toastr.error(response.msg).delay(10000)
              
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


    $("#retailerForm").validate({
   
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
        number: true,
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
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
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
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
      var userForm=document.getElementById('retailerForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_retailer/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
          
            if(response.status=='success')
            {
              toastr.success('Retailler added successfully').delay(10000);
              
              setTimeout(function(){ window.location.href="/get_retailer/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000)
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


    $("#editretailerForm").validate({
   
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
      var userForm=document.getElementById('editretailerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_retailer/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Retailler updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_retailer/"; }, 2000);
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
              toastr.success('Product Add successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_product/"; }, 2000);
              
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

   $("#editproductForm").validate({
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

    submitHandler: function() {
       var productForm=document.getElementById('editproductForm');
       var formData = new FormData(productForm);
       var product_id=$('#product_id').val();
        $.ajax({
          'method':'POST',
          'url':'/edit_product/'+product_id,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
           success: function(response){
            if(response.status=='success')
            {
              toastr.success('Product updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_product/"; }, 2000);
            }
            else
            {
              toastr.error('Something went wrong.').delay(10000);
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


   $("#farmerForm").validate({
   
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
        number: true,
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
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
      },
      soil_card: {
        required: true,
      },
      land_area: {
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
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
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
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please select a image",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('farmerForm');
       var formData = new FormData(userForm);
        $.ajax({
          'method':'POST',
          'url':'/add_farmer/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Farmer added successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_farmer/"; }, 2000);
              
            }
            else
            {
              toastr.error(response.msg).delay(10000)
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


    $("#editfarmerForm").validate({
   
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
      var userForm=document.getElementById('editfarmerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_farmer/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Farmer updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_farmer/"; }, 2000);
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

$("#wholesalerForm").validate({
   
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
        number: true,
        remote: {
          url: "/check_user_mobile/",
          type: "post",
          data: {
            mobile_number: function() {
              return $( "#mobile_number" ).val();
            }
          }
        }
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
      },
      soil_card: {
        required: true,
      },
      land_area: {
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
        number: "Please enter valid mobile number",
        remote: "Mobile number already exists"
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
      },
      soil_card: {
        required: "Please select a image",
      },
      land_area: {
        required: "Please select a image",
      }
    },
    submitHandler: function() {
      var userForm=document.getElementById('wholesalerForm');
       var formData = new FormData(userForm);
      
        $.ajax({
          'method':'POST',
          'url':'/add_wholesaler/',
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Wholesaler added successfully').delay(10000);
              setTimeout(function(){ window.location.href="/get_wholesaler/"; }, 2000);
            }
            else
            {
              toastr.error(response.msg).delay(10000)
            }

          },
          error: function(xhr,status,errorThrown){
            alert(xhr.responseText)
          },
        });
      return false;
    }
  });


$("#editwholeselerForm").validate({
   
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
      var userForm=document.getElementById('editwholeselerForm');
       var formData = new FormData(userForm);
       var user_id_pk=document.getElementById('user_id_pk').value;
        $.ajax({
          'method':'POST',
          'url':'/edit_wholesaler/'+user_id_pk,
          'data': formData,
          'cache':false,
          'contentType': false,
          'processData': false,
          success: function(response){
            if(response.status=='success')
            {
              toastr.success('Wholesaler updated successfully.').delay(10000);
              setTimeout(function(){ window.location.href="/get_wholesaler/"; }, 2000);
              
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


    $('.typeahead').typeahead(
    {  
        source: function(query, result)
        {
         $.ajax({
          url:"/search_city/",
          method:"GET",
          data:{query:query},
          //dataType:"json",
          success:function(data)
          {
           result($.map(data, function(item){
            return item;
           }));
          }
         })
        }
    }
  );
});