function check_user(){
    if(current_user==null){
        window.alert("You need to sign In first.");
        element_handler.goto_link("/account-sign-in/");
    }
    else if(current_user.is_admin){
        element_handler.goto_link("/books-admin/")
    }
    else{
        element_handler.goto_link("/books-user/")
}
}