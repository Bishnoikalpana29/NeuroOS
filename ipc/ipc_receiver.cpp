#include <windows.h>
#include <iostream>
#include <string>

int main()
{
    const char* pipeName = "\\\\.\\pipe\\NeuroOS_IPC";

    std::cout << "====================================\n";
    std::cout << " NeuroOS IPC Receiver\n";
    std::cout << "====================================\n";

    // Create a named pipe for incoming messages.
    HANDLE pipe = CreateNamedPipeA(
        pipeName,
        PIPE_ACCESS_INBOUND,
        PIPE_TYPE_MESSAGE |
        PIPE_READMODE_MESSAGE |
        PIPE_WAIT,
        1,
        0,
        1024,
        0,
        NULL
    );

    if (pipe == INVALID_HANDLE_VALUE)
    {
        std::cerr << "Error: Could not create named pipe. "
                  << "Windows error: " << GetLastError()
                  << std::endl;

        return 1;
    }

    std::cout << "Receiver waiting for sender...\n";

    // Wait for the sender to connect.
    BOOL connected = ConnectNamedPipe(pipe, NULL)
                     ? TRUE
                     : (GetLastError() == ERROR_PIPE_CONNECTED);

    if (!connected)
    {
        std::cerr << "Error: Sender connection failed. "
                  << "Windows error: " << GetLastError()
                  << std::endl;

        CloseHandle(pipe);
        return 1;
    }

    std::cout << "Sender connected successfully.\n";

    char buffer[1025] = {};
    DWORD bytesRead = 0;

    BOOL success = ReadFile(
        pipe,
        buffer,
        1024,
        &bytesRead,
        NULL
    );

    if (success && bytesRead > 0)
    {
        std::string message(buffer, bytesRead);

        std::cout << "Message received: "
                  << message << std::endl;
    }
    else
    {
        std::cerr << "Error: Could not read message. "
                  << "Windows error: " << GetLastError()
                  << std::endl;

        DisconnectNamedPipe(pipe);
        CloseHandle(pipe);
        return 1;
    }

    // Release the pipe resources.
    FlushFileBuffers(pipe);
    DisconnectNamedPipe(pipe);
    CloseHandle(pipe);

    std::cout << "Receiver closed successfully.\n";

    return 0;
}