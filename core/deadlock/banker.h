#ifndef BANKER_H
#define BANKER_H

#include <string>
#include <vector>

// Result of running the safety algorithm.
struct SafetyResult
{
    bool safe;                    // true if a safe sequence exists
    std::vector<int> safeSequence; // process numbers in safe order (P0, P1, ...)
};

// Result of a resource request (Resource-Request Algorithm).
struct RequestResult
{
    bool granted;         // true if the request was granted
    std::string message;  // simple explanation of the decision
    std::vector<int> safeSequence; // safe sequence after granting (if granted)
};

class BankersAlgorithm
{
public:
    // n processes, m resource types
    BankersAlgorithm(int processes, int resources);

    // Load the data. Returns false (and sets error) if the sizes are wrong
    // or any number is negative or Max < Allocation.
    bool setData(const std::vector<std::vector<int>>& allocation,
                 const std::vector<std::vector<int>>& maximum,
                 const std::vector<int>& available);

    // Need = Max - Allocation
    void calculateNeed();

    // Safety algorithm: is the current state safe?
    SafetyResult isSafe() const;

    // Resource-Request algorithm: can process p safely get this request?
    // The state is changed only if the request is granted.
    RequestResult requestResources(int process, const std::vector<int>& request);

    // Printing helpers
    void printState() const;
    static void printSafety(const SafetyResult& result);

    // Last error message from setData (empty if no error)
    std::string getError() const;

private:
    int n; // number of processes
    int m; // number of resource types
    std::vector<std::vector<int>> allocation;
    std::vector<std::vector<int>> maximum;
    std::vector<std::vector<int>> need;
    std::vector<int> available;
    std::string error;
};

#endif