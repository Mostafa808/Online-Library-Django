function profile_handle_buttons(current_element){
    if(current_element.id=="save"){
        var full_name = element_handler.get_id("full-name");
        var email = element_handler.get_id("email");
        var birth_date = element_handler.get_id("birth-date");
        var address =  element_handler.get_id("address");
        var is_admin = element_handler.get_id("is_admin");
        var profile_image = element_handler.get_id("profile-image");
        var website_view = element_handler.get_id("website-view");
        if(Boolean(full_name.value)) current_user.full_name = full_name.value;
        if(Boolean(email.value)) current_user.email = email.value;
        current_user.birth_date = new Date(birth_date.value).toISOString().split("T")[0];
        if(Boolean(address.value)) current_user.address = address.value;
        current_user.is_admin = is_admin.checked;
        if(Boolean(profile_image.value)) current_user.profile_image_link = profile_image.value;
        
        current_user.website_view = website_view.value;

        server_gate.update_user(current_user);

    }else if(current_element.id=="cancel"){
        element_handler.goto_link("/profile/");
    }
    else if(current_element.id=="change-password"){
        element_handler.goto_link("/profile-change-password/");
    }
    else if(current_element.id=="save-password"){
        var oldPassword = element_handler.get_id("your-old-password");
        var newPassword = element_handler.get_id("new-password");
        var confirmPassword = element_handler.get_id("confirm-password");
        if(newPassword.value!=confirmPassword.value){
            window.alert("The Password confirmation is wrong")
            return
        }
        test_user = current_user
        test_user["password"]=oldPassword.value
        server_gate.update_user(test_user, newPassword.value)
    }
    else if(current_element.id == "sign-in-button"){
        var username = element_handler.get_id("user-name");
        var password = element_handler.get_id("password");
        if(!form_handler.validate_fields([username, password],
            ["username","password"])){
                return false;
        }
        server_gate.sign_in(username.value, password.value)
    }
    else if(current_element.id == "create-account"){
        element_handler.goto_link("/account-sign-up/");
    }
    else if(current_element.id == "have-account"){
        element_handler.goto_link("/account-sign-in/");
    }
    else if(current_element.id=="sign-up-button"){
        var current_user_name = element_handler.get_id("user-name");
        var password = element_handler.get_id("password");
        var full_name = element_handler.get_id("full-name");
        var email = element_handler.get_id("email");
        var birth_date = element_handler.get_id("birth-date");
        var address =  element_handler.get_id("address");
        var is_admin = element_handler.get_id("is_admin");
        if(!form_handler.validate_fields([current_user_name, password, full_name, email, birth_date, address, is_admin],
            ["username","password","full name", "email", "birth date", "address", "is admin"])){
                return false;
        }

        current_user = new user();
        if(Boolean(current_user_name.value)) current_user.username = current_user_name.value;
        if(Boolean(password.value)) current_user.password = password.value;
        if(Boolean(full_name.value)) current_user.full_name = full_name.value;
        if(Boolean(email.value)) current_user.email = email.value;
        current_user.birth_date = new Date(birth_date.value).toISOString().split('T')[0];
        if(Boolean(address.value)) current_user.address = address.value;
        current_user.is_admin = is_admin.checked;
        
        server_gate.sign_up(current_user)
        
        
    }
}
function current_data(){
    var full_name = element_handler.get_id("full-name");
    var email = element_handler.get_id("email");
    var birth_date = element_handler.get_id("birth-date");
    var address =  element_handler.get_id("address");
    var is_admin = element_handler.get_id("is_admin");
    var profile_image = element_handler.get_id("profile-image");
    var website_view = element_handler.get_id("website-view");

    if(Boolean(current_user.full_name)) full_name.placeholder = current_user.full_name;
    if(Boolean(current_user.email)) email.placeholder = current_user.email;
    birth_date.valueAsDate = new Date(current_user.birth_date);
    if(Boolean(current_user.address)) address.placeholder = current_user.address;
    is_admin.checked = current_user.is_admin;
    if(Boolean(current_user.profile_image_link)) profile_image.placeholder = current_user.profile_image_link;
    if(Boolean(current_user.website_view)) website_view.value = current_user.website_view;
}
