# Modelo Conejo-Zorro

Primer trabajo para el ramo de Modelamiento Computacional. Consiste en simular un entorno en donde existen depredadores (zorros) y presas (conejos), mediante una matriz bidimensional que indica las posiciones de los sujetos, y "ticks" que representan el transcurso del tiempo.

La idea es graficar las poblaciones de zorros y conejos, y llegar al comportamiento que se vería según las ecuaciones de Lotka-Volterra, sin forzarlo de manera explícita.

Entonces se establece, de manera muy básica, que: 

\-zorros se comen a conejos.

\-tanto conejos como zorros pueden reproducirse, pero para los zorros está sujeto a su alimentación.

\-tanto conejos como zorros mueren después de un tiempo.

La ejecución requiere tener python (fue testeado en python 3.11, pero debería funcionar con 3.10 y anteriores).
También requiere tener algunas librerías básicas como numpy y matplotlib.

Cómo ejecutarlo:

python main.py
