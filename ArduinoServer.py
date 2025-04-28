#include<Wire.h>
#include<SPI.h>
#include<MFRC522.h>
#include<LiquidCrystal_I2C.h>
#include<WiFiS3.h>

// =================== LCD & RFID ===================
LiquidCrystal_I2C lcd(0x27,16,2);
#define SS_PIN 10
#define RST_PIN 9
#define LED_G 4
#define LED_R 5
#define BUZZER 2
#define lock 3
#define Btn 6

MFRC522 mfrc522(SS_PIN,RST_PIN);

// LCD refresh variables
unsigned long lastLCDRefresh=0;
const unsigned long LCD_REFRESH_INTERVAL=30000;

// =================== Wi-Fi Setup ===================
char ssid[]="iPhone";
char pass[]="TinTable95";
int status=WL_IDLE_STATUS;

WiFiServer server(12345);
WiFiClient clients[4];
int numClients=0;

const String validUsername="admin";
const String validPassword="super_secret";

bool isAuthenticated=false;
unsigned long lastActivityTime=0;
const unsigned long timeoutDuration=2*60*1000;

// =================== LCD Functions ===================
void initializeLCD(){
  lcd.init();
  lcd.begin(16,2);
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Scan Your RFID ");
  lcd.setCursor(0,1);
  lcd.print("   Door Locked   ");
}

void refreshLCD(){
  lcd.init();
  lcd.begin(16,2);
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Scan Your RFID ");
  lcd.setCursor(0,1);
  lcd.print("   Door Locked   ");
}

// =================== Setup ===================
void setup(){
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(LED_G,OUTPUT);
  pinMode(LED_R,OUTPUT);
  pinMode(BUZZER,OUTPUT);
  noTone(BUZZER);
  pinMode(Btn,INPUT_PULLUP);
  pinMode(lock,OUTPUT);

  initializeLCD();

  if(WiFi.status()!=WL_NO_MODULE){
    Serial.println("Attempting to connect to WiFi...");
    status=WiFi.begin(ssid,pass);
    delay(5000);
    if(status==WL_CONNECTED){
      Serial.println("Connected to WiFi!");
      Serial.print("IP Address: ");
      Serial.println(WiFi.localIP());
      server.begin();
    }else{
      Serial.println("Failed to connect to WiFi. Running in standalone mode.");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Standalone Mode");
      lcd.setCursor(0,1);
      lcd.print("   Door Locked   ");
      delay(2000);
      refreshLCD();
    }
  }else{
    Serial.println("WiFi module not found. Running in standalone mode.");
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Standalone Mode");
    lcd.setCursor(0,1);
    lcd.print("   Door Locked   ");
    delay(2000);
    refreshLCD();
  }
}

// =================== Logging Functions ===================
void broadcastLog(String message){
  String logMessage="LOG: "+String(millis()/1000)+"s - "+message;
  for(int i=0;i<numClients;i++){
    if(clients[i]&&clients[i].connected()){
      clients[i].println(logMessage);
    }
  }
  Serial.println(logMessage);
}

// =================== Door Unlock Logic ===================
void unlockDoor(String source){
  digitalWrite(LED_G,HIGH);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Door Unlocked ");
  lcd.setCursor(0,1);
  lcd.print("  Please Enter  ");
  tone(BUZZER,2000);delay(100);noTone(BUZZER);delay(50);
  tone(BUZZER,2000);delay(100);noTone(BUZZER);
  digitalWrite(lock,HIGH);
  delay(3000);
  digitalWrite(lock,LOW);
  digitalWrite(LED_G,LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Door Locked ");
  lcd.setCursor(0,1);
  lcd.print(" Scan RFID Card ");
  delay(2000);
  completeSystemReset();
  broadcastLog("Door unlocked by "+source);
}

// =================== System Reset Function ===================
void completeSystemReset(){
  mfrc522.PCD_Init();
  lcd.init();
  lcd.begin(16,2);
  lcd.backlight();
  digitalWrite(LED_G,LOW);
  digitalWrite(LED_R,LOW);
  digitalWrite(lock,LOW);
  noTone(BUZZER);
  if(status==WL_CONNECTED){
    isAuthenticated=false;
  }
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Scan Your RFID ");
  lcd.setCursor(0,1);
  lcd.print("   Door Locked   ");
}

void printInitialCommandMenu(WiFiClient&client){
  client.println("--- Command Menu ---");
  client.println("- login:<username>:<password>   -> Log in to the system");
  client.println("- quit                          -> Disconnect");
}

void printAuthenticatedCommandMenu(WiFiClient&client){
  client.println();
  client.println("Command Menu:");
  client.println("- open_sesame      -> Unlock the door (LED ON)");
  client.println("- close_sesame     -> Lock the door (LED OFF)");
  client.println("- logout           -> Log out");
  client.println("- quit             -> Disconnect");
  client.println();
}

// =================== Main Loop ===================
void loop(){
  if(millis()-lastLCDRefresh>LCD_REFRESH_INTERVAL){
    refreshLCD();
    lastLCDRefresh=millis();
  }
  if(status==WL_CONNECTED){
    handleWiFi();
  }
  handleButton();
  handleRFID();
}

// =================== Wi-Fi Command Handling ===================
void handleWiFi(){
  if(numClients<4){
    WiFiClient newClient=server.available();
    if(newClient){
      for(int i=0;i<4;i++){
        if(!clients[i]||!clients[i].connected()){
          clients[i]=newClient;
          numClients++;
          broadcastLog("New client connected");
          newClient.println("Welcome to the Arduino Door Lock System");
          printInitialCommandMenu(newClient);
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("Client Connected");
          lcd.setCursor(0,1);
          lcd.print("   Door Locked   ");
          delay(2000);
          refreshLCD();
          break;
        }
      }
    }
  }
  for(int i=0;i<numClients;i++){
    if(clients[i]&&clients[i].connected()){
      if(clients[i].available()){
        String receivedMessage="";
        while(clients[i].available()){
          char c=clients[i].read();
          receivedMessage+=c;
          if(c=='\n')break;
        }
        receivedMessage.trim();
        broadcastLog("Received from client: "+receivedMessage);
        lastActivityTime=millis();
        if(receivedMessage.startsWith("login:")){
          int firstColon=receivedMessage.indexOf(':');
          int secondColon=receivedMessage.indexOf(':',firstColon+1);
          if(secondColon>0){
            String username=receivedMessage.substring(firstColon+1,secondColon);
            String password=receivedMessage.substring(secondColon+1);
            if(username==validUsername&&password==validPassword){
              isAuthenticated=true;
              String loginResponse="Login successful!\n\n";
              loginResponse+="Command Menu:\n";
              loginResponse+="- open_sesame      -> Unlock the door (LED ON)\n";
              loginResponse+="- close_sesame     -> Lock the door (LED OFF)\n";
              loginResponse+="- logout           -> Log out\n";
              loginResponse+="- quit             -> Disconnect\n";
              clients[i].print(loginResponse);
              broadcastLog("Client authenticated as: "+username);
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print("Login Successful");
              lcd.setCursor(0,1);
              lcd.print("   Door Locked   ");
              delay(2000);
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print(" Scan Your RFID ");
              lcd.setCursor(0,1);
              lcd.print("   Door Locked   ");
            }else{
              clients[i].println("Invalid username or password.");
              broadcastLog("Failed login attempt");
              printInitialCommandMenu(clients[i]);
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print("Login Failed");
              lcd.setCursor(0,1);
              lcd.print("   Try Again   ");
              delay(2000);
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print(" Scan Your RFID ");
              lcd.setCursor(0,1);
              lcd.print("   Door Locked   ");
            }
          }else{
            clients[i].println("Incorrect login format. Use: login:<username>:<password>");
          }
        }else if(receivedMessage=="quit"){
          clients[i].println("Goodbye.");
          broadcastLog("Client disconnected");
          clients[i].stop();
          numClients--;
          refreshLCD();
        }else if(receivedMessage=="open_sesame"&&isAuthenticated){
          unlockDoor("WiFi client");
          clients[i].println("Door unlocked (via Wi-Fi)");
          printAuthenticatedCommandMenu(clients[i]);
        }else if(receivedMessage=="close_sesame"&&isAuthenticated){
          digitalWrite(lock,LOW);
          clients[i].println("Door locked.");
          broadcastLog("Door locked via WiFi");
          printAuthenticatedCommandMenu(clients[i]);
          refreshLCD();
        }else if(receivedMessage=="logout"&&isAuthenticated){
          isAuthenticated=false;
          clients[i].println("You have been logged out.");
          broadcastLog("Client logged out");
          printInitialCommandMenu(clients[i]);
          refreshLCD();
        }else{
          clients[i].println("Unknown command or not authenticated.");
          if(isAuthenticated){
            printAuthenticatedCommandMenu(clients[i]);
          }else{
            printInitialCommandMenu(clients[i]);
          }
        }
      }
    }else{
      numClients--;
      broadcastLog("Client disconnected");
      refreshLCD();
    }
  }
}

// =================== Button Unlock Handling ===================
void handleButton(){
  static bool buttonPressed=false;
  static unsigned long lastButtonPress=0;
  const unsigned long debounceDelay=50;

  int buttonState=digitalRead(Btn);
  static int lastButtonState=HIGH;
  if(buttonState!=lastButtonState){
    Serial.print("Button state changed to: ");
    Serial.println(buttonState==LOW?"LOW (Pressed)":"HIGH (Released)");
    lastButtonState=buttonState;
  }
  if(buttonState==LOW){
    if(!buttonPressed&&(millis()-lastButtonPress>debounceDelay)){
      buttonPressed=true;
      lastButtonPress=millis();
      Serial.println("Button press detected - unlocking door");
      broadcastLog("Access granted via button");
      unlockDoor("button");
    }
  }else{
    buttonPressed=false;
  }
}

// =================== RFID Unlock Handling ===================
void handleRFID(){
  if(!mfrc522.PICC_IsNewCardPresent())return;
  if(!mfrc522.PICC_ReadCardSerial())return;

  Serial.print("UID tag :");
  String content="";
  for(byte i=0;i<mfrc522.uid.size;i++){
    Serial.print(mfrc522.uid.uidByte[i]<0x10?" 0":" ");
    Serial.print(mfrc522.uid.uidByte[i],HEX);
    content.concat(String(mfrc522.uid.uidByte[i]<0x10?" 0":" "));
    content.concat(String(mfrc522.uid.uidByte[i],HEX));
  }
  Serial.println();
  content.toUpperCase();

  if(content.substring(1)=="AC 6A BD 21"){
    broadcastLog("Access granted via RFID");
    delay(500);
    unlockDoor("RFID");
  }else{
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(" Invalid RFID ");
    lcd.setCursor(0,1);
    lcd.print("   Try Again   ");
    broadcastLog("Access denied - Invalid RFID tag");
    for(int i=0;i<3;i++){
      digitalWrite(LED_R,HIGH);
      tone(BUZZER,1500);
      delay(500);
      digitalWrite(LED_R,LOW);
      noTone(BUZZER);
      delay(100);
    }
    completeSystemReset();
  }
}
