% UDP Client using udpport with Timeout
clc; clear;

% Define server details
serverIP = '134.88.48.231';
serverPort = 7070; % Port of the server

% Create a UDP client
udpClient = udpport("datagram", "IPV4");
fprintf('UDP Client ready to send to %s:%d\n', serverIP, serverPort);

while true
    % Get user input
    message = input('Enter message to send (or type "exit" to quit): ', 's');
    
    if strcmpi(message, 'exit')
        fprintf('Closing connection...\n');
        break;
    end
    
    % Send message
    write(udpClient, uint8(message), serverIP, serverPort);
    fprintf('Sent: %s\n', message);
    
    % Start timer for timeout
    timeout = 10; % Timeout in seconds
    startTime = tic;
    
    % Wait for response with timeout
    while udpClient.NumDatagramsAvailable == 0
        if toc(startTime) > timeout
            fprintf('Request timed out. No response from server.\n');
            break;
        end
        pause(0.1);
    end
    
    % Read response from server if available
    if udpClient.NumDatagramsAvailable > 0
        datagram = read(udpClient, udpClient.NumDatagramsAvailable, "uint8");
        dataReceived = char(datagram.Data);
        senderAddress = datagram.SenderAddress;
        senderPort = datagram.SenderPort;
        
        fprintf('Received: %s from %s:%d\n', dataReceived, senderAddress, senderPort);
    end
end

% Close client
clear udpClient;
