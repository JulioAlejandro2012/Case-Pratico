// Adiciona o evento de submit ao formulário
document.getElementById("emailForm").addEventListener("submit", async (event) => {
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
    const response = await fetch("http://127.0.0.1:8080/process-email/", {
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
    document.getElementById("categoria").innerText = data.Categoria;
    document.getElementById("resposta").innerText = data.Resposta;
    document.getElementById("results").classList.remove("hidden");

    // (Re)adiciona o evento ao botão de copiar
    const copyBtn = document.getElementById("copy-btn");
    const respostaDiv = document.getElementById("resposta");
    const copiedMsg = document.getElementById("copied-msg");
    if (copyBtn && respostaDiv && copiedMsg) {
      copyBtn.onclick = function () {
        navigator.clipboard.writeText(respostaDiv.innerText).then(() => {
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
