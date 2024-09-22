document.addEventListener('DOMContentLoaded', function() {
    function openModal(modalId) {
        document.getElementById(modalId).style.display = "block";
    }

    function closeModal(modalId) {
        document.getElementById(modalId).style.display = "none";
    }


    document.getElementById('openModal').onclick = function() {
        openModal('modal');
    }


    var buttonsEmprestimo = document.getElementsByClassName('open-emprestimo');
    for (var i = 0; i < buttonsEmprestimo.length; i++) {
        buttonsEmprestimo[i].onclick = function() {
            openModal('modal-emprestimo');
            document.getElementById('cliente_id').value = this.getAttribute('data-cliente-id');
            document.getElementById('form-emprestimo').action = "/realizar_emprestimo/" + this.getAttribute('data-cliente-id') + "/";
        }
    }


    var buttonsEdit = document.getElementsByClassName('open-edit');
    for (var i = 0; i < buttonsEdit.length; i++) {
        buttonsEdit[i].onclick = function() {
            var clienteId = this.getAttribute('data-cliente-id');
            fetch('/get_cliente_data/' + clienteId + '/')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('edit_nome').value = data.nome;
                    document.getElementById('edit_cpf').value = data.cpf;
                    document.getElementById('edit_data_nascimento').value = data.data_nascimento;
                    document.getElementById('edit_telefone').value = data.telefone;
                    document.getElementById('edit_renda_mensal').value = data.renda_mensal;
                    document.getElementById('edit_cliente_id').value = clienteId;
                    document.getElementById('form-edit').action = "/editar_cliente/" + clienteId + "/";
                    openModal('modal-edit');
                })
                .catch(error => console.error('Erro ao buscar dados do cliente:', error));
        }
    }


    var buttonsCartao = document.getElementsByClassName('open-cartao');
    for (var i = 0; i < buttonsCartao.length; i++) {
        buttonsCartao[i].onclick = function() {
            openModal('modalCartaoCredito');
            var clienteId = this.getAttribute('data-cliente-id');
            document.getElementById('cliente_id').value = clienteId;
            document.getElementById('formCartaoCredito').action = "/cadastrar_cartao_de_credito/" + clienteId + "/";
        }
    }

    var closeButtons = document.getElementsByClassName('close');
    for (var i = 0; i < closeButtons.length; i++) {
        closeButtons[i].onclick = function() {
            var modal = this.closest('.modal');
            closeModal(modal.id);
        }
    }

    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            closeModal(event.target.id);
        }
    }
});
