#include <AndroidAccessory.h>

AndroidAccessory acc("LitTl3.1 Industries",
	"Vinc3nt",
	"Vinc3nt Arduino Accessory",
	"0.1",
	"http://www.LitTl31.com",
	"0000000012345678");

void setup() {
	// put your setup code here, to run once:
	Serial.begin(115200);
	Serial.print("\r\nStart");

	Serial.println("beginning");	
        //acc.powerOn();
        acc.begin();

}

void loop() {
	byte err;
	byte idle;
	static byte count = 0;
	byte msg[3];
	long touchcount;

	Serial.println("connecting");
	// put your main code here, to run repeatedly:
	if (acc.isConnected()){
		Serial.println("connected");
                //int len = acc.read(msg, sizeof(msg), 1);     
                int len = acc.read();     
	}
	else{
		Serial.println("NOT Connected");
	}

	delay(5000);	
}
