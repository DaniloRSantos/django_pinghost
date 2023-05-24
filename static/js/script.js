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

// script.js
function checkHostAvailability(ipAddress, statusId) {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'check_availability?ip=' + ipAddress, true);
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      console.log(result); // Exibir o objeto JSON no console
    
      var hostAvailable = result.host_available;
      console.log("Host disponível:", hostAvailable); // Exibir o valor de hostAvailable no console

      if (hostAvailable) {
        document.getElementById(statusId).src = '/static/img/ativo.png';
      } else {
        document.getElementById(statusId).src = '/static/img/inativo.png';
      }
    }
  };
  xhr.send();
  };



