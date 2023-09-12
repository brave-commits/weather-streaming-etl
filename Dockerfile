FROM python:3.11.4

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y --no-install-recommends \
    unixodbc-dev \
    unixodbc \
    libpq-dev \
    sudo
RUN curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc 
RUN curl https://packages.microsoft.com/config/debian/11/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list 
RUN sudo apt-get update 
RUN sudo ACCEPT_EULA=Y apt-get install -y msodbcsql18   
RUN sudo ACCEPT_EULA=Y apt-get install -y mssql-tools18 
RUN echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> /.bashrc 
RUN . ~/.bashrc 
RUN sudo apt-get install -y unixodbc-dev 
RUN sudo apt-get install -y libgssapi-krb5-2 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "run.py" ]