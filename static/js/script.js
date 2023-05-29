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





