% TCP Server using tcpserver
clc; clear;

% Define server parameters
serverPort = 55000; % Choose a port

% Create the TCP server
server = tcpserver("134.88.48.231", serverPort, "Timeout", 30);
fprintf('TCP Server listening on port %d...\n', serverPort);

while true
    if server.NumBytesAvailable > 0
        % Read incoming message
        dataReceived = readline(server);
        fprintf('Received: %s\n', dataReceived);

        % Echo back the message to the client
        writeline(server, dataReceived);
        fprintf('Echoed back: %s\n', dataReceived);
    end
    pause(0.1); % Avoid busy looping
end

