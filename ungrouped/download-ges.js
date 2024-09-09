// Select all anchor tags in the document that contain the download links
let links = document.querySelectorAll('a[href*="route=information/download"]');

// Create a download function
function downloadURI(uri, name) {
    let link = document.createElement("a");
    link.href = uri;
    link.download = name;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Loop through each link and download the file with the original name
links.forEach((link) => {
    let url = link.href;

    // Extract the file name from the title attribute or the textContent of the link
    let filename = link.getAttribute("title") || link.textContent.trim() || `file_${Math.random().toString(36).substr(2, 9)}.pdf`;

    // Sanitize the file name (remove any illegal characters)
    filename = filename.replace(/[\/\?<>\\:\*\|"]/g, '').trim() + '.pdf';

    downloadURI(url, filename);
});

console.log(`${links.length} files found and downloaded.`);
