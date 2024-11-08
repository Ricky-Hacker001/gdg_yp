function fetchCropRecommendations() {
    const region = document.getElementById("region").value;
    const start_month = document.getElementById("start_month").value;
    const end_month = document.getElementById("end_month").value;
    const land_area = document.getElementById("land_area").value;

    fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ region, start_month, end_month, land_area })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("recommendations").style.display = "block";
        document.getElementById("low-investment-crop").innerText = data.crop_data['Crop Name'];
        document.getElementById("low-investment-details").innerText = data.recommendation;
    })
    .catch(error => console.error('Error:', error));
}
