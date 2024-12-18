function showSection(section) {
    document.querySelectorAll('.content-section').forEach((el) => {
        el.style.display = 'none';
    });

    const selectedSection = document.getElementById(section);
    if (selectedSection) {
        selectedSection.style.display = 'block';
    }
}

function detectPneumonia() {
    const resultDiv = document.getElementById('result');
    // Simulate pneumonia detection (replace with actual API call)
    const hasPneumonia = Math.random() < 0.5; // Random for simulation

    if (hasPneumonia) {
        resultDiv.innerHTML = `
            <h3>Detection Result: Positive</h3>
            <p>Contact the following doctors immediately:</p>
            <ul>
                <li>Dr. A. Smith: 123-456-7890</li>
                <li>Dr. B. Johnson: 987-654-3210</li>
            </ul>
        `;
    } else {
        resultDiv.innerHTML = `
            <h3>Detection Result: Negative</h3>
            <p>Precautions to take:</p>
            <ul>
                <li>Drink plenty of fluids.</li>
                <li>Get enough rest.</li>
                <li>Wash your hands frequently.</li>
            </ul>
        `;
    }
    resultDiv.style.display = 'block';
}
