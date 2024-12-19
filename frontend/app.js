// API endpoint for file uploads
const apiEndpoint = "https://surmine-bec9180195b8.herokuapp.com/project-files/upload-multiple";

// Form submission event handler
document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent default form submission

    const formData = new FormData();
    const customer = document.getElementById("customer").value;
    const project = document.getElementById("project").value;
    const folder = document.getElementById("folder").value;
    const files = document.getElementById("files").files;

    if (!customer || !project || files.length === 0) {
        alert("Please fill out all required fields and select at least one file!");
        return;
    }

    formData.append("customer", customer);
    formData.append("project", project);
    if (folder) formData.append("folder", folder);
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    try {
        // Send POST request to backend
        const response = await fetch(apiEndpoint, {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            // Display success message if status is 200
            const responseDiv = document.getElementById("response");
            responseDiv.innerHTML = `<h2>Files uploaded successfully!</h2>`;
        } else {
            alert("An error occurred while uploading files.");
        }
    } catch (error) {
        console.error("Error during upload:", error);
        alert("An unexpected error occurred while uploading files.");
    }
});
