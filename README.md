# 📋 Les Triveiros – Inscrição de Equipes

Aplicação em **Streamlit** para inscrição de equipes na Trívia **Les Triveiros**, com integração ao **Firebase Firestore** para persistência dos dados e controle de limite por data.

---

## 🚀 Funcionalidades

- Cadastro de equipes com:
  - Nome da equipe (obrigatório)
  - E-mail do capitão
  - Data escolhida (2 datas disponíeis)
  - Quantidade de membros (1 a 10)
- Controle automático de **limite de 6 equipes por data**
- Contagem de vagas restantes exibida ao usuário
- Dados salvos dinamicamente no **Firebase Firestore**, organizados em **subcoleções por data**
- Página de confirmação após envio bem-sucedido

---

## 🧱 Estrutura do Projeto

les-triveiros/
│
├── app.py # Página inicial – captura nome da equipe
├── firebase_config.py # Inicialização e conexão com Firebase Firestore
├── firebase_key.json # 🔐 Chave da conta de serviço (NÃO subir para repositórios públicos!)
└── pages/
├── inscricoes.py # Formulário de inscrição
└── confirmacao.py # Página de confirmação após envio

yaml
Copy
Edit

---

## 🔐 Requisitos

- Python 3.8+
- Firebase Project com Firestore habilitado
- Conta de serviço com permissão de gravação no Firestore

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/les-triveiros.git
cd les-triveiros
Crie um ambiente virtual e instale as dependências:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
Exemplo de requirements.txt:

txt
Copy
Edit
streamlit
firebase-admin
Baixe sua chave da conta de serviço no Firebase:

Console Firebase > ⚙️ Configurações do Projeto > Contas de serviço > Gerar nova chave privada

Salve o arquivo como firebase_key.json na raiz do projeto

🔥 Firebase Firestore – Organização dos Dados
Os dados são armazenados na coleção inscricoes_trivia, com subcoleções por data:

Copy
Edit
inscricoes_trivia/
   ├── 23 de julho/
   │    └── equipes/
   │         └── (documentos de inscrição)
   └── 25 de julho/
        └── equipes/
             └── (documentos de inscrição)
Cada equipe é um documento com os campos:

equipe: Nome da equipe

data: Data escolhida

email: E-mail do capitão

membros: Número de integrantes

✅ Execução
Rode o app com:

bash
Copy
Edit
streamlit run app.py
⚠️ Avisos de Segurança
Nunca suba o arquivo firebase_key.json para repositórios públicos.

Para produção, defina regras mais restritivas no Firestore para evitar gravações indesejadas.

✨ Futuras melhorias (sugestões)
Exportar inscrições para CSV ou Google Sheets

Adicionar autenticação de admin (via Firebase Auth)

E-mail automático de confirmação para as equipes

Painel para listar equipes inscritas por data

📬 Dúvidas ou sugestões?
Entre em contato com a equipe Les Triveiros!
📧 lestriveiros@gmail.com
📸 @lestriveiros
