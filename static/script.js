let chartInstance = null;

async function fetchData() {
    try {
        const res = await fetch('/data');
        const data = await res.json();

        const tbody = document.getElementById("table-body");
        tbody.innerHTML = "";

        let labels = [];
        let datasets = [];

        let colors = ["red", "blue", "green", "orange"];
        let i = 0;

        for (let host in data) {
            let history = data[host].history;

            if (!history || history.length === 0) continue;

            let latest = history[history.length - 1];

            let statusClass = latest.status === "UP" ? "status-up" : "status-down";

            let row = `<tr>
                <td>${host}</td>
                <td class="${statusClass}">${latest.status}</td>
                <td>${latest.latency || "N/A"} ms</td>
                <td>${latest.uptime}%</td>
            </tr>`;

            tbody.innerHTML += row;

            let times = history.map(h => h.time);
            let latency = history.map(h => parseInt(h.latency) || 0);

            labels = times;

            datasets.push({
                label: host,
                data: latency,
                borderColor: colors[i % colors.length],
                fill: false,
                tension: 0.3
            });

            i++;
        }

        updateChart(labels, datasets);

    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

function updateChart(labels, datasets) {
    const ctx = document.getElementById('chart');

    if (!ctx) return;

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        }
    });
}

setInterval(fetchData, 3000);