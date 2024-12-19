const baseApiEndpoint = "https://surmine-bec9180195b8.herokuapp.com/project-files";

// Load initial data (customers)
async function fetchCustomers() {
    try {
        const response = await fetch(`${baseApiEndpoint}/list-customers`);
        const data = await response.json();
        const navigation = document.getElementById("navigation");

        navigation.innerHTML = ""; // Clear previous navigation
        data.customers.forEach(customer => {
            const customerDiv = document.createElement("div");
            customerDiv.textContent = customer;
            customerDiv.addEventListener("click", () => fetchProjects(customer));
            navigation.appendChild(customerDiv);
        });
    } catch (error) {
        console.error("Error fetching customers:", error);
    }
}

// Fetch projects for a customer
async function fetchProjects(customer) {
    try {
        const response = await fetch(`${baseApiEndpoint}/list-projects/${customer}`);
        const data = await response.json();
        const content = document.getElementById("content");

        content.innerHTML = `<h2>${customer}</h2>`;
        data.projects.forEach(project => {
            const projectDiv = document.createElement("div");
            projectDiv.textContent = project;
            projectDiv.addEventListener("click", () => fetchFiles(customer, project));
            content.appendChild(projectDiv);
        });

        // Update upload button autofill
        document.getElementById("uploadButton").dataset.customer = customer;
        document.getElementById("uploadButton").dataset.project = "";
    } catch (error) {
        console.error("Error fetching projects:", error);
    }
}

// Fetch files for a project
async function fetchFiles(customer, project) {
    try {
        const response = await fetch(`${baseApiEndpoint}/list-files/${customer}/${project}`);
        const data = await response.json();
        const content = document.getElementById("content");

        content.innerHTML = `<h2>${project}</h2>`;
        data.files.forEach(file => {
            const fileDiv = document.createElement("div");
            fileDiv.textContent = file;
            content.appendChild(fileDiv);
        });

        // Update upload button autofill
        document.getElementById("uploadButton").dataset.customer = customer;
        document.getElementById("uploadButton").dataset.project = project;
    } catch (error) {
        console.error("Error fetching files:", error);
    }
}

// Handle upload button click
document.getElementById("uploadButton").addEventListener("click", () => {
    const customer = document.getElementById("uploadButton").dataset.customer || "";
    const project = document.getElementById("uploadButton").dataset.project || "";

    document.getElementById("customer").value = customer;
    document.getElementById("project").value = project;

    // Show upload form modal
    document.getElementById("uploadModal").style.display = "block";
});

// Handle form submission for file upload
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
        const response = await fetch(`${baseApiEndpoint}/upload-multiple`, {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            alert("Files uploaded successfully!");
            document.getElementById("uploadModal").style.display = "none"; // Close upload form modal
            fetchFiles(customer, project); // Refresh files view
        } else {
            alert("An error occurred while uploading files.");
        }
    } catch (error) {
        console.error("Error during upload:", error);
        alert("An unexpected error occurred while uploading files.");
    }
});

// Cancel upload form
document.getElementById("cancelUpload").addEventListener("click", () => {
    document.getElementById("uploadModal").style.display = "none";
});

// Load customers on page load
fetchCustomers();
