# 📋 Les Triveiros – Inscrição de Equipes

Aplicação em **Streamlit** para inscrição de equipes na Trívia **Les Triveiros**, com integração ao **Firebase Firestore** para persistência dos dados e controle de limite por data.

---

## 🚀 Funcionalidades

- Cadastro de equipes com:
  - Nome da equipe (obrigatório)
  - E-mail do capitão
  - Data escolhida (Dependendo datas disponíeis)
  - Quantidade de membros (1 a 10)
- Controle automático de **limite de equipes por data**
- Contagem de vagas restantes exibida ao usuário
- Dados salvos dinamicamente no **Firebase Firestore**, organizados em **subcoleções por data**
- Página de confirmação após envio bem-sucedido

---

## 🔐 Requisitos

- Python 3.8+
- Firebase Project com Firestore habilitado
- Conta de serviço com permissão de gravação no Firestore


✅ Execução
Rode o app com:

bash
Copy
Edit
streamlit run app.py

✨ Futuras melhorias (sugestões)
Exportar inscrições para CSV ou Google Sheets

E-mail automático de confirmação para as equipes


📬 Dúvidas ou sugestões?
Entre em contato com a equipe Les Triveiros!
📧 lestriveiros@gmail.com
📸 @lestriveiros
