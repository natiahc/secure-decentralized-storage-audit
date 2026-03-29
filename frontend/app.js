const API_BASE = "http://localhost:8000";

// ----------------------
// UPLOAD
// ----------------------
async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Select a file first");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    document.getElementById("output").innerText =
        "UPLOAD RESULT:\n" + JSON.stringify(data, null, 2);
}


// ----------------------
// DOWNLOAD
// ----------------------
async function downloadFile() {
    const fileId = document.getElementById("fileId").value;

    if (!fileId) {
        alert("Enter file ID");
        return;
    }

    const res = await fetch(`${API_BASE}/download/${fileId}`);

    if (!res.ok) {
        const text = await res.text();
        alert("Download failed: " + text);
        return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;

    // optional: backend can send filename via header
    const contentDisposition = res.headers.get("Content-Disposition");
    let filename = "downloaded_file";

    if (contentDisposition && contentDisposition.includes("filename=")) {
        filename = contentDisposition.split("filename=")[1].replace(/"/g, "");
    }

    a.download = filename;

    document.body.appendChild(a);
    a.click();

    // cleanup
    a.remove();
    window.URL.revokeObjectURL(url);
}

// ----------------------
// NODE STATUS
// ----------------------
async function loadStatus() {
    const res = await fetch(`${API_BASE}/status`);
    const data = await res.json();

    document.getElementById("statusOutput").innerText =
        JSON.stringify(data, null, 2);
}


// ----------------------
// AUDIT LOGS
// ----------------------
async function loadAudit() {
    const res = await fetch(`${API_BASE}/audit`);
    const data = await res.json();

    document.getElementById("auditOutput").innerText =
        JSON.stringify(data, null, 2);
}