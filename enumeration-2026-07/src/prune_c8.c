/* Poda Erdős–Gyárfás: rechaza grafos intermedios que contienen un C8.
 *
 * geng añade vértices en orden 0,1,2,... y nunca borra aristas, así que
 * "contiene C8" es monótona y podar es correcto. Además PRUNE(n) implica
 * que PRUNE(n-1) pasó, luego todo C8 nuevo pasa por el vértice n-1:
 * basta un DFS de longitud exactamente 8 anclado ahí.
 *
 * Compilar (desde nauty2_8_9/):
 *   gcc -o geng_eg -O4 -mpopcnt -march=native -DMAXN=WORDSIZE -DWORDSIZE=32 \
 *       -DPRUNE=prune_c8 geng.c prune_c8.c gtoolsW.o nautyW1.o nautilW1.o \
 *       naugraphW1.o schreier.o naurng.o
 */

#include "gtools.h"

/* ¿camino simple de v0 a u con `depth` aristas extensible a C8? */
static int
dfs_c8(graph *g, int v0, int u, setword visited, int depth)
{
    setword w = g[u];
    int x;

    if (depth == 7) return (w & bit[v0]) != 0;

    while (w)
    {
        TAKEBIT(x, w);
        if (x != v0 && !(visited & bit[x])
              && dfs_c8(g, v0, x, visited | bit[x], depth + 1))
            return 1;
    }
    return 0;
}

int
prune_c8(graph *g, int n, int maxn)
{
    int v = n - 1;

    if (n < 8) return 0;
    return dfs_c8(g, v, v, bit[v], 0);
}
