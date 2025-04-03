const ctx = document.getElementById("solarChart").getContext("2d");
let chartInstance;

// Load the data
fetch("data/averages/avg_allsky_sfc_sw_dwn.json")
  .then((res) => res.json())
  .then((data) => {
    const select = document.getElementById("departamentoSelect");

    // Sort alphabetically by departamento name
    data.sort((a, b) => a.departamento.localeCompare(b.departamento));

    // Populate dropdown
    data.forEach((item) => {
      const opt = document.createElement("option");
      opt.value = item.departamento;
      opt.textContent = capitalize(item.departamento);

      // Preselect "guatemala" by default
      if (item.departamento.toLowerCase() === "guatemala") {
        opt.selected = true;
      }

      select.appendChild(opt);
    });

    // Render chart for Guatemala by default
    const selected = select.value || "guatemala";
    renderChart(data, selected);

    // Change chart on selection
    select.addEventListener("change", () => {
      renderChart(data, select.value);
    });
  })
  .catch((err) => {
    console.error("Error loading irradiation data:", err);
  });

// Render function
function renderChart(data, selectedDept) {
  const entry = data.find((d) => d.departamento === selectedDept);
  if (!entry) return;

  const labels = Object.keys(entry.datos);
  const values = Object.values(entry.datos);
  const colors = values.map(colorFromValue);

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: `Radiación Solar - ${capitalize(selectedDept)}`,
        data: values,
        backgroundColor: colors,
        borderRadius: 5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        duration: 1000,
        easing: "easeOutQuart"
      },
      plugins: {
        legend: {
          position: "bottom"
        },
        title: {
          display: true,
          text: "Radiación Solar Promedio Mensual (2017–2024)",
          font: {
            size: 18
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y} kWh/m²`
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: "Mes"
          }
        },
        y: {
          title: {
            display: true,
            text: "kWh/m²/día"
          },
          beginAtZero: true
        }
      }
    }
  });
}

// Value to color (green → red)
function colorFromValue(value) {
  if (value < 4.5) return "#2ecc71";       // green
  if (value < 5.2) return "#f1c40f";       // yellow
  if (value < 6.0) return "#e67e22";       // orange
  return "#e74c3c";                        // red
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, " ");
}
