const ctxWind = document.getElementById("solarChart").getContext("2d");
let chartInstance;

Promise.all([
  fetch("data/averages/avg_ws2m.json").then(res => res.json()),
  fetch("data/averages/avg_ws2m_max.json").then(res => res.json()),
  fetch("data/averages/avg_ws2m_min.json").then(res => res.json())
]).then(([avg, max, min]) => {
  const select = document.getElementById("departamentoSelect");

  // Sort alphabetically
  avg.sort((a, b) => a.departamento.localeCompare(b.departamento));
  avg.forEach(entry => {
    const opt = document.createElement("option");
    opt.value = entry.departamento;
    opt.textContent = capitalize(entry.departamento);
    if (entry.departamento === "guatemala") opt.selected = true;
    select.appendChild(opt);
  });

  renderChart("guatemala", avg, max, min);

  select.addEventListener("change", () => {
    renderChart(select.value, avg, max, min);
  });
}).catch(err => {
  console.error("❌ Error loading wind speed range chart:", err);
});

function renderChart(dept, avgData, maxData, minData) {
  const meses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];

  const getDeptData = (data, dept) => {
    const entry = data.find(d => d.departamento === dept);
    return meses.map(m => entry?.datos[m] || null);
  };

  const avgVals = getDeptData(avgData, dept);
  const maxVals = getDeptData(maxData, dept);
  const minVals = getDeptData(minData, dept);

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctxWind, {
    type: "line",
    data: {
      labels: meses,
      datasets: [
        {
          label: "Velocidad Promedio",
          data: avgVals,
          borderColor: "#3498db",
          backgroundColor: "#3498db",
          tension: 0.3,
          pointRadius: 2,
          fill: false
        },
        {
          label: "Velocidad Máxima",
          data: maxVals,
          borderColor: "#e74c3c",
          backgroundColor: "#e74c3c",
          tension: 0.3,
          pointRadius: 2,
          fill: false
        },
        {
          label: "Velocidad Mínima",
          data: minVals,
          borderColor: "#2ecc71",
          backgroundColor: "#2ecc71",
          tension: 0.3,
          pointRadius: 2,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false, // ✅ KEY FIX
      animation: {
        duration: 1000,
        easing: "easeOutQuart"
      },
      plugins: {
        title: {
          display: true,
          text: `Velocidades del Viento (Promedio, Máxima, Mínima) - ${capitalize(dept)}`,
          font: {
            size: 18
          },
          padding: {
            top: 10,
            bottom: 20
          }
        },
        legend: {
          position: "bottom"
        },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y} m/s`
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
            text: "m/s"
          },
          beginAtZero: true
        }
      }
    }
  });
}


function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1).replace(/_/g, " ");
}
