# Xuitter

O Xuitter é uma plataforma Twitter-like minimalista, construída com Django e Django REST Framework e React. Ela permite que os usuários publiquem conteúdo, curtam, repostem, comentem e acessem estatísticas de interação - além de contar com autenticação. 

O objetivo principal do sistema é evidenciar como os testes ajudam na manutenção de um sistema de
software, portanto a alta cobertura de testes no backend foi priorizada.

Para tal, foi utilizado Github Actions para rodar os testes em diversos SOs e versões de Python, além de um automatizador do [Codecov do sistema](https://app.codecov.io/gh/cesarpmorais/Xuitter).

## Integrantes do Grupo
César Morais - 2021031521

Matheus Grandinetti - 2021067496

## Tecnologias utilizadas

- **Django**  
  Framework web Python robusto, utilizado para construir o backend da aplicação, incluindo autenticação, modelos de dados e administração.

- **Django REST Framework (DRF)**  
  Extensão do Django para criação de APIs RESTful. Permite serialização de dados, autenticação via token e construção de endpoints para o frontend consumir.

- **React**  
  Biblioteca JavaScript para construção de interfaces de usuário reativas e componentizadas. Utilizada para o frontend do Xuitter.

- **TypeScript**  
  Superset do JavaScript que adiciona tipagem estática, aumentando a segurança e produtividade no desenvolvimento do frontend React.

- **SQLite**  
  Banco de dados relacional leve, utilizado como padrão no desenvolvimento do backend Django.

- **pytest**  
  Framework de testes para Python, utilizado para garantir a qualidade e cobertura dos testes no backend.

- **Github Actions**  
  Ferramenta de integração contínua (CI) para rodar testes automaticamente em diferentes sistemas operacionais e versões do Python a cada push ou pull request.

- **Codecov**  
  Serviço de análise de cobertura de testes, integrado ao CI para monitorar e exibir a cobertura dos testes do backend.

- **npm concurrently**  
  Pacote Node.js que permite rodar múltiplos comandos (como frontend e backend) simultaneamente durante o desenvolvimento.

## Aprendizados

## Executando o projeto
Usamos o pacote `npm concurrently` para tornar o processo de deploy o mais simples possível. Para executar tanto o frontend quanto o backend:
```
npm install -D concurrently
npm run setup-backend
npm run dev
```

### Backend
### 1. Instalar dependências do projeto
`pip install -r requirements.txt`

### 2. Criar as migrações dos modelos do Django
`python3 manage.py migrate`

### 3. Carregar dados iniciais
`bash load_fixtures.sh`

### 4. Criar superusuário do Django
`python3 manage.py createsuperuser`

### 5. Rodar o servidor
`python3 manage.py runserver`

### Listar Rotas
`python manage.py show_urls --format=table`

### Rodar Testes
`python3 manage.py test`