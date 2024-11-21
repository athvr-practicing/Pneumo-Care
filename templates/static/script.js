function showSection(section) {
    document.querySelectorAll('.content-section').forEach((el) => {
        el.style.display = 'none';
    });

    document.getElementById(section).style.display = 'block';

    if (section === 'upload' || section === 'about' || section === 'requirements') {
        setTimeout(() => {
            document.getElementById('images').classList.remove('hidden');
        }, 1000); 
    }
}



  