// Scripts personalizados para o sistema Casa da Cultura

// Função para inicializar máscaras nos campos
function initMasks() {
    // Máscara para CPF
    $('.cpf-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 11) {
            value = value.substring(0, 11);
        }
        
        if (value.length > 9) {
            $(this).val(value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4'));
        } else if (value.length > 6) {
            $(this).val(value.replace(/(\d{3})(\d{3})(\d{3})/, '$1.$2.$3'));
        } else if (value.length > 3) {
            $(this).val(value.replace(/(\d{3})(\d{3})/, '$1.$2'));
        } else {
            $(this).val(value);
        }
    });

    // Máscara para telefone
    $('.telefone-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 11) {
            value = value.substring(0, 11);
        }
        
        if (value.length > 10) {
            $(this).val(value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3'));
        } else if (value.length > 6) {
            $(this).val(value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3'));
        } else if (value.length > 2) {
            $(this).val(value.replace(/(\d{2})(\d{0,5})/, '($1) $2'));
        } else {
            $(this).val(value);
        }
    });

    // Máscara para CEP
    $('.cep-mask').on('input', function() {
        let value = $(this).val().replace(/\D/g, '');
        if (value.length > 8) {
            value = value.substring(0, 8);
        }
        
        if (value.length > 5) {
            $(this).val(value.replace(/(\d{5})(\d{3})/, '$1-$2'));
        } else {
            $(this).val(value);
        }
    });
}

// Função para inicializar tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Função para inicializar popovers
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Função para confirmar exclusão
function confirmDelete(event, message) {
    if (!confirm(message || 'Tem certeza que deseja excluir este item?')) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Inicializar funções quando o documento estiver pronto
$(document).ready(function() {
    initMasks();
    initTooltips();
    initPopovers();
    
    // Adicionar listener para botões de exclusão
    $('.btn-delete').on('click', function(e) {
        return confirmDelete(e);
    });
    
    // Fechar alertas automaticamente após 5 segundos
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
});

// Função para gerar gráficos no dashboard
function initCharts() {
    // Verificar se o elemento do gráfico existe
    if (document.getElementById('ajudasChart')) {
        // Dados do gráfico de ajudas (serão substituídos dinamicamente pelo backend)
        const ajudasData = {
            labels: ['Hospital', 'Creche', 'Cesta Básica', 'Transporte'],
            datasets: [{
                label: 'Quantidade de Pessoas',
                data: [
                    document.getElementById('ajuda_hospital_count').value,
                    document.getElementById('ajuda_creche_count').value,
                    document.getElementById('cesta_basica_count').value,
                    document.getElementById('ajuda_transporte_count').value
                ],
                backgroundColor: [
                    'rgba(13, 110, 253, 0.7)',
                    'rgba(253, 126, 20, 0.7)',
                    'rgba(25, 135, 84, 0.7)',
                    'rgba(220, 53, 69, 0.7)'
                ],
                borderColor: [
                    'rgba(13, 110, 253, 1)',
                    'rgba(253, 126, 20, 1)',
                    'rgba(25, 135, 84, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        };

        // Criar gráfico de ajudas
        const ajudasCtx = document.getElementById('ajudasChart').getContext('2d');
        new Chart(ajudasCtx, {
            type: 'bar',
            data: ajudasData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Distribuição de Ajudas'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }

    // Verificar se o elemento do gráfico de aniversariantes existe
    if (document.getElementById('aniversariantesChart')) {
        // Obter dados dos aniversariantes por mês
        const meses = [];
        const totais = [];
        
        document.querySelectorAll('.aniversariante-mes-data').forEach(function(el) {
            meses.push(el.getAttribute('data-mes'));
            totais.push(parseInt(el.getAttribute('data-total')));
        });

        // Criar gráfico de aniversariantes por mês
        const aniversariantesCtx = document.getElementById('aniversariantesChart').getContext('2d');
        new Chart(aniversariantesCtx, {
            type: 'line',
            data: {
                labels: meses,
                datasets: [{
                    label: 'Aniversariantes',
                    data: totais,
                    backgroundColor: 'rgba(253, 126, 20, 0.2)',
                    borderColor: 'rgba(253, 126, 20, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Aniversariantes por Mês'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        }
                    }
                }
            }
        });
    }
}

// Inicializar gráficos quando a página for carregada
document.addEventListener('DOMContentLoaded', function() {
    // Verificar se Chart.js está disponível
    if (typeof Chart !== 'undefined') {
        initCharts();
    }
});
