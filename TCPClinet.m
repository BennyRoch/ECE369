% TCP Client using tcpclient
clc; clear;

% Define server details
serverIP = '134.88.48.231'; % Change this to the actual server IP
serverPort = 55000;

% Create a TCP client
client = tcpclient(serverIP, serverPort, "Timeout", 10);
fprintf('Connected to TCP Server at %s:%d\n', serverIP, serverPort);

while true
    % Get user input
    message = input('Enter message to send (or type "exit" to quit): ', 's');

    if strcmpi(message, 'exit')
        fprintf('Closing connection...\n');
        break;
    end

    % Send message
    writeline(client, message);
    fprintf('Sent: %s\n', message);

    % Read server response
    response = readline(client);
    fprintf('Server responded: %s\n', response);
end

% Close client
clear client;
