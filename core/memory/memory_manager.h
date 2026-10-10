#ifndef MEMORY_MANAGER_H
#define MEMORY_MANAGER_H

#include <vector>

using namespace std;

struct MemoryResult
{
    int pageFaults;
    int pageHits;
    double pageFaultRatio;
};

MemoryResult fifoPageReplacement(
    const vector<int>& pages,
    int frameCount
);

MemoryResult lruPageReplacement(
    const vector<int>& pages,
    int frameCount
);

#endif