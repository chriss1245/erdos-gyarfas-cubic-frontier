/* Poda Erdős–Gyárfás agresiva: rechaza grafos intermedios con C8 O C16.
 * Válida SOLO para la caza directa de contraejemplos (un contraejemplo no
 * tiene ciclos de longitud potencia de 2); no sirve para censar
 * supervivientes-con-C16 como hace geng_eg.
 *
 * Misma lógica inductiva que prune_c8.c: geng nunca borra aristas y
 * PRUNE(n) implica PRUNE(n-1) pasado, luego todo ciclo nuevo pasa por el
 * vértice n-1. PREPRUNE hace el chequeo barato (C8) antes y más a menudo.
 *
 * Compilar (desde nauty2_8_9/):
 *   gcc -o geng_eg2 -O4 -mpopcnt -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 \
 *       -DPREPRUNE=preprune_c8 -DPRUNE=prune_c8c16 geng.c prune_c8c16.c \
 *       gtoolsW.o nautyW1.o nautilW1.o naugraphW1.o schreier.o naurng.o
 */

#include "gtools.h"

/* ¿camino simple v0->u con depth aristas, extensible a ciclo de longitud L? */
static int
dfs_cyc(graph *g, int v0, int u, setword visited, int depth, int L)
{
    setword w = g[u];
    int x;

    if (depth == L - 1) return (w & bit[v0]) != 0;

    while (w)
    {
        TAKEBIT(x, w);
        if (x != v0 && !(visited & bit[x])
              && dfs_cyc(g, v0, x, visited | bit[x], depth + 1, L))
            return 1;
    }
    return 0;
}

int
preprune_c8(graph *g, int n, int maxn)
{
    int v = n - 1;

    if (n < 8) return 0;
    return dfs_cyc(g, v, v, bit[v], 0, 8);
}

int
prune_c8c16(graph *g, int n, int maxn)
{
    int v = n - 1;

    if (n >= 8 && dfs_cyc(g, v, v, bit[v], 0, 8)) return 1;
    if (n >= 16 && dfs_cyc(g, v, v, bit[v], 0, 16)) return 1;
    return 0;
}
