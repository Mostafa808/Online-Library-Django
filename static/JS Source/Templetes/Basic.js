/* The user have Username, Name, Email, Address, School Department, Date of Birth, Link to profile image, Password, Is Admin */
class user{
    /**
     * 
     * @param {string} username 
     * @param {string} password 
     * @param {string} full_name 
     * @param {string} email 
     * @param {string} address 
     * @param {string} birth_date 
     * @param {boolean} is_admin 
     * @param {string} profile_image_link
     * @param {string} website_view
     */
    constructor(username = "", password = "", full_name = "", email = "", address = "", birth_date = "", is_admin = false, profile_image_link = "", website_view = ""){
        this.username = username;
        this.password = password;
        this.full_name = full_name;
        this.email = email;
        this.address = address;
        this.birth_date = birth_date;
        this.is_admin = is_admin;
        this.profile_image_link = profile_image_link;
        this.website_view = website_view;
    }
}
class basic_memory{
    static set_object(key, value){
        var raw_data = JSON.stringify(value);
        if(raw_data){
            window.localStorage.setItem(key, raw_data);
            return true;
        }
        return false;
    }
    static get_object(key){
        var value = JSON.parse(window.localStorage.getItem(key));
        return value;
    }
    static del_object(key){
        window.localStorage.removeItem(key);
        return true;
    }
    static clear(){
        window.localStorage.clear()
        return true;
    }
    static view(){
        return window.localStorage
    }
}
class server_gate{
    static get_xml(){
    }
    static sign_in(username, password){
        
        fetch("/account-sign-in-action/",{
            "method":"POST",
            "body":JSON.stringify({"csrfmiddlewaretoken": this.getCookie("csrftoken"), "username" : username, "password":password})
        }).then(response=>response.json()).then(data=>{
            console.log('The server response: ',data)
            if(data["valid"]==false){
                window.alert(data["message"])
            }else{
                users_handler.set_user(data["user"]);
                element_handler.goto_link('/home/');
            }
        }).catch(error=>{
            console.error("The request failed: ". error)
        })
    }
    /**
     * @param {user} user 
     */
    static sign_up(user){
        
        fetch("/account-sign-up-action/",{
            "method":"POST",
            "body":JSON.stringify({"csrfmiddlewaretoken": this.getCookie("csrftoken"), "user" : user})
        }).then(response=>response.json()).then(data=>{
            console.log('The server response: ',data)
            if(data["valid"]==false){
                window.alert(data["message"])
            }else{
                users_handler.set_user(current_user);
                element_handler.goto_link("/home/")
            }
        }).catch(error=>{
            console.error("The request failed: ". error)
        })
    }
    static update_user(user, new_password=null){
        
        if (new_password!=null){
            user["new_password"]=new_password
        }
        fetch("/account-update-action/",{
            "method":"POST",
            "body":JSON.stringify({"csrfmiddlewaretoken": this.getCookie("csrftoken"), "user" : user})
        }).then(response=>response.json()).then(data=>{
            console.log('The server response: ',data)
            if(data["valid"]==false){
                window.alert(data["message"])
            }else{
                users_handler.set_user(data["user"]);
                element_handler.goto_link("/profile/");
            }
        }).catch(error=>{
            console.error("The request failed: ". error)
        })
    }
    static getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}
class element_handler{
    static basic(content, type, id=null, classes=[]){
        /**@type {HTMLElement} */
        var elem = document.createElement(type);
        if(content!=null){
            elem.textContent = content;
        }
        if(id!=null){
            if(!this.check_id(id)){
                elem.id = id;
            }
        }
        for (let class_name of classes) {
            elem.classList.add(class_name);
          }
        return elem;
    }
    static link(content, link, id=null, classes=[], click = false){
        var mylink = this.basic(content,'a', id, classes)
        mylink.href = link;
        if(click){
            var document_handler = document.getElementById("document-handler")
            document_handler.appendChild(mylink);
            mylink.click();
        }
        return mylink
    }
    /**
     * 
     * @param {string} href 
     * @param {string} id 
     * @param {[string]} classes 
     */
    static stylesheet(href, id = null, classes=[]){
        var mystyle = document.createElement('link');
        mystyle.rel = "stylesheet";
        mystyle.href = href;
        if(id!=null){
            mystyle.id = id;
        }
        for (let class_name of classes) {
            mystyle.classList.add(class_name);
        }
        return mystyle;
    }
    /**
     * @param {HTMLElement} element
     */
    static remove_children(element){
        element.innerHTML = '';
        return true;
    }
    static get_id(id){
        return document.getElementById(id);
    }
    static check_id(id){
        // is id exists?
        return !(this.get_id(id)==null);
    }
    static goto_link(link){
        this.link('',link,null,[],true)
    }
}
class users_handler{
    /** @param {user} newuser */
    static set_user(current_user){
        basic_memory.set_object("current_user",current_user);
    }
    /**
     * 
     * @param {user} oldUser 
     */
    static del_user(){
        basic_memory.del_object("current_user");
    }    
}
// form handler
class form_handler{
    /**
     * @param {HTMLInputElement} field 
     * @returns {boolean}
     */
    static is_required(field){
        return field.required;
    }
    /**
     * 
     * @param {HTMLInputElement} field 
     * @param {string} field_name 
     * @returns {boolean}
     */
    static validate_field(field, field_name){
        if(this.is_required(field) && !Boolean(field.value)){
            window.alert("Please enter: " + field_name);
            return false;
        }
        return true;
    }
    /**
     * 
     * @param {[HTMLInputElement]} fields 
     * @param {[string]} fields_names 
     */
    static validate_fields(fields, fields_names){
        for(let index=0; index < fields.length; index++){
            if(!this.validate_field(fields[index], fields_names[index])){
                return false;
            }
        }
        return true;
    }
}
// book details and book copy
class book_details {
    constructor(ISBN, title, authors, category, description, publisher, publishedDate) {
        this.ISBN = ISBN;
        this.title = title;
        this.authors = authors;
        this.category = category;
        this.description = description;
        this.publisher = publisher;
        this.publishedDate = new Date(publishedDate);
    }
}
class book_copy {
    constructor(ID, details, printedDate, isAvailable, borrowedBy, dueDate) {
        this.ID = ID;
        this.details = details;
        this.printed_date = new Date(printedDate);
        this.is_available = isAvailable;
        this.borrowed_by = borrowedBy;
        this.due_date = dueDate ? new Date(dueDate) : null;
    }
}

// global settings
var recursive = false;
//memory model
/** @type {user} */
var current_user = basic_memory.get_object("current_user");

// UI Functions
function scroll_manager(){
    var aside_node = document.querySelectorAll("aside")[0];
    var aside_bound = document.querySelectorAll("aside")[0].getBoundingClientRect();
    var article_bound = document.querySelectorAll("article")[0].getBoundingClientRect();
    
    aside_node.style.top = Math.max(article_bound.top,0).toString()+'px';
    aside_bound = document.querySelectorAll("aside")[0].getBoundingClientRect();
    article_bound = document.querySelectorAll("article")[0].getBoundingClientRect();
    
    if(aside_bound.bottom > article_bound.bottom){
        aside_node.style.top = (article_bound.bottom-aside_bound.bottom).toString()+'px';
    }
}

function reverse_arrow_icon(close, arrow){
    if (close==1){
         arrow.src = arrow.src.replace("right_arrow.png","left_arrow.png")
        arrow.alt='Left Arrow'
    }
    else if(close==0){
        arrow.src = arrow.src.replace("left_arrow.png","right_arrow.png")
        arrow.alt='Right Arrow'
    }
}
function show_hide_side(){
    var close;
    var side_node = document.querySelectorAll("aside")[0];
    var article_node = document.querySelectorAll("article")[0];
    let arrows = document.querySelectorAll("body > main > aside > img")

    if (arrows[0].src.includes("right_arrow.png")){
        close = 1;
        side_node.classList.add("side-close")
        article_node.classList.add("article-expand");
    }
    else if(arrows[0].src.includes("left_arrow.png")){
        close = 0;
        side_node.classList.remove("side-close")
        article_node.classList.remove("article-expand");
    }
    reverse_arrow_icon(close, arrows[0]);
}
/**
 * 
 * @param {HTMLElement} current_element 
 */
function handle_tap(current_element){
    if(current_element.id=="open-profile"){
        var profile_handler = document.getElementById("profile-handler");
        if(profile_handler.classList.contains("not-used")){
            profile_handler.classList.remove("not-used");
            profile_handler.classList.add("used");
            if(current_user==null){
                //view sign-in and sign-up
                element_handler.remove_children(profile_handler)                
                let sign_in = element_handler.basic("Sign-In", "button","sign-in");
                sign_in.type = 'button';
                sign_in.onclick = ()=> handle_tap(sign_in);
                profile_handler.appendChild(sign_in)

                let sign_up = element_handler.basic("Sign-Up", "button","sign-up");
                sign_up.type = 'button';
                sign_up.onclick = ()=> handle_tap(sign_up);
                profile_handler.appendChild(sign_up)
                
            }else{
                //view profile settengs
                element_handler.remove_children(profile_handler)
                let profile_settings = element_handler.basic("Profile Settings", "button","profile-settings");
                profile_settings.type = 'button';
                profile_settings.onclick = ()=> handle_tap(profile_settings);
                profile_handler.appendChild(profile_settings)

                let log_out = element_handler.basic("Log-Out", "button","log-out");
                log_out.type='button';
                log_out.onclick = ()=>handle_tap(log_out);
                profile_handler.appendChild(log_out);
            }
        }
        else{
            reset();
        }
    }
    else if(current_element.id =="log-out"){
        basic_memory.del_object('current_user');
        current_user = null;
        element_handler.goto_link('/home/');
    }
    else if(current_element.id =="profile-settings"){
        element_handler.goto_link('/profile/');
    }
    else if(current_element.id =="open-home"){
        element_handler.goto_link('/home/');
    }
    else if(current_element.id =="open-books"){
        element_handler.goto_link('/books/');
    }
    else if(current_element.id =="sign-in"){
        element_handler.goto_link('/account-sign-in/');
    }
    else if(current_element.id =="sign-up"){
        element_handler.goto_link('/account-sign-up/');
    }
    else{
        reset();
    }
}
// global reset
function reset(){
    let profile_handler = document.getElementById("profile-handler");
    if(profile_handler.classList.contains("used")){
        profile_handler.classList.remove("used");
        profile_handler.classList.add("not-used");
    }
}
// update profile image
function update_profile_image(){
    if(Boolean(current_user)){
        if (Boolean(current_user.profile_image_link)){
            document.getElementById("open-profile").src = current_user.profile_image_link;
        }
    }
}
// update website view
function update_website_view(){
    
    if(Boolean(current_user)){
        var main_head = document.querySelector("head");
        var current_user_view = document.getElementById("user-desired-view");
        var css_location = "/static/CSS Source/Templetes/";
        if(Boolean(current_user_view)){
            main_head.removeChild(current_user_view);
        }
        if (Boolean(current_user.website_view)){
            main_head.appendChild(
                element_handler.stylesheet(css_location+current_user.website_view+".css","user-desired-view")
            )
        }
    }
}
// update section
function pre_body_load(){
    update_website_view();
}
function post_load(){
    update_profile_image();
    window.onscroll = scroll_manager;
}
// test section
function alert_break(){
    window.alert("it is working.");
}