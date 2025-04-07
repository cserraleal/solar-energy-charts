const ctxPrecip = document.getElementById("solarChart").getContext("2d");
let chartInstance;

// Load precipitation data
fetch("data/averages/avg_prectotcorr.json")
  .then((res) => res.json())
  .then((data) => {
    const select = document.getElementById("departamentoSelect");

    // Sort alphabetically
    data.sort((a, b) => a.departamento.localeCompare(b.departamento));

    // Populate dropdown
    data.forEach((item) => {
      const opt = document.createElement("option");
      opt.value = item.departamento;
      opt.textContent = capitalize(item.departamento);
      if (item.departamento.toLowerCase() === "guatemala") {
        opt.selected = true;
      }
      select.appendChild(opt);
    });

    // Initial render
    renderChart(data, select.value);

    // Update on change
    select.addEventListener("change", () => {
      renderChart(data, select.value);
    });
  })
  .catch((err) => {
    console.error("Error loading precipitation data:", err);
  });

function renderChart(data, selectedDept) {
  const entry = data.find((d) => d.departamento === selectedDept);
  if (!entry) return;

  const labels = Object.keys(entry.datos);
  const values = Object.values(entry.datos);
  const colors = values.map(colorFromPrecip);

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctxPrecip, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: `Precipitación Promdio - ${capitalize(selectedDept)}`,
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
          position: "top"
        },
        title: {
          display: false,
          text: "Precipitación Promedio Mensual",
          align: "center",
          font: {
            size: 18,
            weight: "bold",
            color: "#000000"
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y} mm`
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
            text: "mm"
          },
          beginAtZero: true
        }
      }
    }
  });
}

// Light blue → dark blue based on rainfall (mm)
function colorFromPrecip(value) {
  if (value < 3) return "#cce5ff";    // very light blue
  if (value < 5) return "#99ccff";   // light blue
  if (value < 7) return "#6699ff";   // medium blue
  if (value < 10) return "#3366cc";   // dark blue
  return "#003399";                    // very dark blue
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, " ");
}
