// Definir o token CSRF como uma variável global
const csrfToken = '{{ csrf_token }}';
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

    // Log de depuração
    console.log('IP do Host:', ipHost);
    console.log('DNS do Host:', dnsHost);
    console.log('Nome do Host:', nomeHost);
    console.log('Categoria do Host:', categoriaHost);
    console.log('CEP:', cep);
    console.log('Logradouro:', logradouro);
    console.log('Número:', numero);
    console.log('Complemento:', complemento);
    console.log('Bairro:', bairro);
    console.log('Cidade:', cidade);
    console.log('Estado:', estado);


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
    estado: estado
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


document.getElementById('btn-carregar-coordenada').addEventListener('click', function(event) {
  event.preventDefault(); // Impede o comportamento padrão de envio do formulário
  carregar_coordenadas();
});

function carregar_coordenadas() {
  // Obter os valores dos campos de endereço
  const cep = document.getElementById('cep').value;
  const logradouro = document.getElementById('logradouro').value;
  const numero = document.getElementById('numero').value;
  const complemento = document.getElementById('complemento').value;
  const bairro = document.getElementById('bairro').value;
  const cidade = document.getElementById('cidade').value;
  const estado = document.getElementById('estado').value;

  // Montar a string de endereço
  const endereco = `${logradouro}, ${numero}, ${bairro}, ${cidade}, ${estado}, ${cep}, ${complemento}`;
  const enderecoCodificado = encodeURIComponent(endereco);

  // Construir a URL da API do Google Maps
  const apiKey = '<sua_chave_de_API>';
  const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${enderecoCodificado}&key=${apiKey}`;

  // Fazer a requisição para obter as coordenadas do endereço
  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.status === 'OK' && data.results.length > 0) {
        const location = data.results[0].geometry.location;
        const latitudeInput = document.getElementById('latitude');
        const longitudeInput = document.getElementById('longitude');

        latitudeInput.value = location.lat;
        longitudeInput.value = location.lng;

        // Exibir mensagem de sucesso
        const successMessage = document.getElementById('success-message');
        successMessage.textContent = 'Coordenadas carregadas com sucesso.';
        successMessage.style.display = 'block';
      } else {
        // Exibir mensagem de erro
        const errorMessage = document.getElementById('error-message');
        errorMessage.textContent = 'Não foi possível obter as coordenadas para o endereço informado.';
        errorMessage.style.display = 'block';
      }
    })
    .catch(error => {
      // Exibir mensagem de erro
      const errorMessage = document.getElementById('error-message');
      errorMessage.textContent = 'Erro ao acessar a API do Google Maps.';
      errorMessage.style.display = 'block';
    });
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
