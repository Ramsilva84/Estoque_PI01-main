# 🛠️ Como rodar o projeto

Este repositório contém dois projetos separados:

- `Backend/`: API em **Python**.
- `Frontend/controle-estoque/`: Aplicação **React**.

---

> ℹ️ Este README foi criado para facilitar a execução **local** dos projetos do repositório original.  
> Para acessar o repositório principal, acesse:  
> 👉 [Repositório original](https://github.com/Vyce96/Estoque_PI01)

---

## ⚙️ Backend (Python)

### Pré-requisitos
- Python 3.10+
- pip

### Passos

```bash
cd Backend
pip install -r .\requirements.txt
py .\app.py 
```

---

## 🖥️ Frontend (React)

### Pré-requisitos
- Node.js 18+
- npm

### Passos

```bash
cd Frontend/controle-estoque
npm install
npm run dev         

---

## Endpoints principais (Backend)

- `POST /login` → autenticação de usuário  
- `GET /produtos` → lista todos os produtos  
- `POST /produtos` → adiciona novo produto  
- `PUT /produtos/<id>` → atualiza um produto existente  
- `DELETE /produtos/<id>` → remove um produto

---

## Deploy em Nuvem

O backend foi hospedado temporariamente na nuvem utilizando a plataforma **Replit**.  
Isso permitiu a execução do servidor Flask em ambiente remoto e a geração de uma URL pública,  
que pôde ser acessada para realizar testes dos endpoints em qualquer lugar.

---
