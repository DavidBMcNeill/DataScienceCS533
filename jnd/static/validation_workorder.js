/***************************/
//@Author: Adrian "yEnS" Mato Gondelle & Ivan Guardado Castro
//@website: www.yensdesign.com
//@email: yensamg@gmail.com
//@license: Feel free to use it, but keep this credits please!                    
/***************************/

$(document).ready(function(){
    //global vars
   // alert("hello");
    var form = $("#registerForm");
    var name = $("#name");
    var own_mobile_no = $("#own_mobile_no");
   
    
    
    //On blur
    name.blur(validateName);
    own_mobile_no.blur(validateOwnMobileNo);
     
    //On key press
    
    name.keyup(validateName);
    own_mobile_no.keyup(validateOwnMobileNo);
    // phone.keyup(validatePass2);      
    
    //On Submitting
    form.submit(function(){
        if(validateName() & validateOwnMobileNo()  )
            return true
        else
        {
            alert('Error! mandatory information not filled.');
            return false;
        }    
    });
    
    //validation functions
    function validateEmail(){
        //testing regular expression
        var a = $("#email").val();
        var filter = /^[a-zA-Z0-9]+[a-zA-Z0-9_.-]+[a-zA-Z0-9_-]+@[a-zA-Z0-9]+[a-zA-Z0-9.-]+[a-zA-Z0-9]+.[a-z]{2,4}$/;
        //if it's valid email
        if(filter.test(a)){
            email.removeClass("input-single-error");
            return true;
        }
        //if it's NOT valid
        else{
            email.addClass("input-single-error");
            return false;
        }
    }
    
    function validateName(){
        //if it's NOT valid
        if(name.val().length < 4){
            name.addClass("input-single-error");  
			
            return false;
        }
        //if it's valid
        else{
            name.removeClass("input-single-error");
            return true;
        }
    }
    function validateOwnMobileNo(){
        //if it's NOT valid
        if(own_mobile_no.val().length < 2){
            own_mobile_no.addClass("error-103");
			document.getElementById("own_mobile_no").focus();
            return false;
        }
        //if it's valid
        else{
            own_mobile_no.removeClass("error-103");
            return true;
        }
    }
    
    function validatePhone(){
        //if it's NOT valid
        if(phone.val().length < 4){
            phone.addClass("input-single-error");
            return false;
        }
        //if it's valid
        else{
            phone.removeClass("input-single-error");
            return true;
        }
    }
   
   
});