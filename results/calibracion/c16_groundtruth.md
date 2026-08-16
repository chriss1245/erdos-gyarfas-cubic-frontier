# Verdad de tierra para calibrar el propagador de C16

Fecha: 2026-08-12. Máquina: 16 cores.

## Motivo

El modo de fallo peligroso de una tubería SAT + propagador de subgrafo prohibido es la
**sobre-restricción**: devuelve 0 en todo y por tanto **pasa cualquier comprobación cuya
respuesta correcta sea 0**. Solo lo detecta un test con respuesta conocida **distinta de
cero**.

Los censos que ya teníamos (cúbicos conexos sin C4/C8: n=24 → 4, n=26 → 23, n=28 → 251)
ejercitan C4 y C8 con respuestas no-cero, pero el camino de **C16** solo aparecía como ceros.
Estos recuentos cierran ese flanco.

## Método

`nauty2_8_9/geng -c -d3 -D3 N` (cúbicos conexos) → `count_c16free.py 16`, que reutiliza el
parser graph6 y el DFS con bitmask de `filter_eg.py` (el mismo código validado en el barrido
n≤30). Recuento independiente con `check_pow2.py` (implementación distinta, networkx).

## Resultados

| n | cúbicos conexos | sin C16 | recuento independiente (networkx) | régimen |
|---|---|---|---|---|
| 14 | 509 | 509 | 509 ✓ | trivial: C16 no cabe en 14 vértices; control de convenio |
| 16 | 4.060 | **219** | 219 ✓ | C16 abarca todo el grafo (= no hamiltonianos) |
| 18 | 41.301 | **1.471** | 1.471 ✓ | **C16 como ciclo propio** — el régimen de interés |
| 20 | 510.489 | **12.709** | 12.709 ✓ | C16 como ciclo propio |
| 22 | 7.319.447 | **52.781** | 52.781 re-testados ✓ (*) | C16 como ciclo propio |

Los totales de cúbicos conexos (509, 4.060, 41.301, 510.489, 7.319.447) coinciden con
OEIS A002851, lo que confirma que las opciones de `geng` seleccionan la clase pretendida
y que el troceado `res/mod` de n=22 (6 trozos) no perdió ni duplicó ningún grafo (además:
52.781 formas canónicas distintas tras `labelg`, cero duplicados).

(*) En n=14-20 el recuento networkx (`recount_nx.py`, 2026-08-16) recorre el censo COMPLETO
re-enumerado con `geng` y reproduce ambos totales — verificación en las dos direcciones. En
n=22 el censo completo (7,3M) no se re-recorrió con networkx: se re-testó individualmente
cada uno de los 52.781 supervivientes (ninguno contiene C16, todos cúbicos de orden 22), y
la dirección "no falta ninguno" descansa en el total del censo + labelg. La coincidencia de
SMS (52.781) NO cuenta como verificación del ancla: SMS es el instrumento bajo calibración.
Ficheros: `recount_nx_n18.txt`, `recount_nx_n20_r*.txt`, `recount_nx_n22_c*.txt`.

Grafos volcados en `n14_no-c16.g6`, `n16_no-c16.g6`, `n18_no-c16.g6`, `n20_no-c16.g6` y
`groundtruth_n22/n22_no-c16_r*.g6` (este directorio) para comparar conjuntos, no solo
cardinales, vía `labelg`.

## Uso previsto

Exigir a SMS (clase cúbica, conexos, prohibiendo **solo** C16) exactamente 219, 1.471 y
12.709 en n=16, 18 y 20. n=18 y n=20 son los tests decisivos: ahí C16 es un ciclo propio, el
mismo régimen en el que trabajaría el propagador en n=32. n=14 solo comprueba que el
propagador no dispara cuando el patrón no cabe.
