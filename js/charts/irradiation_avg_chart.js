const canvas = document.getElementById("solarChart").getContext("2d");

// Define a color palette (up to 22 departments)
const COLORS = [
  "#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c", "#e67e22",
  "#34495e", "#fd79a8", "#00cec9", "#6c5ce7", "#d63031", "#fab1a0", "#81ecec",
  "#55efc4", "#ffeaa7", "#74b9ff", "#a29bfe", "#636e72", "#fdcb6e", "#b2bec3", "#0984e3"
];

// Load the average irradiation data
fetch("data/averages/avg_allsky_sfc_sw_dwn.json")
  .then((res) => res.json())
  .then((data) => {
    const labels = Object.keys(data[0].datos); // ["Enero", "Febrero", ...]
    const datasets = data.map((entry, index) => {
      const color = COLORS[index % COLORS.length];
      return {
        label: capitalize(entry.departamento),
        data: Object.values(entry.datos),
        fill: false,
        borderColor: color,
        backgroundColor: color,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 5,
      };
    });

    new Chart(canvas, {
      type: "line",
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1500,
          easing: 'easeOutQuart'
        },
        plugins: {
          title: {
            display: true,
            text: "Radiación Solar Promedio Mensual por Departamento (2017–2024)",
            font: {
              size: 20
            },
            padding: {
              top: 10,
              bottom: 20
            }
          },
          tooltip: {
            mode: "nearest",
            intersect: false,
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y} kWh/m²`
            }
          },
          legend: {
            position: 'bottom',
            labels: {
              boxWidth: 12,
              font: {
                size: 12
              }
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
            beginAtZero: false
          }
        }
      }
    });
  })
  .catch((err) => {
    console.error("Error loading irradiation data:", err);
  });

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, " ");
}
