# Calibración de SMS contra enumeración exhaustiva (clase cúbica, conexos)

Fecha: 2026-08-12. Máquina: 16 cores, ejecución monohilo por caso.
Binarios: SMS `464f12f`, CaDiCaL `b023aaf`, Glasgow `1217f5b`
(el script de SMS clona Glasgow en HEAD, no en un commit fijado: hay que anotarlo,
no suponerlo — el `abd331a` que documenta Balaji tampoco lo fija su propia imagen).
Driver: `sms_run.py` (grado exactamente 3, `--connected`, `--cutoff 0`).

## Por qué hacen falta anclas NO-CERO

El fallo peligroso de una tubería SAT + propagador es la **sobre-restricción**: devuelve 0
en todo y por tanto **pasa cualquier test cuya respuesta correcta sea 0**. Solo lo detecta
un test con respuesta conocida distinta de cero. Ocho de las doce anclas de abajo lo son.

## Anclas

| orden | prohibido | esperado | SMS | fuente de la verdad de tierra |
|---|---|---|---|---|
| 10 | C16 | 19 | **19** ✓ | `geng` (cúbicos conexos) |
| 14 | C16 | 509 | **509** ✓ | `geng` (C16 no cabe: control de convenio) |
| 16 | C16 | 219 | **219** ✓ | `geng` + doble detector (bitmask / networkx) |
| 18 | C16 | 1.471 | **1.471** ✓ | ídem |
| 20 | C16 | 12.709 | **12.709** ✓ | ídem |
| 24 | C4, C8 | 4 | **4** ✓ | Markström Tabla 3 + barrido propio |
| 26 | C4, C8 | 23 | **23** ✓ | ídem |
| 28 | C4, C8 | 251 | **251** ✓ | ídem |
| 24 | C4, C8, C16 | 0 | **0** ✓ | barrido propio |
| 26 | C4, C8, C16 | 0 | **0** ✓ | barrido propio |
| 28 | C4, C8, C16 | 0 | **0** ✓ | Markström + barrido propio |
| 30 | C4, C8, C16 | 0 | **0** ✓ | barrido propio (348,7 core-horas) |

**Comparación a nivel de conjunto**, no solo de cardinal: los grafos que emite SMS en n=24 y
n=26 coinciden exactamente con los de `geng` tras etiquetado canónico con `labelg`
(4 = 4 y 23 = 23, cero diferencias).

## Robustez

| eje | comprobación | resultado |
|---|---|---|
| codificación de cardinalidad | contador **totalizer** en vez de secuencial | n=18/C16 → 1.471 ✓; n=28/C4,C8 → 251 ✓; n=30 → 0 ✓; n=32 → 0 ✓ |
| cutoff de minimalidad | por defecto (200000) frente a 0 | n=32 → 0 en ambos (607 s con cutoff, 505 s sin él) ✓ |

## Controles positivos EN LOS ÓRDENES DE LA FRONTERA

La calibración cubre los fallos independientes del orden (encoding, patrones, propagadores:
el mismo código corre en todos los órdenes). No cubre una rotura dependiente del orden que
hiciera la fórmula insatisfacible por vacuidad a partir de cierto tamaño. Por eso se lanzan
consultas de **existencia** prohibiendo solo {C4, C8}, donde se sabe que hay soluciones:

| orden | prohibido | esperado | SMS | tiempo |
|---|---|---|---|---|
| 24 | C4, C8 | SAT | **SAT** (rc=10) ✓ | 2,4 s |
| 32 | C4, C8 | SAT | **SAT** ✓ | 64,8 s |
| 36 | C4, C8 | SAT | **SAT** ✓ | 73,2 s |
| 38 | C4, C8 | SAT | **SAT** ✓ | 9,1 s |
| 40 | C4, C8 | SAT | **SAT** ✓ | 108,8 s |

Los ceros de la frontera no son, por tanto, un artefacto de que la tubería deje de encontrar
nada en órdenes grandes.

## Comparación con el aparato de validación de Balaji

Su `verification.md` declara: un ancla no-cero (n=10 prohibiendo **solo C4** → 5), la
reproducción del baseline n≤16 (ceros), acuerdo con su solver CEGAR propio hasta n=19,
totalizer en n=17/20/22/25, colex en n=17/20 (n=22/25 agotaron 55 min), y controles positivos
prohibiendo solo C4 en n=10/17/20/25/30. Sus propagadores de **C8 y C16 nunca se enfrentan a
una respuesta no-cero conocida**, y no hay comparación a nivel de conjunto.
