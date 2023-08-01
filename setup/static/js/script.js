// Definir o token CSRF como uma variável global
const csrfToken = '{{ csrf_token }}';
const checkboxes = document.querySelectorAll('input[type=checkbox]');
const btnEditar = document.querySelector('#btn-editar');
const btnExcluir = document.querySelector('#btn-excluir');
const btnIncluir = document.querySelector('#btn-incluir');
let map;
const latitudeInput = document.getElementById('latitude');
const longitudeInput = document.getElementById('longitude');


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



btnIncluir.addEventListener('click', () => {
  const ipHost = document.getElementById('ip_host').value;
  const dnsHost = document.getElementById('dns_host').value;
  const nomeHost = document.getElementById('nome_host').value;
  const categoriaHost = document.getElementById('categoria_host').value;

  // Obter os valores dos campos de endereço
  const cep = document.getElementById('cep').value;
  const logradouro = document.getElementById('logradouro').value;
  const numero = document.getElementById('numero').value;
  const complemento = document.getElementById('complemento').value;
  const bairro = document.getElementById('bairro').value;
  const cidade = document.getElementById('cidade').value;
  const estado = document.getElementById('estado').value;
  const latitude = document.getElementById('latitude').value;
  const longitude = document.getElementById('longitude').value;

  // Criar um objeto com os dados do formulário
  const formData = {
    ip_host: ipHost,
    dns_host: dnsHost,
    nome_host: nomeHost,
    categoria_host: categoriaHost,
    cep: cep,
    logradouro: logradouro,
    numero: numero,
    complemento: complemento,
    bairro: bairro,
    cidade: cidade,
    estado: estado,
    latitude: latitude,
    longitude: longitude,
  };

  // Enviar uma requisição POST para a URL de cadastro
  fetch('/cadastro/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: new URLSearchParams(formData).toString()
  })
    .then(response => {
      if (response.ok) {
        // Exibir mensagem de sucesso
        alert('Host cadastrado com sucesso!');
        // Redirecionar para a página desejada, se necessário
      } else {
        throw new Error('Erro ao cadastrar o host.');
      }
    })
    .catch(error => {
      // Lidar com erros de requisição
      console.error(error);
    });
});





// Função auxiliar para obter o valor do token CSRF de um cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

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

function editarHost() {
  console.log('Editar host chamado.');
  var hostCheckbox = document.querySelector('input[name="host_checkbox"]:checked');
  
  // Verifique se hostCheckbox não é nulo
  if (hostCheckbox) {
    var selectedId = hostCheckbox.value;
    console.log('ID do host selecionado:', selectedId);
    document.getElementById('host-id').value = selectedId;
    document.getElementById('form-editar-hosts').submit();
  } else {
    console.log('Nenhum checkbox selecionado.');
  }
}


//------------------------------------------------------------------------------

// Função para inicializar o mapa


  
function preencherCoordenadas(latitude, longitude) {
  console.log('Atualizando campos de coordenadas e mapa');
  latitudeInput.value = latitude;
  longitudeInput.value = longitude;
  const map = window.map.map;
  const marker = window.map.marker;
  const newCoords = new google.maps.LatLng(latitude, longitude);
  marker.setPosition(newCoords);
  map.setCenter(newCoords);
}



