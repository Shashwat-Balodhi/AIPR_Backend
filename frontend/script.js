async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("https://your-backend-url.onrender.com/process", {
            method: "POST",
            body: formData
        });

        const data = await response.json();
        document.getElementById("output").innerText = data.analysis || "No response";
    } catch (error) {
        console.error("Error:", error);
    }
}
