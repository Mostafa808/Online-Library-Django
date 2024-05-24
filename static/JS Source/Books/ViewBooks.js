class book_handler{
    static update_init(){
        if(!edit_book_flag){
            return;
        }
        element_handler.get_id("isbn").value = current_selected_book.ISBN;
        element_handler.get_id("book-title").value = current_selected_book.title;
        element_handler.get_id("category").value = current_selected_book.category;
        
        element_handler.get_id("authors").value = current_selected_book.authors.join(";")
        element_handler.get_id("description").value = current_selected_book.description;
        element_handler.get_id("publisher").value = current_selected_book.publisher;
        element_handler.get_id("published-date").value = current_selected_book.published_date;
        element_handler.get_id("copy-id").value = current_selected_book_copy.ID;
        element_handler.get_id("isbn").value = current_selected_book_copy.details;
        element_handler.get_id("print-date").value = current_selected_book_copy.printed_date;
        element_handler.get_id("action-page-type").innerHTML = "Edit Book"
        element_handler.get_id("action-page-message").innerHTML = "If you entered a new ISBN that is not recorded in the database a new Book will be created otherwise books with this ISBN will be edited. The same applies for Copy ID for either creating a new copy or editing an existing one <br/><br/>"
    }
}