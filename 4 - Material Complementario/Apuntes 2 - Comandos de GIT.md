# Comandos útiles de GIT

<font face = "Arial" size=3 color = "#fff200"> GIT nos permitirá interactuar con el repositorio remoto, que se encuentra en la nube, desde el repositorio local. </font>

## Introducción a GitHub

<font face="Bell MT" size=3 color="#f7d794">
GitHub se trata de un sistema de control de versiones, utilizado por múltiples desarrolladores por su practicidad a la hora de almacenar y construir un proyecto en común. Lo que hace especial a esta plataforma es que permite poder controlar las versiones que se generan en un proyecto, permitiendo que cada desarrollador trabaje sobre un mismo código pero que, al modificarlo, no presente conflictos entre el trabajo que han realizado dos o más programadores sobre un mismo código.

En este sentido, los desarrolladores podrán trabajar libremente sobre un mismo código de manera individual, por lo cual es una buena práctica crear una nueva rama para cada modificación que se realice sobre el proyecto del Repositorio.

A continuación, detallaremos algunos comandos iniciales para controlar nuestro Repositorio.
</font>

## Configuración inicial en nuestra terminal de VS Code

| COMANDO | DESCRIPCIÓN | EJEMPLO |
|---------|-------------|---------|
|git config user.name "nombre_usuario"| Configura el nombre de usuario con el cual se nos identificará en el repositorio.| git config user.name "Gerardo"|
|git config user.password "contraseña"| Permite crear una contraseña.| git config user.password "1234" |
|git config user.email "mi_correo"| Ingresamos el correo con el cual nos hemos registrado en GitHub.| git config user.email "guribururomero@gmail.com"|
|git config user.tipo_config| Permite observar los valores que hemos configurado anteriormente. Podemos colocar luego de user. los identificadores "name, password, email", entre otros.| git config user.name|

## Trabajando con el Repositorio

| COMANDO | DESCRIPCIÓN |
|---------|-------------|
| git pull | Permite importar los cambios que se hayan publicado en el repositorio remoto, una manera de actualizar el repositorio local.|
| git add "archivo" | Nos permitirá agregar un archivo con contenido para lanzarlo al repositorio remoto|
| git commit -m "mensaje" | Permite agregar una descripción de los cambios realizados en un archivo |
| git push origin "rama" | Permite lanzar al repositorio remoto los nuevos cambios que hemos realizado a los archivos con un commit |
| git branch "nombre_rama" | Permite crear una nueva rama |
| git branch | Devuelve una lista de las ramas existentes en el repositorio |
| git checkout "nombre_rama | Nos dirige hacia otra rama que existe en el repositorio |
| git log | Devuelve una lista de todos los cambios que han tenido un commit
