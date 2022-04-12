#ifdef ESP8266
# include<ESP8266WiFi.h>
#include<ESPAsyncUDP.h>
#else
# include<WiFi.h>
#include<AsyncUDP.h>
#endif

#include "esp_undocumented.h"

#ifdef BROADCAST_TSF
# if defined(ESP8266)
#  include<ESPAsyncUDP.h>
# elif defined(ESP32)
#  include<AsyncUDP.h>
# else
#  undef BROADCAST_TSF
# endif
#endif //defined(BROADCAST_TSF)


volatile int64_t last_pulse_time;
 
///////////////////////////////////////////////////////////////////////////
////////////////////////// CONFIGURATION SECTION //////////////////////////
///////////////////////////////////////////////////////////////////////////

const char WIFI_SSID[] = "The Promised LAN";
const char WIFI_PSK[] = "GoBucks!";

#define SYNC_INTERRUPT digitalPinToInterrupt(D0)
#define SERIAL_BAUD 115200

#define TSF_SEND_INTERVAL_MS 1000
#define TSF_SEND_PORT 2323
//#define BROADCAST_TSF
//uncomment to enable broadcasting the TSF regularly over UDP

///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////

void IRAM_ATTR sync_pulse_isr(void) {
	last_pulse_time = ESP_WDEV_TIMESTAMP();
}

#ifdef BROADCAST_TSF
AsyncUDP time_broadcaster;
uint32_t next_send_time_ms = 0;
#endif //defined(BROADCAST_TSF)


void setup() {
	WiFi.mode(WIFI_STA);
#ifdef ESP8266
	WiFi.setPhyMode(WIFI_PHY_MODE_11N);
#endif
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

#ifdef BROADCAST_TSF
	if (millis() >= next_send_time_ms) {
		next_send_time_ms = millis() + TSF_SEND_INTERVAL_MS;
		int64_t time_to_send = ESP_WDEV_TIMESTAMP();
		time_broadcaster.broadcastTo((uint8_t*) &time_to_send, sizeof time_to_send, TSF_SEND_PORT);
	}
#endif


}
