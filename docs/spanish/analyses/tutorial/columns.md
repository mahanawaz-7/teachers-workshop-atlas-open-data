Inicialmente, este conjunto de datos tiene {data} filas o eventos

##### Descripción de las columnas
Esto es lo que significan cada columna del conjunto de datos:
- **EventID**: un identificador único para cada evento registrado en el detector. Cada evento corresponde a una foto instantánea de lo que sucede durante una colisión en el detector.
- **nParticles**: la cantidad total de leptones reconstruidos en el evento. En este conjunto de datos simulado simplificado, nos centramos en eventos con 2, 3 o 4 partículas, lo que es típico para ciertos análisis. En realidad, los recuentos de partículas pueden variar significativamente según el proceso físico que se esté estudiando.
- **Energía leptónica principal (GeV)**: la energía del leptón de mayor energía en un evento, medida en gigaelectronvoltios (GeV). Este valor representa el leptón más energético entre todos los leptones detectados en el evento, lo que proporciona información sobre la dinámica del evento.

A continuación, puedes ver cómo lucen las columnas inicialmente: