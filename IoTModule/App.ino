#include <ESP8266WiFi.h>
#include <DallasTemperature.h>
#include <OneWire.h>
#include <AzureIoTHub.h>
#include <AzureIoTProtocol_MQTT.h>
#include <AzureIoTUtility.h>

#define TEMPERATURE_PIN            D4
#define CARDIO_INPUT_PIN           A0
#define CARDIO_LOMIN_PIN           D0
#define CARDIO_LOPLU_PIN           D1
#define PULSE_PIN                  D2

#define S_ECG_SIZE 226

OneWire oneWire(TEMPERATURE_PIN);
DallasTemperature DS18B20(&oneWire);

static char *connectionString = CONNECTION_STRING;
static char *ssidString = SSID_STRING;
static char *passString = PASS_STRING;


//Temperature string
char temperatureString[6];

//Constants for Cardio
int BPM;
unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval_cardio = 10;       
unsigned long oldtime = 0;
unsigned long newtime = 0;
unsigned long beat_time = 0;
unsigned long cek_beat_time = 0;
int data_now, data_old, delta_data;
bool flag_detek = false;
float HR, HR_old;
float BPM_Array[interval_cardio];
static int increment;

//Message sending and pending
static bool messagePending = false;
static bool messageSending = true;

//Interval for sending and pending
static int interval = INTERVAL;


//IoT Hub client handle
static IOTHUB_CLIENT_LL_HANDLE iotHubClientHandle;

//Message counting for sending
static int messageCount = 1;

static unsigned long remessage = 0;



IPAddress apIP(192, 168, 4, 1);

void setup() {
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);

    //Cardio pin
    pinMode(CARDIO_INPUT_PIN, INPUT);

    // leads for electrodes off detection
    pinMode(CARDIO_LOMIN_PIN, INPUT); // Setup for leads off detection LO -
    pinMode(CARDIO_LOPLU_PIN, INPUT); // Setup for leads off detection LO +
    
    //init Time
    initTime();
    
    //Read SSID, Password and Device Connection String
    readCredentials();
    
    //Connection to Wi-Fi
    Connection(ssidString, passString);
    
    //IoT Hub Client init
    iotHubClientHandle = IoTHubClient_LL_CreateFromConnectionString(connectionString, MQTT_Protocol);
    if (iotHubClientHandle == NULL) { // if hub client handle is failed to create
          Serial.println("Failed on IoTHubClient_CreateFromConnectionString.");
          while (1);
    }
    //Init standart message call and callback functions for IoT Hub client
    IoTHubClient_LL_SetOption(iotHubClientHandle, "product_info", "NodeMCU_ESP8266");
    IoTHubClient_LL_SetMessageCallback(iotHubClientHandle, receiveMessageCallback, NULL);
    IoTHubClient_LL_SetDeviceMethodCallback(iotHubClientHandle, deviceMethodCallback, NULL);
    IoTHubClient_LL_SetDeviceTwinCallback(iotHubClientHandle, twinCallback, NULL);
    
    //Temperature monitoring start
    DS18B20.begin();
    increment = 0;
}

void loop() {
    float temperature = getTemperature();
    float hr = getHR();
    float cardio = getCardio();
    if (increment < interval_cardio) {
        BPM_Array[increment++] = cardio;
    }
    
    
    Serial.printf("Cardio: %lf\n", cardio);
    if (remessage < millis()) {
        if (!messagePending && messageSending) {
            char messagePayload[MESSAGE_MAX_LEN];
            readMessage(messageCount, messagePayload, temperature, hr, BPM_Array, increment);
            sendMessage(iotHubClientHandle, messagePayload);
            memset(BPM_Array, 0.0, interval_cardio);
            messageCount++;
            increment = 0;
        }
        remessage = millis() + interval;
        IoTHubClient_LL_DoWork(iotHubClientHandle);
    }
    
    delay(5);
}