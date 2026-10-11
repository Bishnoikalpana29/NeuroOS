#include "banker.h"

#include <iostream>
#include <vector>

using namespace std;

int main()
{
    int n, m;

    // Read the number of processes and resource types.
    if (!(cin >> n >> m) || n <= 0 || m <= 0)
    {
        cout << "ERROR: Invalid process or resource count.\n";
        return 1;
    }

    vector<vector<int>> allocation(n, vector<int>(m));
    vector<vector<int>> maximum(n, vector<int>(m));
    vector<int> available(m);

    // Read Allocation matrix.
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (!(cin >> allocation[i][j]))
            {
                cout << "ERROR: Invalid Allocation input.\n";
                return 1;
            }
        }
    }

    // Read Maximum matrix.
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            if (!(cin >> maximum[i][j]))
            {
                cout << "ERROR: Invalid Maximum input.\n";
                return 1;
            }
        }
    }

    // Read Available vector.
    for (int j = 0; j < m; j++)
    {
        if (!(cin >> available[j]))
        {
            cout << "ERROR: Invalid Available input.\n";
            return 1;
        }
    }

    BankersAlgorithm banker(n, m);

    if (!banker.setData(allocation, maximum, available))
    {
        cout << "ERROR: " << banker.getError() << "\n";
        return 1;
    }

    // Calculate Need = Maximum - Allocation.
    cout << "NEED\n";

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < m; j++)
        {
            cout << maximum[i][j] - allocation[i][j];

            if (j + 1 < m)
                cout << " ";
        }

        cout << "\n";
    }

    // Run the existing Banker's Algorithm.
    SafetyResult result = banker.isSafe();

    if (result.safe)
    {
        cout << "SAFE\n";
        cout << "SEQUENCE ";

        for (size_t i = 0; i < result.safeSequence.size(); i++)
        {
            cout << "P" << result.safeSequence[i];

            if (i + 1 < result.safeSequence.size())
                cout << " -> ";
        }

        cout << "\n";
    }
    else
    {
        cout << "UNSAFE\n";
        cout << "No safe sequence exists.\n";
    }

    return 0;
}