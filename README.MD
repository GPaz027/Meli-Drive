# Google Drive Permissions & Log Application

## Instrucciones de instalación

1. El script puede ejecutarse de dos formas diferentes, separadas por dos archivos de Python. 
    * **Uso personal (personal.py)**: En este caso el usuario deberá contar con su propia instancia de MySQL, así como con sus credenciales del mail emisor. En este caso, llenar las credenciales manualmente en el archivo de Python (mail y BD).
    * **Uso de prueba (demo.py)**: En este caso, el mail emisor ya está seteado por secrets, y el Drive en donde se buscarán los archivos corresponde a una service account de Google Cloud.
2. Para asegurar las credenciales se tuvo que utilizar Docker Stack, por lo que los secretos deben ser ingresados manualmente antes de empezar.
    * `echo "PASSWORD" | docker secret create mysql_root_password -`
    * `echo "USERNAME" | docker secret create mysql_root_username -`
    * `echo "PASSWORD_EMAIL" | docker secret create smtp_password -`
    * `echo "EMAIL" | docker secret create smtp_email -`
3. Luego se puede buildear el Docker compose: `docker-compose build`
4. Crear el stack `docker stack deploy -c docker-compose.yml meli`
5. Ingresar al contenedor de Python y correr `python demo.py` o `python personal.py`


## Documentación consultada

* Acceder archivos de Drive mediante Python: https://stackoverflow.com/questions/67623860/how-to-access-shared-google-drive-files-through-python
* Autenticación de PyDrive2: https://docs.iterative.ai/PyDrive2/oauth/
