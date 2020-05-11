function validateSignupForm(){
    var form_ = document.forms["signupform"];
    if(form_["first_name"].value === ""){
        alert("First Name must be filled");
        return false;
    }
    if(form_["last_name"].value === ""){
        alert("Last Name must be filled");
        return false;
    }
    if(form_["email"].value === ""){
        alert("email cannot be empty");
        return false;
    }
    var emailID = form_["email"].value;
    atpos = emailID.indexOf("@");
    dotpos = emailID.lastIndexOf(".");
    if (atpos < 1 || ( dotpos - atpos < 2 )) {
        alert("Please enter correct email ID");
        return false;
     }
    if(form_["password"].value == ""){
        alert("pasword cannot be empty");
        return false;
    }
    else if(form_["password"].value.length < 8) {
        alert("Minimum 8 characters requires for password!");
        return false;
    }
    if(form_["confirm password"].value == ""){
        alert("Confirm your password please");
        return false;
    }
    if(form_["password"].value != form_["confirm password"].value){
        alert("Your Password and Confirm Password must match");
        return false;
    }
    if(form_["role"].value == ""){
        alert("You must select a role");
        return false;
    }
    return true;
}
function validateLoginForm(){
    var form_ = document.forms["loginform"];
    if(form_["email"].value == ""){
        alert("email cannot be empty");
        return false;
    }
    var emailID = form_["email"].value;
    atpos = emailID.indexOf("@");
    dotpos = emailID.lastIndexOf(".");
    if (atpos < 1 || ( dotpos - atpos < 2 )) {
        alert("Please enter correct email ID");
        return false;
     }
    if(form_["password"].value == ""){
        alert("pasword cannot be empty");
        return false;
    }
    if(form_["role"].value == ""){
        alert("You must select a role");
        return false;
    }
    return true;
}