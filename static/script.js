document.addEventListener("DOMContentLoaded", function () {
    const addDestinationButton = document.getElementById("addDestinationButton");
    const additionalDestinations = document.getElementById("additional-destinations");
    const saveApplyButton = document.getElementById("save-apply-btn");
    const downloadButton = document.getElementById("download-btn");

    const sourceInput = document.getElementById("source");
    const destinationInput = document.getElementById("destination");

    const ports = []; // To store all ports

    addDestinationButton.addEventListener("click", function () {
        const newInput = document.createElement("input");
        newInput.type = "text";
        newInput.name = "additional-port";
        newInput.placeholder = "Add additional port";
        newInput.className = "input-text";

        additionalDestinations.appendChild(newInput);
    });

    saveApplyButton.addEventListener("click", function () {
        const source = sourceInput.value;
        const destination = destinationInput.value;

        const additionalPortInputs = document.querySelectorAll("[name='additional-port']");
        additionalPortInputs.forEach(input => {
            ports.push(input.value);
        });

        // Send the data to the backend and save it to the database
        const formData = new FormData();
        formData.append("source", source);
        formData.append("destination", destination);

        ports.forEach(port => {
            formData.append("ports[]", port);
        });

        fetch("/save", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            alert(data); // Display the response message
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    downloadButton.addEventListener("click", function () {
        // Use jsPDF to generate and download a PDF
        const pdf = new jsPDF();
        
        pdf.text(`Source: ${sourceInput.value}`, 10, 10);
        pdf.text(`Destination: ${destinationInput.value}`, 10, 20);
        ports.forEach((port, index) => {
            pdf.text(`Additional Port ${index + 1}: ${port}`, 10, 30 + index * 10);
        });

        pdf.save("route_information.pdf");
    });
});
