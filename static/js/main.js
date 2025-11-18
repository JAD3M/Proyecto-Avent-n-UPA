console.log("Frontend Flask conectado correctamente");

document.addEventListener("DOMContentLoaded", function () {
    const tipoUsuario = document.querySelector('input[name="tipo"]').value;
    const campoMatricula = document.getElementById("matriculaCocheField");

    if (tipoUsuario === "pasajero") {
        campoMatricula.style.display = "none";
    }
});