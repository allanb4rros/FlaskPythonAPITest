// Aguarde até que o DOM esteja completamente carregado
document.addEventListener('DOMContentLoaded', function () {
    // Obter os resultados da API Flask
    fetch('/api/test_results')
        .then(response => response.json())  // Converte a resposta para JSON
        .then(data => {
            // Manipule os dados recebidos (test_results) e exiba-os na tabela
            const tableBody = document.getElementById('testResultsBody');

            // Itera sobre cada resultado no array test_results
            data.test_results.forEach(result => {
                const row = document.createElement('tr');  // Cria uma nova linha na tabela

                // Adicione as colunas da tabela
                const columns = ['_id', 'test_name', 'status', 'comparison_variable', 'content', 'expected', 'datetime'];
                columns.forEach(columnName => {
                    const cell = document.createElement('td');  // Cria uma nova célula na linha

                    // Adaptação para exibir os valores de final_location e initial_location do objeto 'comparison_variable'
                    if (columnName === 'comparison_variable' && result[columnName]) {
                        const { final_location, initial_location } = result[columnName];

                        if (final_location && initial_location) {
                            // Constrói o texto com base nos valores de final_location e initial_location
                            const textContent = `initial_location: (${initial_location.x || ''}, ${initial_location.y || ''}), final_location: (${final_location.x || ''}, ${final_location.y || ''})`;
                            cell.textContent = textContent;
                        } else {
                            cell.textContent = '';  // Se um ou ambos estiverem ausentes, defina como vazio
                        }
                    } else {
                        cell.textContent = result[columnName] || '';  // Se o valor estiver ausente, defina como vazio
                    }

                    // Adicione classes com base no status, usando operador de coalescência nula para lidar com valores nulos/undefined
                    if (columnName === 'status') {
                        cell.classList.add(result[columnName]?.toLowerCase() || '');
                    }

                    row.appendChild(cell);  // Adiciona a célula à linha
                });

                tableBody.appendChild(row);  // Adiciona a linha ao corpo da tabela
            });
        })
        .catch(error => console.error('Erro ao obter dados da API:', error));
});
