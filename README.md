# Replicacion de la app


Para inicializar el proyecto debes tener Ollama instalado
Ingresa al siguiente link [click aqui](https://ollama.com/), una vez descargado Ollama debes añadir los modelos utilizados.  

Debes hacer esto en tu consola:
```
ollama pull llama2:7b
```
```
ollama pull nomic-embed-text:latest
```
Una vez con ambos modelos corriendo local, debes asegurarte que Ollama este corriendo verifica que estas sobre el proyecto, segun sea tu editor de codigo preferido
```
cd /home/tu_usuario/descargas/chat-rag/src
```
Este es un ejemplo de ruta, debes usar tu ruta.  

Una vez en src, debes usar el siguiente comando:
```
uv run streamlit run app.py
```
# Contexto del documento adjuntado  
El documento adjuntado habla sobre la Migracion en Colombia, desde diferentes puntos de vista como por ejemplo los derechos humanos, las estrategias locales, regionales y nacionales con respecto al tema
, tambien se plantean los desafios para los años siguientes, teniendo en cuenta que es un documento de 2022, y hace una comparacion entre migrates retornados y migrantes externos.  

Algunos ejemplos de pregunta y respuesta esperada:

>Hablame de la migracion en Colombia y las estrategias que tomaron los gobiernos de turno  

Y su respuesta:

>La migración en Colombia es un tema complejo y multifacético, como en muchos otros países. Según el Banco Mundial, en 2020, Colombia recibió a más de 170,000 migrantes internacionales, lo que representa el 0.6% de la población total del país.
>
>Desde el punto de vista económico, la migración puede tener un impacto positivo en la economía colombiana, ya que los migrantes pueden aportar nuevos conocimientos, habilidades y experiencia laboral, lo que puede mejorar la productividad y la competitividad del país. Según el Banco Mundial, los ingresos de los migrantes en Colombia aumentan de tres a seis veces cuando se trasladan de países de ingresos bajos a países de ingresos altos.
>
>Sin embargo, la migración también puede tener un impacto negativo en la economía colombiana, como la competencia por los mismos empleos y la presión sobre los recursos naturales y públicos. Además, la migración puede generar tensiones sociales y culturales, especialmente si no se abordan adecuadamente las necesidades y expectativas de los migrantes.
>
>En cuanto a las estrategias que han tomado los gobiernos de turno para abordar la migración en Colombia, existen varias iniciativas que buscan fomentar el desarrollo económico y social de los territorios de origen de los migrantes, así como también promover la integración de los mismos en la sociedad colombiana. Algunas de estas estrategias incluyen:
>
>1. Programas de capacitación y formación profesional para los migrantes, con el objetivo de mejorar sus habilidades y conocimientos laborales.
>2. Iniciativas de empleo y generación de oportunidades laborales en los territorios de origen de los migrantes, para reducir la brecha económica entre estos y Colombia.
>3. Fomento del turismo y el desarrollo cultural en los territorios de origen de los migrantes, para promover su identidad y patrimonio cultural.
>4. Iniciativas de integración social y cultural para fomentar la convivencia pacífica entre los migrantes y la población local, a través de programas de educación cultural y social.
>5. Fortalecimiento de las redes de apoyo y seguridad para proteger los derechos de los migrantes y promover su integración en la sociedad colombiana.
>
>En resumen, la migración en Colombia es un tema complejo que requiere abordar desde diversas perspectivas, incluyendo el punto de vista económico, social y cultural. Los gobiernos de turno han implementado varias estrategias para abordar este fenómeno, pero es importante continuar trabajando en la integración y convivencia pacífica entre los migrantes y la población local.

Otro ejemplo interesante,

>¿Cuáles son los temas principales de este documento?

Respuesta esperada: 

>Los temas principales del documento son:
>
>1. La creación del Estatuto de Protección Temporal para Migranes Venezolanos (ETPV) por el Gobierno colombiano, que permitirá ofrecer amparo legal a los migrantes, acceso a derechos y una oportunidad para planear un futuro personal.
>2. La generosidad de la decisión del Gobierno colombiano en abrir estas puertas para los migrantes venezolanos, calificada por gobiernos y asociaciones internacionales.
>3. El discurso de Gabriel García Márquez tras recibir la Orden del Águila Azteca en la Ciudad de México, en el que agradece al país que lo recibió tantas veces en el trascurso de su vida, en diferentes circunstancias y siempre con los brazos abiertos.
>4. La importancia de las acciones prominentes desarrolladas por extranjeros en favor de la comunidad mexicana o de la humanidad en general, como reconocido en la creación del Estatuto de Protección Temporal para Migranes Venezolanos (ETPV).

### Nota: Se añadio test de carga de documentos PDF y prueba del Embedding en test_pdf_loader.py y test_embedding.py
