function showSection(section) {
    document.querySelectorAll('.content-section').forEach((el) => {
        el.style.display = 'none';
    });

    document.getElementById(section).style.display = 'block';
}

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    let formData = new FormData(this);
    fetch('/upload_image', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.result) {
            resultDiv.innerHTML = `<h3>Result: ${data.result}</h3>`;
        } else {
            resultDiv.innerHTML = `<h3>Error: ${data.error}</h3>`;
        }
    })
    .catch(error => {
        document.getElementById('result').innerHTML = `<h3>Error: ${error}</h3>`;
    });
});
