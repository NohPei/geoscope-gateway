# include<WiFi.h>
# include<esp_wifi.h>

///////////////////////////////////////////////////////////////////////////
////////////////////////// CONFIGURATION SECTION //////////////////////////
///////////////////////////////////////////////////////////////////////////

const char WIFI_SSID[] = "The Promised LAN";
const char WIFI_PSK[] = "GoBucks!";

#define SYNC_INTERRUPT digitalPinToInterrupt(D0)
#define SERIAL_BAUD 115200


///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////


volatile int64_t last_pulse_time;

void ARDUINO_ISR_ATTR sync_pulse_isr(void) {
	last_pulse_time = esp_wifi_get_tsf_time(WIFI_IF_STA);
}



void setup() {
	WiFi.mode(WIFI_STA);
	WiFi.begin(WIFI_SSID, WIFI_PSK);

	Serial.begin(SERIAL_BAUD);

	//arm the sync interrupt
	attachInterrupt(SYNC_INTERRUPT, sync_pulse_isr, RISING);
		//trigger the real time sample on the pulse rising edges 


}


void loop() {
	if (Serial.available() > 0) {
		switch (Serial.read()) {
			case 'p':
			case 't':
				Serial.write((uint8_t*) &last_pulse_time, sizeof last_pulse_time);
				//the ESPs are already little-endian, so this should be fine right there.
			default:
				break;
		}
	}


}
