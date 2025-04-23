document.addEventListener("DOMContentLoaded", function () {
	const queryForm = document.getElementById("queryForm");
	const imageInput = document.getElementById("imageInput");
	const imagePreview = document.getElementById("imagePreview");
	const previewImg = document.getElementById("previewImg");
	const answerOutput = document.getElementById("answerOutput");
	const extractedTextOutput = document.getElementById("extractedTextOutput");
	const buildingCodeOutput = document.getElementById("buildingCodeOutput");
	const exampleCards = document.querySelectorAll(".example-card");
	const dropZone = document.getElementById("dropZone");
	const uploadPrompt = document.getElementById("uploadPrompt");
	const changeImageBtn = document.getElementById("changeImageBtn");
	const statusBadge = document.getElementById("statusBadge");

	// Drag and drop functionality
	["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
		dropZone.addEventListener(eventName, preventDefaults, false);
	});

	function preventDefaults(e) {
		e.preventDefault();
		e.stopPropagation();
	}

	["dragenter", "dragover"].forEach((eventName) => {
		dropZone.addEventListener(eventName, highlight, false);
	});

	["dragleave", "drop"].forEach((eventName) => {
		dropZone.addEventListener(eventName, unhighlight, false);
	});

	function highlight() {
		dropZone.classList.add("highlight");
	}

	function unhighlight() {
		dropZone.classList.remove("highlight");
	}

	dropZone.addEventListener("drop", handleDrop, false);

	function handleDrop(e) {
		const dt = e.dataTransfer;
		const files = dt.files;
		if (files.length) {
			imageInput.files = files;
			handleFiles(files);
		}
	}

	function handleFiles(files) {
		if (files.length > 0) {
			const file = files[0];
			if (file.type.match("image.*")) {
				updateImagePreview(file);
			} else {
				showNotification("Please upload an image file.", "error");
			}
		}
	}

	// Click to browse files
	dropZone.addEventListener("click", function () {
		if (imagePreview.classList.contains("d-none")) {
			imageInput.click();
		}
	});

	// Change image button
	changeImageBtn.addEventListener("click", function (e) {
		e.stopPropagation();
		imageInput.click();
	});

	// Image preview functionality
	imageInput.addEventListener("change", function (e) {
		if (e.target.files.length > 0) {
			const file = e.target.files[0];
			updateImagePreview(file);
		}
	});

	function updateImagePreview(file) {
		const url = URL.createObjectURL(file);
		previewImg.src = url;
		uploadPrompt.classList.add("d-none");
		imagePreview.classList.remove("d-none");
		dropZone.style.padding = "10px";
	}

	// Update status badge
	function updateStatus(status, type = "secondary") {
		statusBadge.textContent = status;
		statusBadge.className = `badge bg-${type}`;
	}

	// Show notification
	function showNotification(message, type = "info") {
		// You could implement a toast notification here
		console.log(`${type.toUpperCase()}: ${message}`);
	}

	// Form submission
	queryForm.addEventListener("submit", function (e) {
		e.preventDefault();

		const formData = new FormData(queryForm);
		if (!formData.get("image")) {
			showNotification("Please upload an image.", "error");
			return;
		}

		if (!formData.get("question")) {
			showNotification("Please enter your question.", "error");
			return;
		}

		// Update status
		updateStatus("Processing...", "warning");

		// Clear previous results
		answerOutput.innerHTML = `
			<div class="placeholder-content">
				<div class="loading-message">Analyzing your plan...</div>
				<div class="spinner">
					<div class="double-bounce1"></div>
					<div class="double-bounce2"></div>
				</div>
			</div>`;
		extractedTextOutput.innerHTML =
			'<div class="placeholder-content small"><i class="fas fa-spinner fa-spin me-2"></i>Extracting text...</div>';
		buildingCodeOutput.innerHTML =
			'<div class="placeholder-content small"><i class="fas fa-spinner fa-spin me-2"></i>Retrieving building code...</div>';

		// Submit the form data
		fetch("/api/process", {
			method: "POST",
			body: formData,
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error(response.statusText || "Network response was not ok");
				}
				return response.json();
			})
			.then((data) => {
				// Update status
				updateStatus("Response received", "success");

				// Display the results
				if (data.error) {
					answerOutput.innerHTML = `<div class="alert alert-danger mb-0"><i class="fas fa-exclamation-circle me-2"></i>${data.error}</div>`;
					updateStatus("Error", "danger");
				} else {
					// Format the answer with nicer styling
					answerOutput.innerHTML = formatAnswer(data.answer);
					extractedTextOutput.innerHTML = formatOutput(data.extractedText);
					buildingCodeOutput.innerHTML = formatOutput(data.buildingCode);
				}

				// Auto-scroll to answer
				answerOutput.scrollIntoView({ behavior: "smooth", block: "nearest" });
			})
			.catch((error) => {
				// Update status
				updateStatus("Error", "danger");

				// Display error
				answerOutput.innerHTML = `<div class="alert alert-danger mb-0"><i class="fas fa-exclamation-circle me-2"></i>${error.message}</div>`;
				console.error("Error:", error);

				showNotification("An error occurred while processing your request.", "error");
			});
	});

	// Format answer with nice styling
	function formatAnswer(text) {
		if (!text) return '<div class="text-muted">No answer generated.</div>';

		// Replace URLs with links
		text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');

		// Add paragraph breaks
		text = text.replace(/\n\n/g, "</p><p>");

		return `<p>${text}</p>`;
	}

	// Format output areas
	function formatOutput(text) {
		if (!text || text.includes("No text extracted") || text.includes("No building code")) {
			return `<div class="text-muted"><i class="fas fa-info-circle me-2"></i>No data available.</div>`;
		}

		// Try to detect if it's JSON to format it nicely
		if (text.trim().startsWith("{") || text.trim().startsWith("[")) {
			try {
				const jsonData = JSON.parse(text);
				return `<pre>${JSON.stringify(jsonData, null, 2)}</pre>`;
			} catch (e) {
				// Not valid JSON, continue with regular formatting
			}
		}

		return `<pre>${text}</pre>`;
	}

	// Example cards functionality
	exampleCards.forEach((card) => {
		card.addEventListener("click", function () {
			const imagePath = this.getAttribute("data-image");
			const question = this.getAttribute("data-question");

			updateStatus("Loading example...", "info");

			// Fetch the sample image and create a file object
			fetch(`/${imagePath}`)
				.then((response) => {
					if (!response.ok) {
						throw new Error("Network response was not ok");
					}
					return response.blob();
				})
				.then((blob) => {
					// Create a File object from the blob
					const file = new File([blob], imagePath.split("/").pop(), { type: "image/png" });

					// Create a DataTransfer object to set the file input value
					const dataTransfer = new DataTransfer();
					dataTransfer.items.add(file);
					imageInput.files = dataTransfer.files;

					// Update preview
					updateImagePreview(file);

					// Set the question
					document.getElementById("questionInput").value = question;

					updateStatus("Example loaded", "info");
					showNotification("Example loaded successfully. Click Submit to analyze.", "success");
				})
				.catch((error) => {
					console.error("Error loading example:", error);
					showNotification("Error loading example. Please try again.", "error");
					updateStatus("Error loading example", "danger");
				});
		});
	});
});

// Add styles for the loading components
document.head.insertAdjacentHTML(
	"beforeend",
	`
<style>
.highlight {
    border-color: #3498db !important;
    background-color: rgba(52, 152, 219, 0.1) !important;
}

.alert {
    border-radius: 8px;
}

pre {
    white-space: pre-wrap;
    word-break: break-word;
    margin-bottom: 0;
}

.loading-message {
    text-align: center;
    margin-bottom: 15px;
    color: #3498db;
    font-weight: 500;
    font-size: 16px;
    letter-spacing: 0.5px;
}
</style>
`
);
