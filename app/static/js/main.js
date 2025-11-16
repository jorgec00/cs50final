//Load the progress bars when the webpage is loaded
document.addEventListener("DOMContentLoaded", () => {
    loadProgress();
});

//Load progress bars when page loads
async function loadProgress() {
    //Get element from html File
    const progressBars = document.getElementById("progressBars");

    //Ensure it was returned
    if (!progressBars) return; // not on dashboard page

    // Clear existing content

    // Fetch progress data from API
    try {
        const response = await fetch("/api/progress", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // ... render data into progressBars ...
        const certs = data.certifications; // Assuming API returns { certifications: [...] }
        // If empty show message
        if (certs.length === 0) {
            progressBars.innerHTML = "<p>No certifications in progress.</p>";
            return;
        }

        //Build progress bar for each certification
        // Render with initial width 0% and store target in data-target so we can animate to it
        const barsHTML = certs.map(cert => {
            const percentage = Number(cert.percent_complete).toFixed(2);
            const certName = cert.name;

            //Change bar color based on percentage
            let barClass = "bg-danger"; // Red for 0-49%
            if (percentage >= 50 && percentage < 80) {
                barClass = "bg-warning"; // Yellow for 50-79%
            } else if (percentage >= 80) {
                barClass = "bg-success"; // Green for 80-100%
            }

            //Create the html for the progress bar; start width at 0 and store target in data-target
            return `
                <div class="mb-4">
                    <small class="text-muted">${certName}</small>
                    <div class="progress" style="height: 25px;">
                        <div class="progress-bar ${barClass}" role="progressbar" style="width: 0%;" data-target="${percentage}" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
                            0%
                        </div>
                    </div>
                </div>
            `;
        }).join("");

        // Insert HTML with bars at width 0
        progressBars.innerHTML = barsHTML;

        // Animate bars to their target widths on the next animation frame
        requestAnimationFrame(() => {
            const bars = progressBars.querySelectorAll('.progress-bar');
            bars.forEach(bar => {
                const target = bar.dataset.target;
                bar.style.width = `${target}%`;
                bar.setAttribute('aria-valuenow', target);
                bar.textContent = `${target}%`;
            });
        });

    } catch (err) {
        console.error("Failed to load progress:", err);
        progressBars.innerHTML = `<p>Error loading progress data.</p>`;
    }


}