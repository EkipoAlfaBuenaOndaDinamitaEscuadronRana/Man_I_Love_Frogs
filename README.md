# Man I Love Frogs
Compilador de Rosamaría Martínez y Adrián García

## Documentación
Podrás encontrar la documentación en [este archivo](https://docs.google.com/document/d/1uo_Ad0OShn6FkB5r4D5TGvB4o_46ZmvYzrOaCscHmEU/edit?usp=sharing)

## Instalación
Lo primero, es abrir una terminal y clonar el repositorio escribiendo:
```
git clone https://github.com/EkipoAlfaBuenaOndaDinamitaEscuadronRana/Man_I_Love_Frogs.git
```

o en caso de querer clonarlo con ssh puedes usar:
```
git clone git@github.com:EkipoAlfaBuenaOndaDinamitaEscuadronRana/Man_I_Love_Frogs.git
```

Posteriormente, es necesario tener instalado python en tu maquina. Puedes instalarlo [aquí](https://www.python.org/downloads/).

Para correr el proyecto, hay que usar el comando:

```
python3 super_compi.py
```

## Contribuír al proyecto
Si un desarrollador desea contribuir a esta iniciativa, podrá hacerlo creando un Pull Request en el cual deberá de colocar el siguiente formato en la descripción. 

```
[SuperCompi-<# de tarea en trello>](https://trello.com/c/r8XnpNS5/<#-nombre-de-tarea>)

## Descripción
Breve descripción de lo que la tarea hace

## Checklist
* [ ] El código funciona
* [ ] Se añadieron pruebas
* [ ] Las pruebas pasan
* [ ] El codigo pasó por el estilizador de código
```
Una vez terminada la tarea realizada, el resto del equipo aprovará sus cambios y si se considera útil, se mergeará al proyecto

## Pruebas unitarias
Para correr las pruebas unitarias, es necesario usar el comando
```
python3 -m unittest compilador/tests/unit_tests.py
```

## Code Styler
Para este proyecto, usamos [Black](https://github.com/psf/black) como estilizador de código. Cada vez que se mande un Pull Request a revisión, es importante correr alguno de los siguietes dos comandos para poder hacer el merge del PR.
```
black .
```
```
python3 -m black .
```

### Avances de entrega 1
1. Gramatica
2. Expresiones regulares
3. Diagramas descriptivos del lenguaje
4. Lexer
5. Parser

### Avances de entrega 2
1. Directorio de Funciones
2. Tablas de Variables
3. Tabla de Consideraciones Semánticas

### Avances de entrega 3
1. Tabla de Consideraciones Semánticas (programada)
2. Manejo de expresiones
3. Pruebas Unitarias
4. Refactorización de código

### Avances de entrega 4
1. Manejo de expresiones (con correcciones)
2. Solucion de bugs relacionados con parser
3. Asignacion de variables
4. Tabla de variables funcional

### Avances de entrega 5
1. Uso de operadores comparativos en expresiones aritmeticas
2. Consideraciones semanticas implementadas
3. Game engine

### Avances de entrega 6
1. Quadruplos hacen asignaciones
2. Se instauró un code styler
3. Expresiones aritmeticas con tipos

### Avances de entrega 7
1. Quadruplos hacen estatus no lineales y funciones
2. Se hace type checking de toda expresion
3. Se empieza la alocación de memoria y el desarrollo de la vm
4. Refactorización de jerarquia de archivos
