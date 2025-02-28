document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("predictForm").addEventListener("submit", async (event) => {
        event.preventDefault();
        
        console.log("Form Submitted"); // Debugging line to ensure the form submission event is firing
        let latitude = document.getElementById("latitude").value.trim();
        let longitude = document.getElementById("longitude").value.trim();
        console.log("Latitude:", latitude, "Longitude:", longitude); // Debugging line

        // Check if latitude and longitude are not empty
        if (!latitude || !longitude) {
            console.error("Latitude and Longitude are required!");
            document.getElementById("result").innerText = "Please enter valid latitude and longitude.";
            return;
        }

        // Parse latitude and longitude
        latitude = parseFloat(latitude);
        longitude = parseFloat(longitude);

        // Validate the parsed values
        if (isNaN(latitude) || isNaN(longitude)) {
            console.error("Invalid Latitude or Longitude!");
            document.getElementById("result").innerText = "Invalid Latitude or Longitude.";
            return;
        }

        console.log("Sending Data:", { latitude, longitude });

        // Make the fetch request to the backend
        try {
            let response = await fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latitude, longitude })
            });

            let result = await response.json();
            console.log("Server Response:", result);

            // Display recommended crops
            if (result.recommended_crops) {
                document.getElementById("result").innerHTML = `<h3>Recommended Crops:</h3> 
                <ol>
                    <li>${result.recommended_crops[0]}</li>
                    <li>${result.recommended_crops[1]}</li>
                    <li>${result.recommended_crops[2]}</li>
                </ol>`;
            } else {
                document.getElementById("result").innerText = "Error: " + result.error;
            }
        } catch (error) {
            console.error("Error:", error);
            document.getElementById("result").innerText = "Failed to fetch prediction.";
        }
    });
});