import os
import smtplib
import mysql.connector
from datetime import datetime
from mysql.connector import Error
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

smtp_email = os.environ.get('SMTP_EMAIL')
smtp_password = os.environ.get('SMTP_PASSWORD')
mysql_host = os.environ.get('MYSQL_HOST')
mysql_database = os.environ.get('MYSQL_DATABASE')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')

def db_connection():
    try:
        connection = mysql.connector.connect(host=mysql_host, database=mysql_database, user=mysql_user, password=mysql_password)
        if connection.is_connected():
            print('Conexion correcta')
            return connection
    except Error as e:
        print(f"Error al conectar con la DB: {e}")
        return None


def insert_or_update_db_row(file_id, file_name, file_extension, owner_email, visibility, last_modified, connection):
    cursor = connection.cursor()

    query = "SELECT * FROM files WHERE id = %s"
    cursor.execute(query, (file_id,))
    record = cursor.fetchone()

    if record:
        query = """
        UPDATE files
        SET name = %s, owner_email = %s, visibility = %s, last_modified = %s, extension = %s
        WHERE id = %s
        """
        cursor.execute(query, (file_name, owner_email, visibility, last_modified, file_extension, file_id))
        print(f"Archivo {file_name} actualizado")
    else:
        query = """
        INSERT INTO files (id, name, extension, owner_email, visibility, last_modified)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (file_id, file_name, file_extension, owner_email, visibility, last_modified))
    connection.commit()


def add_public_record(connection, file_id, file_name):
    cursor = connection.cursor()
    query = """
    INSERT IGNORE INTO public_files (id, name)
    VALUES (%s, %s)
    """
    cursor.execute(query, (file_id, file_name))
    connection.commit()

    visibility = 0
    cursor = connection.cursor()
    query = """
    UPDATE files
    SET visibility = %s
    WHERE id = %s
    """
    cursor.execute(query, (visibility, file_id))
    connection.commit()


def get_file_extension(extension):
    mime_type_to_extension = {
    # Google Docs formats
    'application/vnd.google-apps.document': 'docx',  # Google Docs
    'application/vnd.google-apps.spreadsheet': 'xlsx',  # Google Sheets
    'application/vnd.google-apps.presentation': 'pptx',  # Google Slides
    'application/vnd.google-apps.form': 'form',  # Google Forms
    'application/vnd.google-apps.drawing': 'drawio',  # Google Drawings
    'application/vnd.google-apps.script': 'gs',  # Google Apps Script
    'application/vnd.google-apps.site': 'site',  # Google Sites
    'application/vnd.google-apps.folder': 'folder',  # Google Drive Folder
    
    # Document formats
    'application/pdf': 'pdf',  # PDF
    'application/msword': 'doc',  # Microsoft Word
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',  # Microsoft Word (OpenXML)
    'application/vnd.ms-excel': 'xls',  # Microsoft Excel
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',  # Microsoft Excel (OpenXML)
    'application/vnd.ms-powerpoint': 'ppt',  # Microsoft PowerPoint
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'pptx',  # Microsoft PowerPoint (OpenXML)
    'application/rtf': 'rtf',  # Rich Text Format
    'application/epub+zip': 'epub',  # ePub eBook
    
    # Image formats
    'image/jpeg': 'jpg',  # JPEG images
    'image/png': 'png',  # PNG images
    'image/gif': 'gif',  # GIF images
    'image/svg+xml': 'svg',  # SVG vector images
    'image/bmp': 'bmp',  # Bitmap images
    'image/tiff': 'tiff',  # TIFF images
    'image/webp': 'webp',  # WebP images
    
    # Audio formats
    'audio/mpeg': 'mp3',  # MP3 audio
    'audio/wav': 'wav',  # WAV audio
    'audio/ogg': 'ogg',  # OGG audio
    'audio/x-aac': 'aac',  # AAC audio
    'audio/x-wav': 'wav',  # WAV audio

    # Video formats
    'video/mp4': 'mp4',  # MP4 video
    'video/x-msvideo': 'avi',  # AVI video
    'video/x-ms-wmv': 'wmv',  # Windows Media Video
    'video/webm': 'webm',  # WebM video
    'video/quicktime': 'mov',  # QuickTime video

    # Compressed formats
    'application/zip': 'zip',  # ZIP archive
    'application/x-rar-compressed': 'rar',  # RAR archive
    'application/x-7z-compressed': '7z',  # 7-Zip archive
    'application/x-tar': 'tar',  # TAR archive
    'application/gzip': 'gz',  # Gzip compressed file,
    'application/x-zip-compressed': 'zip',
    
    # Plain text formats
    'text/plain': 'txt',  # Plain text
    'text/csv': 'csv',  # Comma-separated values
    'text/html': 'html',  # HTML document
    'text/css': 'css',  # CSS file
    'text/javascript': 'js',  # JavaScript file
    'application/json': 'json',  # JSON format

    # Others
    'application/xml': 'xml',  # XML format
    'application/octet-stream': 'bin',  # Binary file
    'application/x-sh': 'sh',  # Shell script
    'application/x-httpd-php': 'php',  # PHP file
    }

    file_extension = mime_type_to_extension.get(extension, 'No extension')
    return file_extension


def main(connector):
    # Listar archivos en Google Drive
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        file_name = file['title']
        extension = file['mimeType']
        file_extension = get_file_extension(extension)
        owner = file['owners'][0]['displayName'] if 'owners' else 'Unknown'
        owner_email = file['owners'][0]['emailAddress'] if 'owners' in file else 'Unknown'
        visibility = file.get('shared', False)
        last_modified = file.get('modifiedDate', 'No disponible')
        formatted_date = datetime.strptime(last_modified, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M:%S")
        file_id = file['id']
        insert_or_update_db_row(file_id, file_name, file_extension, owner_email, visibility, formatted_date, connector)
        if visibility:
            print('Switching permissions...')
            print(owner_email)
            permissions = file.GetPermissions()
            for permission in permissions:
                if permission['role'] != 'owner':  # Si se eliminan los del propietario, este pierde el acceso a sus archivos.
                    file.DeletePermission(permission['id'])
            send_notification_email(owner_email, file['title'])
            add_public_record(connector, file_id, file_name)
        print(f"Nombre: {file['title']}")
        print(f"Extensión: {extension}")
        print(f"Propietario: {owner}")
        print(f"Visibilidad (compartido): {'Sí' if visibility else 'No'}")
        print(f"Fecha de última modificación: {formatted_date}")
        print("="*40)


def send_notification_email(owner_email, file_name):
    if owner_email == 'Unknown':
        return
    smtp_server = 'smtp.office365.com'
    smtp_port = 587

    sender_email = smtp_email
    sender_password = smtp_password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = owner_email
    msg['Subject'] = f"Permisos modificados en {file_name}"
    body = f"Hola, \n\n Se han modificado los permisos de '{file_name}. \n Saludos.'"
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, owner_email, msg.as_string())
        server.quit()
        print(f"Corre enviado a {owner_email}")
    except Exception as e:
        print(f"Error: {e}")



connector = db_connection()

# Autenticación
gauth = GoogleAuth()

gauth.CommandLineAuth()

drive = GoogleDrive(gauth)

if connector:
    main(connector)
    
