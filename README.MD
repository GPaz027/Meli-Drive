# Google Drive Permissions & Log Application

## Instrucciones de uso

1. Rellenar el archivo `.env` con las variables de entorno correspondientes (incluyendo la contraseña y password del mail emisor que notificará al dueño de los archivos de Drive el cambio de permisos. Este mail debe ser de hotmail/outlook por la API que usa SMTP, pero puede cambiarse a Google en la línea 180).
2. Correr la aplicación con sus dos contenedores (Python y MySQL) con `docker-compose up`.
3. Ingresar al contenedor de Python con `docker exec -it CONTAINER_ID bash`
4. Correr el script desde dentro del contenedor con `python personal.py`
5. Verá en la terminal que aparece un enlace a la API de Google, ingresar desde el navegador.
6. Tras autenticarse, en la misma ventana del navegador aparecerá un código que se copiará y se pegará en la terminal del contenedor.
7. El script debería llevar funcionar normalmente.
8. Para revisar la base de datos, se puede acceder al contenedor de MySQL y utilizar MySQL CLI para hacer consultas, para eso `mysql -u USER -pPASSWORD`.
9. En caso de tener archivos públicos, en la tabla `public_files` debería aparecer el registro. Además, debería el dueño del Drive debería haber recibido un correo del emisor configurado en el paso 1, informando el nombre del archivo que sufrió las modificaciones. Finalmente, los permisos del archivo deberían ser privados.

## Documentación consultada

* Acceder archivos de Drive mediante Python: https://stackoverflow.com/questions/67623860/how-to-access-shared-google-drive-files-through-python
* Autenticación de PyDrive2: https://docs.iterative.ai/PyDrive2/oauth/
