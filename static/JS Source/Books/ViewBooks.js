class book_handler{
    static update_init(){
        if(!edit_book_flag){
            return;
        }
        element_handler.get_id("isbn").value = current_selected_book.ISBN;
        element_handler.get_id("book-title").value = current_selected_book.title;
        element_handler.get_id("category").value = current_selected_book.category;
        let delimiter = ";"
        element_handler.get_id("authors").value = delimiter.join(current_selected_book.authors);
        element_handler.get_id("description").value = current_selected_book.description;
        element_handler.get_id("publisher").value = current_selected_book.publisher;
        element_handler.get_id("published-date").value = current_selected_book.published_date;
        element_handler.get_id("copy-id").value = current_selected_book_copy.ID;
        element_handler.get_id("isbn").value = current_selected_book_copy.details;
        element_handler.get_id("print-date").value = current_selected_book_copy.printed_date;
    }
}