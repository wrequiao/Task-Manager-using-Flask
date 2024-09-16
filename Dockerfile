# Usa uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o container
COPY requirements.txt .

# Instala as dependências listadas em requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia todos os arquivos da aplicação para o diretório de trabalho do container
COPY . .

# Define a variável de ambiente para indicar que estamos rodando em modo produção
#ENV FLASK_ENV=/todo_project/__ini__.py

ENV FLASK_APP=/todo_project/run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expõe a porta 5000 para acessar a aplicação Flask
EXPOSE 5000

# Comando para rodar a aplicação Flask
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python", "-m", "flask", "run"]

