# Yoruba TTS - Text to Speech en Yoruba

Este proyecto permite convertir texto en Yoruba a audio utilizando modelos de transformación (Transformers). Además, incluye una interfaz web sencilla con Flask 
para generar, reproducir y descargar archivos de audio. Está diseñado para ser utilizado en un entorno de servidor con Apache2 y Gunicorn.

---

## Requisitos previos

Asegúrate de tener los siguientes componentes instalados en tu sistema:
- **Ubuntu 22.04**
- **Python 3.11**
- **Apache2**
- **Gunicorn**
- Acceso a Internet para descargar modelos y dependencias.

---

## Instalación

### 1. Configurar Python 3.11
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python3.11-distutils
sudo apt install python3.11-venv
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.11
sudo python3.11 -m pip install --upgrade pip

### 2. Instalar dependencias del proyecto

pip install flask transformers accelerate scipy torch gunicorn

### 3. Instalar y configurar Apache2

sudo apt-get install apache2
sudo a2enmod proxy proxy_http
sudo systemctl restart apache2

### 4. Estructura del proyecto
Organiza los archivos del proyecto de la siguiente manera:

/ruta/a/tu/proyecto/
│
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    └── audio/
## Uso

### 1. Ejecutar la aplicación localmente
Para probar la aplicación localmente, ejecuta:
python3.11 app.py

### 2. Configurar Gunicorn como servicio

# Crea un archivo de servicio para Gunicorn en /etc/systemd/system/tts-yoruba.service:

[Unit]
Description=Gunicorn instance to serve TTS Yoruba
After=network.target

[Service]
User=gpuchi
Group=gpuchi
WorkingDirectory=/ruta/a/tu/proyecto
ExecStart=/home/gpuchi/.local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target

# Inicia y habilita el servicio:

sudo systemctl start tts-yoruba
sudo systemctl enable tts-yoruba

## 3. Configurar Apache2 para redirigir a Gunicorn
# Crea un archivo en /etc/apache2/sites-available/tts-yoruba.conf:

<VirtualHost *:80>
    ServerName tu-dominio.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/

    ErrorLog ${APACHE_LOG_DIR}/tts-yoruba-error.log
    CustomLog ${APACHE_LOG_DIR}/tts-yoruba-access.log combined
</VirtualHost>

# Habilita el sitio y reinicia Apache:

sudo a2ensite tts-yoruba.conf
sudo systemctl restart apache2

### Contribuciones
## 1. Crea un fork del proyecto.
## 2. Crea una rama para tu funcionalidad:

git checkout -b nueva-funcionalidad

## 3. Realiza los cambios y haz un commit:

git commit -m "Añadir nueva funcionalidad"

## 4. Envía tus cambios:

git push origin nueva-funcionalidad

## 5. Abre un Pull Request.

### Créditos

Desarrollado por gpuchi como parte de un esfuerzo para preservar y facilitar el uso del idioma Yoruba en tecnologías modernas.

### Licencia

Este proyecto se distribuye bajo la licencia MIT.


