// Função para armazenar o nome localmente
function armazenarNome() {
    var nome = document.getElementById('text').value; // Captura o valor do campo de entrada
    localStorage.setItem('nome', nome); // Armazena o nome localmente com a chave 'nome'
}

// Adiciona um evento de clique ao botão
document.getElementById('criar-conta-btn').addEventListener('click', armazenarNome);