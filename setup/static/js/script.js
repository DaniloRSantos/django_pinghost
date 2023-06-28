const checkboxes = document.querySelectorAll('input[type=checkbox]');
const btnEditar = document.querySelector('#btn-editar');
const btnExcluir = document.querySelector('#btn-excluir');
const btnIncluir = document.querySelector('#btn-incluir');

checkboxes.forEach(checkbox => {
  checkbox.addEventListener('change', () => {
    const checkedCheckboxes = document.querySelectorAll('input[type=checkbox]:checked');
    if (checkedCheckboxes.length === 1) {
      btnEditar.style.display = 'block';
      btnExcluir.style.display = 'block';
    } else if (checkedCheckboxes.length > 1) {
      btnEditar.style.display = 'none';
      btnExcluir.style.display = 'block';
    } else {
      btnEditar.style.display = 'none';
      btnExcluir.style.display = 'none';
    }
  });
});



function confirmarExclusao() {
  // Capturar os checkboxes selecionados
  var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');

  // Verificar se há algum checkbox selecionado
  if (checkboxes.length > 0) {
    // Exibir a mensagem de confirmação
    var confirmacao = confirm('Tem certeza de que deseja excluir ' + checkboxes.length + ' item(s)?');

    // Verificar se o usuário confirmou a exclusão
    if (confirmacao) {
      // Submeter o formulário para realizar a exclusão
      document.getElementById('form-excluir').submit();
    }
  } else {
    alert('Selecione pelo menos um item para excluir.');
  }
}

