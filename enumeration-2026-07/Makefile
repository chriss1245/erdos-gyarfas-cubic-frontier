# Builds the pruned generators against an existing nauty 2.8.9 build tree.
#   make NAUTY=/path/to/nauty2_8_9
# The W1 objects (WORDSIZE=32, MAXN=32) are produced by nauty's own `make`.
# WORDSIZE=32 suffices for n <= 32 and is what the published sweeps used.

NAUTY  ?= ../nauty2_8_9
CC     ?= gcc
CFLAGS ?= -O3 -mpopcnt -march=native
DEFS    = -DMAXN=WORDSIZE -DWORDSIZE=32
OBJS    = $(NAUTY)/gtoolsW.o $(NAUTY)/nautyW1.o $(NAUTY)/nautilW1.o \
          $(NAUTY)/naugraphW1.o $(NAUTY)/schreier.o $(NAUTY)/naurng.o

all: geng_eg geng_eg2

# census variant: cubic graphs, no C8 (combine with geng's -f for no C4)
geng_eg: src/prune_c8.c $(NAUTY)/geng.c
	$(CC) -o $@ $(CFLAGS) $(DEFS) -I$(NAUTY) \
	  -DPRUNE=prune_c8 $(NAUTY)/geng.c src/prune_c8.c $(OBJS)

# hunt variant: cubic graphs, no C8 and no C16 (combine with -f for no C4)
geng_eg2: src/prune_c8c16.c $(NAUTY)/geng.c
	$(CC) -o $@ $(CFLAGS) $(DEFS) -I$(NAUTY) \
	  -DPREPRUNE=preprune_c8 -DPRUNE=prune_c8c16 $(NAUTY)/geng.c src/prune_c8c16.c $(OBJS)

test: all
	NAUTY=$(NAUTY) tests/run_tests.sh quick

test-full: all
	NAUTY=$(NAUTY) tests/run_tests.sh full

clean:
	rm -f geng_eg geng_eg2

# checksums of the shipped files (excludes built binaries and caches)
checksums:
	rm -rf src/__pycache__
	find . -type f ! -name SHA256SUMS ! -name geng_eg ! -name geng_eg2 \
	  -exec sha256sum {} \; | sort -k2 > SHA256SUMS

.PHONY: all test test-full clean checksums
