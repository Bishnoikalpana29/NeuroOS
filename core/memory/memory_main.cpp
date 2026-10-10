#include <iostream>
#include <vector>
#include "memory_manager.h"

using namespace std;

void runTest(const vector<int>& pages, int frameCount, const string& testName)
{
    cout << "\n====================================\n";
    cout << testName << "\n";
    cout << "Number of Frames: " << frameCount << "\n";

    cout << "Page Reference String: ";

    if (pages.empty())
    {
        cout << "(Empty)";
    }
    else
    {
        for (int page : pages)
        {
            cout << page << " ";
        }
    }

    cout << "\n";

    MemoryResult fifoResult =
        fifoPageReplacement(pages, frameCount);

    MemoryResult lruResult =
        lruPageReplacement(pages, frameCount);

    cout << "\n---------- TEST RESULTS ----------\n";
    cout << "Algorithm\tPage Faults\tPage Hits\n";

    cout << "FIFO\t\t"
         << fifoResult.pageFaults << "\t\t"
         << fifoResult.pageHits << "\n";

    cout << "LRU\t\t"
         << lruResult.pageFaults << "\t\t"
         << lruResult.pageHits << "\n";

    cout << "----------------------------------\n";
}

int main()
{
    // Test 1: Normal reference string
    vector<int> normalPages = {
        7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2
    };

    runTest(normalPages, 3, "TEST 1: NORMAL INPUT");

    // Test 2: Only one memory frame
    vector<int> oneFramePages = {
        1, 2, 3, 1, 2
    };

    runTest(oneFramePages, 1, "TEST 2: ONE FRAME");

    // Test 3: Repeated page references
    vector<int> repeatedPages = {
        1, 1, 1, 1, 1
    };

    runTest(repeatedPages, 3, "TEST 3: REPEATED PAGES");

    // Test 4: Empty reference string
    vector<int> emptyPages = {};

    runTest(emptyPages, 3, "TEST 4: EMPTY INPUT");

    cout << "\nAll test cases executed.\n";

    return 0;
}