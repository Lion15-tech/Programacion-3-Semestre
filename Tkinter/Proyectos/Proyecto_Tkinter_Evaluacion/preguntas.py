# Diccionario para guardar el nombre de los alumnos y su calificación final
alumnos_resultados = {}

# Lista con las preguntas de la evaluación
# Cada elemento tiene la pregunta, las opciones de respuesta y cuál es la correcta
preguntas_evaluacion = [
    {
        "pregunta": "¿Cuál es la función para mostrar texto en pantalla en Python?",
        "opciones": ["echo", "print()", "mostrar()", "console.log()"],
        "respuesta": "print()"
    },
    {
        "pregunta": "¿Qué tipo de dato es el valor 3.14?",
        "opciones": ["int", "string", "float", "boolean"],
        "respuesta": "float"
    },
    {
        "pregunta": "¿Cómo se escribe una lista en Python?",
        "opciones": ["(1, 2, 3)", "{1, 2, 3}", "[1, 2, 3]", "<1, 2, 3>"],
        "respuesta": "[1, 2, 3]"
    },
    {
        "pregunta": "¿Qué palabra se usa para definir una función?",
        "opciones": ["def", "function", "func", "crear"],
        "respuesta": "def"
    }
]