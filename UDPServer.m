% UDP Server using udpport
clc; clear;

% Get the local IP address from the user
serverIP = '134.88.48.231';
serverPort = 7070; % Port of this server

% Create a UDP server
udpServer = udpport("datagram", "IPV4", "LocalHost", serverIP, "LocalPort", serverPort);
fprintf('UDP Server listening on %s:%d...\n', serverIP, serverPort);

while true
    if udpServer.NumDatagramsAvailable > 0
        % Read incoming message
        datagram = read(udpServer, udpServer.NumDatagramsAvailable, "uint8");
        dataReceived = char(datagram.Data);
        senderAddress = datagram.SenderAddress;
        senderPort = datagram.SenderPort;
        
        fprintf('Received: %s from %s:%d\n', dataReceived, senderAddress, senderPort);
        
        % Echo back the message to the client
        write(udpServer, uint8(dataReceived), senderAddress, senderPort);
        fprintf('Echoed back: %s\n', dataReceived);
    end
    pause(0.1); % Avoid busy looping
end