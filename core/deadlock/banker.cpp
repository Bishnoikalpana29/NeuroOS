#include "banker.h"

#include <iomanip>
#include <iostream>

BankersAlgorithm::BankersAlgorithm(int processes, int resources)
    : n(processes), m(resources)
{
}

bool BankersAlgorithm::setData(const std::vector<std::vector<int>>& alloc,
                               const std::vector<std::vector<int>>& maxim,
                               const std::vector<int>& avail)
{
    error = "";

    // 1. Check the sizes.
    if (n <= 0 || m <= 0)
    {
        error = "Number of processes and resources must be positive.";
        return false;
    }
    if ((int)alloc.size() != n || (int)maxim.size() != n || (int)avail.size() != m)
    {
        error = "Matrix or vector size does not match processes/resources.";
        return false;
    }

    // 2. Check every number.
    for (int i = 0; i < n; i++)
    {
        if ((int)alloc[i].size() != m || (int)maxim[i].size() != m)
        {
            error = "Each row must have one value per resource type.";
            return false;
        }
        for (int j = 0; j < m; j++)
        {
            if (alloc[i][j] < 0 || maxim[i][j] < 0)
            {
                error = "Negative numbers are not allowed.";
                return false;
            }
            if (maxim[i][j] < alloc[i][j])
            {
                error = "Max cannot be less than Allocation (process P" +
                        std::to_string(i) + ").";
                return false;
            }
        }
    }
    for (int j = 0; j < m; j++)
    {
        if (avail[j] < 0)
        {
            error = "Available resources cannot be negative.";
            return false;
        }
    }

    // 3. Save the data and compute Need.
    allocation = alloc;
    maximum = maxim;
    available = avail;
    calculateNeed();
    return true;
}

void BankersAlgorithm::calculateNeed()
{
    need.assign(n, std::vector<int>(m, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            need[i][j] = maximum[i][j] - allocation[i][j];
}

SafetyResult BankersAlgorithm::isSafe() const
{
    SafetyResult result;
    result.safe = false;

    std::vector<int> work = available;     // resources we currently have free
    std::vector<bool> finished(n, false);  // which processes could finish

    while ((int)result.safeSequence.size() < n)
    {
        bool found = false;

        for (int i = 0; i < n; i++)
        {
            if (finished[i])
                continue;

            // Can process i get everything it still needs?
            bool canRun = true;
            for (int j = 0; j < m; j++)
            {
                if (need[i][j] > work[j])
                {
                    canRun = false;
                    break;
                }
            }

            if (canRun)
            {
                // Process i runs, finishes and gives back its resources.
                for (int j = 0; j < m; j++)
                    work[j] += allocation[i][j];

                finished[i] = true;
                result.safeSequence.push_back(i);
                found = true;
            }
        }

        // No process could run in this pass: the state is unsafe.
        if (!found)
            break;
    }

    result.safe = ((int)result.safeSequence.size() == n);
    if (!result.safe)
        result.safeSequence.clear();
    return result;
}

RequestResult BankersAlgorithm::requestResources(int p, const std::vector<int>& request)
{
    RequestResult result;
    result.granted = false;

    if (p < 0 || p >= n)
    {
        result.message = "Invalid process number.";
        return result;
    }
    if ((int)request.size() != m)
    {
        result.message = "Request must have one value per resource type.";
        return result;
    }
    for (int j = 0; j < m; j++)
    {
        if (request[j] < 0)
        {
            result.message = "Request cannot contain negative numbers.";
            return result;
        }
    }

    // Step 1: request must not exceed what the process declared it needs.
    for (int j = 0; j < m; j++)
    {
        if (request[j] > need[p][j])
        {
            result.message = "DENIED: process exceeded its maximum claim.";
            return result;
        }
    }

    // Step 2: enough resources must be available right now.
    for (int j = 0; j < m; j++)
    {
        if (request[j] > available[j])
        {
            result.message = "WAIT: resources are not available right now.";
            return result;
        }
    }

    // Step 3: pretend to grant the request.
    for (int j = 0; j < m; j++)
    {
        available[j] -= request[j];
        allocation[p][j] += request[j];
        need[p][j] -= request[j];
    }

    // Step 4: keep it only if the new state is still safe.
    SafetyResult check = isSafe();
    if (check.safe)
    {
        result.granted = true;
        result.message = "GRANTED: the system stays in a safe state.";
        result.safeSequence = check.safeSequence;
    }
    else
    {
        // Undo the pretend allocation.
        for (int j = 0; j < m; j++)
        {
            available[j] += request[j];
            allocation[p][j] -= request[j];
            need[p][j] += request[j];
        }
        result.message = "DENIED: granting it would make the system unsafe.";
    }
    return result;
}

void BankersAlgorithm::printState() const
{
    std::cout << "Process   Allocation   Max          Need\n";
    for (int i = 0; i < n; i++)
    {
        std::cout << "P" << std::left << std::setw(8) << i;

        for (int j = 0; j < m; j++)
            std::cout << allocation[i][j] << " ";
        std::cout << "      ";

        for (int j = 0; j < m; j++)
            std::cout << maximum[i][j] << " ";
        std::cout << "      ";

        for (int j = 0; j < m; j++)
            std::cout << need[i][j] << " ";
        std::cout << "\n";
    }

    std::cout << "Available: ";
    for (int j = 0; j < m; j++)
        std::cout << available[j] << " ";
    std::cout << "\n";
}

void BankersAlgorithm::printSafety(const SafetyResult& result)
{
    if (result.safe)
    {
        std::cout << "System is in a SAFE state.\nSafe sequence: ";
        for (size_t i = 0; i < result.safeSequence.size(); i++)
        {
            std::cout << "P" << result.safeSequence[i];
            if (i + 1 < result.safeSequence.size())
                std::cout << " -> ";
        }
        std::cout << "\n";
    }
    else
    {
        std::cout << "System is in an UNSAFE state (no safe sequence exists).\n"
                  << "Deadlock is possible.\n";
    }
}

std::string BankersAlgorithm::getError() const
{
    return error;
}