// ID of the canvas element
const ctx = document.getElementById("solarChart").getContext("2d");

// Location and year you want to show (you can make this dynamic later)
const ubicacionSeleccionada = "Ciudad de Guatemala";
const añoSeleccionado = 2023;

// Fetch the JSON data
fetch("data/irradiation.json")
  .then((response) => response.json())
  .then((jsonData) => {
    // Filter the data for the selected location and year
    const registro = jsonData.find(
      (entry) =>
        entry.ubicacion === ubicacionSeleccionada &&
        entry.año === añoSeleccionado
    );

    if (!registro) {
      console.error("No se encontró información para esta ubicación y año.");
      return;
    }

    const etiquetas = Object.keys(registro.datos);
    const valores = Object.values(registro.datos);

    // Create the chart
    new Chart(ctx, {
      type: "line",
      data: {
        labels: etiquetas,
        datasets: [{
          label: "Radiación Solar (kWh/m²)",
          data: valores,
          fill: true,
          borderColor: "#f39c12",
          backgroundColor: "rgba(243, 156, 18, 0.2)",
          tension: 0.4,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Radiación Solar Mensual - ${ubicacionSeleccionada} (${añoSeleccionado})`,
            font: {
              size: 18
            }
          },
          legend: {
            labels: {
              font: {
                size: 14
              }
            }
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                return `${context.dataset.label}: ${context.parsed.y} kWh/m²`;
              }
            }
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "kWh por metro cuadrado"
            }
          },
          x: {
            title: {
              display: true,
              text: "Mes"
            }
          }
        }
      }
    });
  })
  .catch((error) => {
    console.error("Error al cargar el archivo JSON:", error);
  });
