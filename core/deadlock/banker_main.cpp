#include "banker.h"

#include <iostream>
#include <vector>

using namespace std;

// Prints a heading, then the state and its safety result.
static void showCase(const string& title, BankersAlgorithm& bank)
{
    cout << "\n==================================================\n";
    cout << title << "\n";
    cout << "==================================================\n";
    bank.printState();
    cout << "\n";
    BankersAlgorithm::printSafety(bank.isSafe());
}

int main()
{
    // ---------- Test 1: classic safe state (5 processes, 3 resources) ----------
    BankersAlgorithm bank1(5, 3);
    bool ok = bank1.setData(
        {{0, 1, 0}, {2, 0, 0}, {3, 0, 2}, {2, 1, 1}, {0, 0, 2}},   // Allocation
        {{7, 5, 3}, {3, 2, 2}, {9, 0, 2}, {2, 2, 2}, {4, 3, 3}},   // Max
        {3, 3, 2});                                                 // Available
    if (!ok)
    {
        cout << "Error: " << bank1.getError() << "\n";
        return 1;
    }
    showCase("TEST 1: Safe state", bank1);

    // ---------- Test 2: valid request that is granted ----------
    cout << "\n--- P1 requests (1, 0, 2) ---\n";
    RequestResult r = bank1.requestResources(1, {1, 0, 2});
    cout << r.message << "\n";
    if (r.granted)
        cout << "New state is safe. Sequence found by the algorithm.\n";

    // ---------- Test 3: request denied because it would be unsafe ----------
    cout << "\n--- P4 requests (3, 3, 0) ---\n";
    r = bank1.requestResources(4, {3, 3, 0});
    cout << r.message << "\n";

    cout << "\n--- P0 requests (0, 2, 0) ---\n";
    r = bank1.requestResources(0, {0, 2, 0});
    cout << r.message << "\n";

    // ---------- Test 4: request above maximum claim ----------
    cout << "\n--- P1 requests (5, 0, 0) ---\n";
    r = bank1.requestResources(1, {5, 0, 0});
    cout << r.message << "\n";

    // ---------- Test 5: unsafe state ----------
    BankersAlgorithm bank2(3, 2);
    ok = bank2.setData(
        {{1, 0}, {0, 1}, {1, 1}},   // Allocation
        {{3, 2}, {2, 3}, {3, 3}},   // Max
        {0, 0});                    // Available
    if (!ok)
    {
        cout << "Error: " << bank2.getError() << "\n";
        return 1;
    }
    showCase("TEST 5: Unsafe state", bank2);

    // ---------- Test 6: invalid input ----------
    cout << "\n==================================================\n";
    cout << "TEST 6: Invalid input (Max < Allocation)\n";
    cout << "==================================================\n";
    BankersAlgorithm bank3(1, 1);
    if (!bank3.setData({{5}}, {{3}}, {1}))
        cout << "Rejected correctly: " << bank3.getError() << "\n";

    return 0;
}