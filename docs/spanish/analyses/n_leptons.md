## Número de leptones en el estado final
Cuando se producen partículas en un colisionador de partículas, a menudo decaen inmediatamente en otras partículas. Estos productos del decaimiento son lo que detectamos y analizamos. Al estudiar las partículas en el estado final (las visibles después de todos los decaimientos), podemos inferir qué partículas se crearon originalmente en la colisión.

Para entender esto mejor, veamos los [diagramas de Feynman](https://cds.cern.ch/record/2791333/files/Feynman%20Diagrams%20-%20ATLAS%20Physics%20Cheat%20Sheet%20in%20Spanish%20%7C%20Diagramas%20de%20Feynman.pdf). Estos diagramas ayudan a visualizar las interacciones de las partículas. En los ejemplos siguientes, el tiempo corre de izquierda a derecha, es decir que para leerlos, se ven **de izquierda a derecha**: las partículas de la izquierda se producen en la colisión y las partículas de la derecha son los productos de decaimientos finales que detectamos.

Aquí hay un diagrama que muestra un bosón Z decayendo en dos leptones (ya sean electrones o muones):

![Decaimiento del bosón Z en dos leptones](images/Z_decay_{theme}.png)

En el diagrama anterior, la línea ondulada de la izquierda representa el bosón Z, producido en la colisión. A medida que nos movemos hacia la derecha, el bosón Z alcanza un vértice, donde decae a dos leptones. Estos leptones se muestran como líneas rectas, etiquetadas como ℓ, que podrían ser electrones o muones. Las flechas en las líneas indican si cada leptón es una partícula o una antipartícula: las flechas que apuntan a la derecha muestran partículas, mientras que las flechas que apuntan a la izquierda muestran antipartículas. Este diagrama ilustra cómo un bosón Z decae a un par de leptones con cargas opuestas, que detectamos en nuestro experimento.

Los procesos más complejos, como el decaimiento del bosón de Higgs, pueden dar como resultado más leptones en el estado final. Por ejemplo, aquí hay un bosón de Higgs decayendo en dos bosones Z, cada uno de los cuales decae a su vez en dos leptones:

![Decaimiento del bosón de Higgs en bosones Z y leptones](images/higgs4l_decay_{theme}.png)

Una línea discontinua a la izquierda representa el bosón de Higgs (H). El bosón de Higgs decae en un vértice en dos bosones Z, que se muestran como líneas onduladas etiquetadas como Z. Cada bosón Z luego decae en dos leptones, tal como en el primer diagrama. Nuevamente, las líneas rectas con flechas representan los leptones, y la dirección de la flecha indica si son partículas o antipartículas. En total, este proceso da como resultado cuatro leptones, que son las partículas finales que detectamos. Este diagrama demuestra cómo el decaimiento de un bosón de Higgs puede dar lugar a múltiples partículas a través de una cascada de interacciones.

En muchos procesos de partículas, las partículas se producen a menudo en pares. Por ejemplo, el bosón Z decae a dos leptones (una partícula y su antipartícula) porque interactúa por igual con la materia y la antimateria. De manera similar, el bosón de Higgs produce múltiples leptones cuando su decaimiento involucra partículas intermedias como los bosones Z, que a su vez decae a pares de leptones.

El conjunto de datos que estás analizando contiene eventos con diferentes cantidades de leptones. A continuación, se muestra un gráfico que muestra la distribución de los recuentos de leptones en todo el conjunto de datos. Los eventos con menos leptones son más comunes porque los procesos más simples, como los que involucran a los bosones W o Z, ocurren con mayor frecuencia que los más raros y complejos, como el decaimiento del bosón de Higgs.

![Distribución de la cantidad de leptones detectados por evento en el conjunto de datos](images/lepton_plot_{theme}_{lumi}.png)

Estudia los diagramas de Feynman y los datos anteriores. Dependiendo de si te estás enfocando en encontrar el bosón Z o el bosón de Higgs, selecciona la cantidad de leptones que esperas observar en tu estado final.

> [!CAUTION]
Al seleccionar el número de leptones, se aplican criterios adicionales para garantizar la calidad de los datos. Los leptones deben estar bien separados de otras partículas (**aislados**) e **identificados con precisión** como electrones o muones. Dado que a veces las partículas pueden identificarse erróneamente, utilizamos niveles de identificación para medir nuestra confianza en su tipo. Además, solo se incluyen los eventos con señales lo suficientemente fuertes como para activar el sistema de selección del detector (llamados disparadores), específicamente para identificar electrones o muones.
> [!END]