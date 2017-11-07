Instrucciones de Uso Tarea 1:

En el método main del programa Tarea1.py se deben definir los parametros.
En lit = Litoral(a,b,c) se crea el objeto un objeto de la Clase Litoral llamado lit. El parametro a es al ancho de la porción del litoral a modelar, b es el alto y c es el tamaño de la discretización.

A continuación en el main se encuentra lo siguiente:

pi = Process(target = solve(lit,hora)
pi.start()
pif = Process(target = solvefab(lit,hora)
pif.start()

Esto ejecuta de manera progresiva los procesos solicitados (en orden), las instrucciones del estilo pi plotean el litoral (lit) creado anteriormente,sin la planta industrial a la hora indicada, mientras que las instrucciones del estilo pif, hacen lo mismo, pero para el litoral con la planta  industrial.