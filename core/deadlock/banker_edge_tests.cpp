#include "banker.h"

#include <iostream>

using namespace std;

static int failures = 0;

static void check(const string& name, bool condition)
{
    cout << (condition ? "[PASS] " : "[FAIL] ") << name << "\n";
    if (!condition)
        failures++;
}

int main()
{
    // 1. Zero processes is invalid.
    BankersAlgorithm a(0, 3);
    check("Zero processes rejected", !a.setData({}, {}, {1, 1, 1}));

    // 2. Wrong matrix size is invalid.
    BankersAlgorithm b(2, 2);
    check("Wrong size rejected", !b.setData({{0, 0}}, {{1, 1}, {1, 1}}, {1, 1}));

    // 3. Negative number is invalid.
    BankersAlgorithm c(1, 1);
    check("Negative value rejected", !c.setData({{0}}, {{-1}}, {1}));

    // 4. Single process, single resource: safe.
    BankersAlgorithm d(1, 1);
    d.setData({{0}}, {{5}}, {5});
    SafetyResult sd = d.isSafe();
    check("Single process is safe", sd.safe && sd.safeSequence.size() == 1);

    // 5. Single process needs more than available: unsafe.
    BankersAlgorithm e(1, 1);
    e.setData({{0}}, {{5}}, {2});
    check("Need above available is unsafe", !e.isSafe().safe);

    // 6. Invalid process number in a request.
    BankersAlgorithm f(1, 1);
    f.setData({{0}}, {{5}}, {5});
    check("Invalid process number denied", !f.requestResources(7, {1}).granted);

    // 7. Wrong request length.
    check("Wrong request length denied", !f.requestResources(0, {1, 1}).granted);

    // 8. Denied request must leave the state unchanged.
    BankersAlgorithm g(2, 1);
    g.setData({{1}, {1}}, {{3}, {3}}, {0});
    g.requestResources(0, {1});  // not available, so no change
    check("State unchanged after refused request", !g.isSafe().safe);

    // 9. All-zero request is harmless and granted when state is safe.
    BankersAlgorithm h(1, 1);
    h.setData({{0}}, {{2}}, {2});
    check("Zero request granted", h.requestResources(0, {0}).granted);

    cout << "\n" << (failures == 0 ? "ALL EDGE TESTS PASSED" : "SOME TESTS FAILED") << "\n";
    return failures;
}