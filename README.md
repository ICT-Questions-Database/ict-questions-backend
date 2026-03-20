# ICT Questions

## Como rodar o backend com Docker

### 1. Clone o repositório
```bash
git clone git@github.com:ICT-Questions-Database/ict-questions-backend.git
cd ict-questions-backend/
```

### 2. Crie os arquivos de ambiente
```bash
cp .env.example .env
cp .env.example .env.docker
```

### 3. Preencha o .env e o env.docker
Preencha os arquivos .env e .env.docker completos

### 4. Suba os containers
```bash
docker compose up --build
```
