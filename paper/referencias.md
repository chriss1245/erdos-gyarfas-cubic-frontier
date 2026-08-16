# Informe bibliográfico EG (agente, 2026-07-25)

## VEREDICTO: frontera cúbica exhaustiva sigue en n=28 (Markström 2004). n=30 es NUEVO.

- Paper más reciente (Carr, arXiv:2605.22844, mayo 2026) aún cita "cubic counterexample ≥30 vertices"
  con Markström 2004 como única fuente computacional. erdosproblems.com/64: ABIERTA (edit. 2026-04-10).
- ÚTIL: Carr 2026 prueba que todo contraejemplo minimal regular es cúbico, ≥4/7 de vértices de grado 3
  ⇒ el caso cúbico es el estructuralmente crítico. Citar para motivar.
- OJO: Pirzada–Shah–Baskoro EJGTA 10(1) 2022 "afirma" la conjetura con argumento inválido — la
  comunidad la trata como abierta. NO citar como demostración; su familia (94 vértices sin C4/C8/C16
  pero CON C32, con puentes) es irrelevante para n=30.

## Referencias clave para nota.tex

1. K. Markström, "Extremal graphs for some problems on cycles in graphs", Congr. Numer. 171 (2004) 177–188.
   Cúbicos hasta 28; 4 grafos de 24 vértices sin C4/C8 (uno planar); general ≥17 (con Royle).
2. Salehi Nowbandegani–Esfandiari, CID 2011: bipartito ≥32.
3. Heckman–Krakovski, Electron. J. Combin. 20(2) (2013) #P7: cúbicos planares 3-conexos.
4. Gao–Shan, Graphs Combin. 38 (2022) 168: P8-free. Hu–Shen, Discrete Math. 347 (2024) 114175: P10-free.
5. Hegde–Sandeep–Shashank, arXiv:2410.22842: P13-free (estado del arte en caminos inducidos).
6. Carr, arXiv:2605.22844 (2026): contraejemplo minimal predominantemente cúbico.
7. Liu–Montgomery (J. AMS 2023): grado mínimo ≥ C absoluta ⇒ ciclo potencia de 2.
8. Bensmail, DMGT 37 (2017): para q≥3 hay cúbicos sin ciclos q-potencia arbitrariamente grandes.
9. McKay–Piperno, J. Symbolic Comput. 60 (2014) 94–112 (nauty).

URLs y detalle completo: ver transcript del agente / este informe se copió del resultado íntegro.
PENDIENTE: informe del 2º agente (fuentes primarias: enunciado exacto EG, premio, Markström íntegro).

# Informe de FUENTES PRIMARIAS (agente 2, 2026-07-25)

## Enunciado exacto (erdosproblems.com/64, verbatim, edit. 2026-04-10)
"Does every finite graph with minimum degree at least 3 contain a cycle of length 2^k for
some k≥2?" — estado FALSIFIABLE/Open, premio $1000 (confirmado en YAML de teorth/erdosproblems).
Erdős & Gyárfás creían la respuesta NEGATIVA (verbatim del sitio); su conjetura fuerte
(∀r: existe grafo con δ≥r sin ciclos 2^k) fue refutada por Liu–Montgomery [LiMo20, JAMS 2023].

## Markström 2004 (PDF PRIMARIO leído: abel.math.umu.se/~klasm/Uppsatser/cycex.pdf)
- "Extremal graphs for some problems on cycles in graphs", Congr. Numer. 171 (2004).
  (Páginas discrepan entre fuentes: 179–192 (UCSD) vs 177–188 (RG) — SIN VERIFICAR.)
- Verbatim: generó "all cubic graphs on less than 29 vertices" (minibaum + fortran propio,
  chequeando ciclos 4/8/16). "No counterexamples to the conjecture was found."
- **TABLA 3 (¡clave!): cúbicos sin C4 y C8: n=24 → 4, n=26 → 23, n=28 → 251.**
  ⇒ NUESTRO CENSO n=26 (23) NO ES INÉDITO — pero COINCIDE 23=23: tercera validación.
  ⇒ Pendiente posible (opcional, 285 core-h): censar n=28 con geng_eg y comparar con 251.
- Los 4 de n=24: uno y solo uno planar, construible desde K4 expandiendo vértices en
  triángulos. OJO: "todos tienen C16" es DEDUCCIÓN (no cita textual del paper).
- Erdős ofreció "$100 for a proof and $50 for a counterexample" (verbatim Markström).
  DISCREPANCIA con los $1000 de erdosproblems.com — en la nota: mencionar ambos.
- Royle: "all relevant graphs on less than 16 vertices" (frontera general ≥16 en primaria;
  el "≥17" que circula es secundario, página de Royle caída — no citar UCSD para fronteras).
- Datación de la conjetura: Markström dice 1995; Bloom la documenta en [Er93] Quaestiones
  Math. 16 (1993) p.343 (no verificado en PDF original, paywall).
- El PDF de Markström está en scratchpad de la sesión: cycex.pdf (copiar a docs/ si se quiere).

## Fuentes Erdős (vía /bibs/ de erdosproblems.com, con MR)
[Er93] Quaestiones Math. 16 (1993) 333–350, p.343. MR1254162 ← primera aparición según Bloom.
[Er94b] Math. Pannon. (1994) 261–269; [Er95] Resenhas (1995) 165–186, p.174;
[Er96] Tatra Mt. Math. Publ. (1996) 7–9; [Er97b] Discrete Math. 165/166 (1997) 227–231;
[Er97c] The Mathematics of Paul Erdős I (1997) 47–67.
[LiMo20] Liu–Montgomery, arXiv:2010.15802; J. Amer. Math. Soc. 36 (2023) 1191–1234.
