function apply_googlebooks_info(isbn, successCallback) {
    // var isbn = $('input#isbn13').val();
    console.log('requesting isbn' + isbn);

    // show the loader
    $('img#cover_img').attr('src', '../static/img/loader.gif');

    $.getJSON("https://www.googleapis.com/books/v1/volumes?q=isbn:" + isbn, function(data){
        console.log("got data", data);

        if (data.totalItems === 0) {
            console.warn('got nothing from Google Books with isbn' + isbn);
        } else {
            if (data.totalItems !== 1) {
                // TODO
                console.warn('Got multiple items, defaulting to the first one...');
            }
            book_info = data.items[0].volumeInfo;
            var thumbnail_url = book_info.imageLinks.thumbnail;

            $('input#title').val(book_info.title);
            $('input#description').val(book_info.description);
            $('input#thumbnail_url').val(thumbnail_url).trigger('blur');

            successCallback();
        }
    });
}

function got_new_isbn(){
    var isbn_input = $(this).val();
    // remove dashes & make sure X's are uppercase
    // this makes isbn.js happy
    isbn_input = isbn_input.replace(/-/g,'');
    isbn_input = isbn_input.replace(/x/g,'X');

    var parsed_isbn = ISBN.parse(isbn_input);
    // if isbn is valid, request the isbn13 from google books
    console.log('parsed_isbn', parsed_isbn);

    // add error class as default. only on success is it removed.
    $(this).addClass('error');

    if (parsed_isbn) {
        if ((parsed_isbn.check === parsed_isbn.check10 && parsed_isbn.isIsbn10) ||
            (parsed_isbn.check === parsed_isbn.check13 && parsed_isbn.isIsbn13)) {
            // Reset the form to isbn13 value
            $(this).val(ISBN.asIsbn13(isbn_input));
            // Fetch & apply info from Google Books
            apply_googlebooks_info($(this).val(), function() {
                // remove error class on success
                $('input#isbn13').removeClass('error');
            });
        }
    } else {
        console.warn('bad isbn');
    }
}

$('input#isbn13').blur(got_new_isbn);

$('input#thumbnail_url').blur(function(){
    $('img#cover_img').attr('src', $('input#thumbnail_url').val());
});
