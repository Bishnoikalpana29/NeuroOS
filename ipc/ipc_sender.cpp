#include <windows.h>
#include <iostream>
#include <string>

int main()
{
    const char* pipeName = "\\\\.\\pipe\\NeuroOS_IPC";

    std::cout << "====================================\n";
    std::cout << " NeuroOS IPC Sender\n";
    std::cout << "====================================\n";

    // Message sent to the receiver.
    const std::string message =
        "Hello from NeuroOS IPC Sender!";

    std::cout << "Connecting to receiver...\n";

    // Open the receiver's named pipe.
    HANDLE pipe = CreateFileA(
        pipeName,
        GENERIC_WRITE,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (pipe == INVALID_HANDLE_VALUE)
    {
        DWORD errorCode = GetLastError();

        std::cerr << "Error: Could not connect to receiver. "
                  << "Windows error: " << errorCode
                  << std::endl;

        std::cerr << "Make sure the receiver is running first."
                  << std::endl;

        return 1;
    }

    std::cout << "Connected successfully.\n";

    DWORD bytesWritten = 0;

    BOOL success = WriteFile(
        pipe,
        message.c_str(),
        static_cast<DWORD>(message.size()),
        &bytesWritten,
        NULL
    );

    if (!success || bytesWritten != message.size())
    {
        std::cerr << "Error: Could not send the complete message. "
                  << "Windows error: " << GetLastError()
                  << std::endl;

        CloseHandle(pipe);
        return 1;
    }

    std::cout << "Message sent: "
              << message << std::endl;

    // Release the handle.
    CloseHandle(pipe);

    std::cout << "Sender closed successfully.\n";

    return 0;
}