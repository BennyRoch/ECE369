% UDP Client using udpport
clc; clear;

% Define server details
serverIP = '134.88.49.223';
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
    
    % Wait for response
    while udpClient.NumDatagramsAvailable == 0
        pause(0.1);
    end
    
    % Read response from server
    datagram = read(udpClient, udpClient.NumDatagramsAvailable, "uint8");
    dataReceived = char(datagram.Data);
    senderAddress = datagram.SenderAddress;
    senderPort = datagram.SenderPort;
    
    fprintf('Received: %s from %s:%d\n', dataReceived, senderAddress, senderPort);
end

% Close client
clear udpClient;