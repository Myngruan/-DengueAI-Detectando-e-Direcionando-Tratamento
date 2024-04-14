document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("btnRodarModelo").addEventListener("click", function () {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/rodar_modelo", true);
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onload = function () {
            if (xhr.status == 200) {
                alert("Ok! O modelo foi rodado com sucesso!");
            } else {
                alert("Ocorreu um erro ao rodar o modelo.");
            }
        };

        xhr.onerror = function () {
            alert("Erro de conexão.");
        };

        xhr.send();
    });
});
