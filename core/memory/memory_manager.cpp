#include "memory_manager.h"

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>

using namespace std;


// FIFO Page Replacement
MemoryResult fifoPageReplacement(
    const vector<int>& pages,
    int frameCount
)
{
    MemoryResult result = {0, 0, 0.0};

    if (frameCount <= 0 || pages.empty())
    {
        return result;
    }

    vector<int> frames;
    queue<int> insertionOrder;

    cout << "\n========== FIFO PAGE REPLACEMENT ==========\n";

    for (int page : pages)
    {
        cout << "Page " << page << ": ";

        // Check whether the page is already loaded.
        if (find(frames.begin(), frames.end(), page)
            != frames.end())
        {
            result.pageHits++;
            cout << "Page Hit | Frames: ";

        }
        else
        {
            result.pageFaults++;

            if (static_cast<int>(frames.size()) < frameCount)
            {
                frames.push_back(page);
            }
            else
            {
                int oldestPage = insertionOrder.front();
                insertionOrder.pop();

                auto position = find(
                    frames.begin(),
                    frames.end(),
                    oldestPage
                );

                if (position != frames.end())
                {
                    *position = page;
                }
            }

            insertionOrder.push(page);

            cout << "Page Fault | Frames: ";
        }

        for (int frame : frames)
        {
            cout << frame << " ";
        }

        cout << "\n";
    }

    int totalReferences = static_cast<int>(pages.size());

    result.pageFaultRatio =
        static_cast<double>(result.pageFaults)
        / totalReferences;

    cout << "\nFIFO Page Faults: "
         << result.pageFaults << "\n";

    cout << "FIFO Page Hits: "
         << result.pageHits << "\n";

    cout << "FIFO Page-Fault Ratio: "
         << result.pageFaultRatio << "\n";

    return result;
}


// LRU Page Replacement
MemoryResult lruPageReplacement(
    const vector<int>& pages,
    int frameCount
)
{
    MemoryResult result = {0, 0, 0.0};

    if (frameCount <= 0 || pages.empty())
    {
        return result;
    }

    vector<int> frames;
    vector<int> lastUsed;

    cout << "\n========== LRU PAGE REPLACEMENT ==========\n";

    for (int time = 0; time < static_cast<int>(pages.size()); time++)
    {
        int page = pages[time];

        cout << "Page " << page << ": ";

        auto position = find(
            frames.begin(),
            frames.end(),
            page
        );

        if (position != frames.end())
        {
            result.pageHits++;

            int index = static_cast<int>(
                position - frames.begin()
            );

            lastUsed[index] = time;

            cout << "Page Hit | Frames: ";
        }
        else
        {
            result.pageFaults++;

            if (static_cast<int>(frames.size()) < frameCount)
            {
                frames.push_back(page);
                lastUsed.push_back(time);
            }
            else
            {
                int leastRecentlyUsedIndex = 0;

                for (int i = 1;
                     i < static_cast<int>(lastUsed.size());
                     i++)
                {
                    if (lastUsed[i]
                        < lastUsed[leastRecentlyUsedIndex])
                    {
                        leastRecentlyUsedIndex = i;
                    }
                }

                frames[leastRecentlyUsedIndex] = page;

                lastUsed[leastRecentlyUsedIndex] = time;
            }

            cout << "Page Fault | Frames: ";
        }

        for (int frame : frames)
        {
            cout << frame << " ";
        }

        cout << "\n";
    }

    int totalReferences = static_cast<int>(pages.size());

    result.pageFaultRatio =
        static_cast<double>(result.pageFaults)
        / totalReferences;

    cout << "\nLRU Page Faults: "
         << result.pageFaults << "\n";

    cout << "LRU Page Hits: "
         << result.pageHits << "\n";

    cout << "LRU Page-Fault Ratio: "
         << result.pageFaultRatio << "\n";

    return result;
}