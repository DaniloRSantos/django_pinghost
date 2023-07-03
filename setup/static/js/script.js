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


function excluirHosts() {
  var hostCheckboxes = document.getElementsByName('host_checkbox');
  var selectedIds = [];
  for (var i = 0; i < hostCheckboxes.length; i++) {
      if (hostCheckboxes[i].checked) {
          selectedIds.push(hostCheckboxes[i].value);
      }
  }
  
  if (selectedIds.length > 0) {
    var confirmationMessage = 'IDs dos hosts selecionados para exclusão: ' + selectedIds.join(', ');
    var confirmation = confirm(confirmationMessage);
    
    if (confirmation) {
      document.getElementById('host-ids').value = selectedIds.join(',');
      document.getElementById('form-excluir-hosts').submit();
    }
  } else {
    alert('Nenhum host selecionado para exclusão.');
  }
}


document.getElementById('btn-carregar-coordenada').addEventListener('click', function(event) {
  event.preventDefault(); // Impede o comportamento padrão de envio do formulário
  carregar_coordenadas();
});

function carregar_coordenadas() {
  // ... código existente ...

  request.onload = function () {
    if (request.status >= 200 && request.status < 400) {
      var response = JSON.parse(request.responseText);

      if (response.status === 'OK' && response.results.length > 0) {
        var location = response.results[0].geometry.location;
        var latitudeInput = document.getElementById('latitude');
        var longitudeInput = document.getElementById('longitude');

        latitudeInput.value = location.lat;
        longitudeInput.value = location.lng;

        // Exibir mensagem de sucesso
        var successMessage = document.getElementById('success-message');
        successMessage.textContent = 'Coordenadas carregadas com sucesso.';
        successMessage.style.display = 'block';
      } else {
        // Exibir mensagem de erro
        var errorMessage = document.getElementById('error-message');
        errorMessage.textContent = 'Não foi possível obter as coordenadas para o endereço informado.';
        errorMessage.style.display = 'block';
      }
    } else {
      // Exibir mensagem de erro
      var errorMessage = document.getElementById('error-message');
      errorMessage.textContent = 'Erro ao acessar a API do Google Maps.';
      errorMessage.style.display = 'block';
    }
  };

  request.onerror = function () {
    // Exibir mensagem de erro
    var errorMessage = document.getElementById('error-message');
    errorMessage.textContent = 'Erro de conexão ao acessar a API do Google Maps.';
    errorMessage.style.display = 'block';
  };

  request.send();
}


/*
function editarHost() {
  var hostCheckbox = document.querySelector('input[name="host_checkbox"]:checked');

  if (hostCheckbox) {
    var selectedId = hostCheckbox.value;
    document.getElementById('host-ids').value = selectedId;
    document.getElementById('form-editar-hosts').submit();
  } else {
    alert('Nenhum host selecionado para editar.');
  }
}
*/
