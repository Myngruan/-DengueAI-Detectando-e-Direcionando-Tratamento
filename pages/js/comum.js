function limparLocalStorage() {
    localStorage.removeItem('consultaData'); // Remove o item 'consultaData' do armazenamento local
    localStorage.removeItem('nome'); // Remove o item 'consultaData' do armazenamento local
}

// Adiciona um evento de clique ao link com o ID 'limpar-link'
document.getElementById('limpar-link').addEventListener('click', limparLocalStorage);