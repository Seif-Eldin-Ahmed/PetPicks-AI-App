document.getElementById('upload-form').addEventListener('submit', function(e) {

    // Prevents the page from reloading
    e.preventDefault();

    // To take a copy of the form and put it inside a variable
    let formData = new FormData(this);
    console.log(formData);

    // Post request to send the form data to the '/upload' path and wait for the response
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then( response => response.json() )
    .then( data => {
        document.getElementById('result-container').innerText = 'Result: ' + data.result;
    })
    .catch( error => {
        console.log('Error', error)
    })

});
