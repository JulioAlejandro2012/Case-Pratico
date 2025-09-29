function initializeApp() {
  const form = document.getElementById("emailForm");
  const textElement = document.getElementById("text");
  const fileElement = document.getElementById("file");
  const resultsElement = document.getElementById("results");
  const responseElement = document.getElementById("response");

  // Verifica se todos os elementos necessários estão presentes
  if (!form || !textElement || !fileElement || !resultsElement || !responseElement) {
    console.error("Elementos necessários não encontrados no DOM");
    console.log("Form:", form);
    console.log("Text:", textElement);
    console.log("File:", fileElement);
    console.log("Results:", resultsElement);
    console.log("Response:", responseElement);
    return;
  }

  console.log("Todos os elementos encontrados, inicializando aplicação...");

  // Adiciona o evento de submit ao formulário
  form.addEventListener("submit", async (event) => {
    event.preventDefault();

  // Obtém os elementos do formulário
  const form = event.target;
  const submitButton = form.querySelector('button[type="submit"]');
  const text = document.getElementById("text").value;
  const fileInput = document.getElementById("file");
  const file = fileInput.files.length > 0 ? fileInput.files[0] : null;


  // Validação: exige texto ou arquivo
  if (!text && !file) {
    alert("Por favor, insira um texto ou selecione um arquivo para processar.");
    return;
  }

  // Cria o FormData para envio dos dados
  const formData = new FormData();

  // Adiciona o texto ao FormData, se houver
  if (text) {
    formData.append("text", text);
  }

  // Adiciona o arquivo ao FormData, se houver
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }

  // Feedback visual: desabilita botão e mostra "carregando"
  submitButton.disabled = true;
  submitButton.textContent = "Processando...";
  document.getElementById("results").classList.add("hidden");

  try {
    // Envia requisição para o backend
    const response = await fetch('https://emailclassifierai.onrender.com/process-email/', {
      method: "POST",
      body: formData,
    });

    // Verifica se houve erro na resposta
    if (!response.ok) {
      // Tenta extrair mensagem de erro do backend
      const errorData = await response.json().catch(() => null);
      const errorMessage = errorData?.detail || `Erro do servidor: ${response.status} ${response.statusText}`;
      throw new Error(errorMessage);
    }

    // Recebe e exibe os dados de resultado
    const data = await response.json();
    const responseElement = document.getElementById("response");
    const categoriaElement = document.getElementById("categoria");
    const resultsElement = document.getElementById("results");

    if (responseElement) {
      responseElement.innerText = data.response;
    }
    if (categoriaElement) {
      categoriaElement.innerText = data.classification || "Não classificada";
    }
    if (resultsElement) {
      resultsElement.classList.remove("hidden");
      resultsElement.scrollIntoView({ behavior: "smooth" });

    }

    // (Re)adiciona o evento ao botão de copiar
    const copyBtn = document.getElementById("copy-btn");
    const responseDiv = document.getElementById("response");
    const copiedMsg = document.getElementById("copied-msg");
    if (copyBtn && responseDiv && copiedMsg) {
      copyBtn.onclick = function () {
        navigator.clipboard.writeText(responseDiv.innerText).then(() => {
          copiedMsg.classList.remove("hidden");
          setTimeout(() => {
            copiedMsg.classList.add("hidden");
          }, 1000);
        });
      };
    }
  } catch (error) {
    // Exibe alerta em caso de erro
    alert("Ocorreu um erro: " + error.message);
  } finally {
    // Restaura o botão ao estado original
    submitButton.disabled = false;
    submitButton.textContent = "Processar";
  }
  });
}

// Inicializa a aplicação quando o DOM estiver pronto
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}
