const ctx = document.getElementById("solarChart").getContext("2d");
let chartInstance;

fetch("data/violin/wind_ws2m_violin.json")
  .then((res) => res.json())
  .then((data) => {
    const select = document.getElementById("departamentoSelect");

    // Sort and create dropdown
    data.sort((a, b) => a.departamento.localeCompare(b.departamento));
    data.forEach((entry) => {
      const opt = document.createElement("option");
      opt.value = entry.departamento;
      opt.textContent = capitalize(entry.departamento);
      if (entry.departamento === "guatemala") opt.selected = true;
      select.appendChild(opt);
    });

    renderChart(data, select.value);

    select.addEventListener("change", () => {
      renderChart(data, select.value);
    });
  })
  .catch((err) => {
    console.error("❌ Error loading wind scatter data:", err);
  });

  function renderChart(data, dept) {
    const entry = data.find(d => d.departamento === dept);
    if (!entry) return;
  
    const monthNames = [
      "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
      "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];
  
    const scatterData = [];
  
    monthNames.forEach((mes, i) => {
      const baseX = i + 1; // x = 1–12
      const values = entry.datos[mes] || [];
      values.forEach(val => {
        scatterData.push({
          x: baseX + (Math.random() - 0.5) * 0.6, // Add horizontal jitter
          y: val
        });
      });
    });
  
    if (chartInstance) chartInstance.destroy();
  
    chartInstance = new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: [{
          label: `Velocidad del Viento (WS2M) - ${capitalize(dept)}`,
          data: scatterData,
          backgroundColor: "#3498db",
          pointRadius: 1.5,
          pointHoverRadius: 3
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Distribución Horaria de Velocidad del Viento (WS2M)",
            font: { size: 18 },
            padding: { top: 10, bottom: 20 }
          },
          legend: { display: false }
        },
        scales: {
          x: {
            type: "linear",
            min: 0.5,
            max: 12.5,
            title: {
              display: true,
              text: "Mes"
            },
            ticks: {
              stepSize: 1,
              callback: (val) => monthNames[val - 1] || ""
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
  