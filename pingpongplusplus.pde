/*
 * PingPong++
 * -------------
 * By Michael Bernstein (msbernst@mit.edu) and Xiao Xiao (x_x@mit.edu)
 * 
 * The board configuration should look like below.
 * Numbers are the default pin locations on the Arduino.
 *
 * |-------------------------------|
 * |  1         2  |  5          6 |
 * |               |               |
 * |               |               |
 * |  4         3  |  8          7 |
 * |-------------------------------|
 */

struct Hit {
  int upperLeft;
  int upperRight;
  int lowerLeft;
  int lowerRight;
  unsigned long startTime;
  char side;
  boolean reported;  // have we sent it off via serial yet?
};

int leftPins[] = {
  6, 7, 8, 9}; // clockwise from top left
int rightPins[] = {
  2, 3, 4, 5}; // clockwise from top left

const unsigned long NO_RECORD = -1;
const unsigned long TIMEOUT_BETWEEN_HITS = 300000; // in millis
const char LEFT = 'l';
const char RIGHT = 'r';

Hit curHit = { 
  NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, NO_RECORD, LEFT, false};

void setup() {
  Serial.begin(9600);
  //Serial.println("Starting PingPongPlusPlus");
  for (int i = 0; i < 4; i++) {
    int pinNumber = leftPins[i];
    pinMode(pinNumber, INPUT);
  }
  for (int i = 0; i < 4; i++) {
    int pinNumber = rightPins[i];
    pinMode(pinNumber, INPUT);
  }
}

void loop() {
  readPins(leftPins, LEFT);
  readPins(rightPins, RIGHT);
  
  if (isCompleteHit(&curHit) && !curHit.reported) {
    // print the current hit status
    Serial.print("hit: {");
    Serial.print(curHit.upperLeft);
    Serial.print(" ");
    Serial.print(curHit.upperRight);
    Serial.print(" ");
    Serial.print(curHit.lowerRight);
    Serial.print(" ");
    Serial.print(curHit.lowerLeft);
    Serial.print(" ");
    Serial.print(curHit.side);
    Serial.println("}");
    
    curHit.reported = true;
  }

  if (hitTimedOut()) {
    // create a new hit
    //Serial.println("The old hit timed out.  Starting new hit.");
    Hit newHit;
    newHit.upperLeft = newHit.upperRight = newHit.lowerLeft = newHit.lowerRight = NO_RECORD;
    newHit.side = LEFT;
    newHit.startTime = NO_RECORD;
    newHit.reported = false;
    
    curHit = newHit;
  }
  
}

/*
 * Looks at each pin on the side to see if it is LOW (e.g., registered a hit) 
 * and updates the Hit data structure if so.
 */
void readPins(int* pinList, char curSide) {
  for (int i = 0; i < 4; i++) {
    int pinNumber = pinList[i];
    int pinValue = digitalRead(pinNumber);
    //Serial.println(pinValue);

    if (pinValue == LOW) {
      //Serial.println("high detected");
      unsigned long detectionTime = micros();
      if (curHit.startTime == NO_RECORD) {
        curHit.startTime = detectionTime;
        curHit.side = curSide;
      }
      // add this data to the existing hit
      updateCorner(pinNumber, curSide, detectionTime);
     }
  }
}

/*
 * Updates the current hit data structure in the correct corner, given the pin number
 */
void updateCorner(int pinNumber, char curSide, unsigned long detectionTime) {
  int *sidePins;
  if (curSide == RIGHT) {
    sidePins = rightPins;
  }
  else {
    sidePins = leftPins;
  }
  
  if (pinNumber == sidePins[0] && curHit.upperLeft == NO_RECORD) {
    curHit.upperLeft = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[1] && curHit.upperRight == NO_RECORD) {
    curHit.upperRight = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[2] && curHit.lowerRight == NO_RECORD) {
    curHit.lowerRight = detectionTime - curHit.startTime;
  }
  else if (pinNumber == sidePins[3] && curHit.lowerLeft == NO_RECORD) {
    curHit.lowerLeft = detectionTime - curHit.startTime;
  }
}

boolean hitTimedOut() {
  unsigned long time_since = micros() - curHit.startTime;
  boolean timed_out = (time_since >= TIMEOUT_BETWEEN_HITS);
  return (curHit.startTime == NO_RECORD || timed_out);
}

boolean isCompleteHit(struct Hit *hit) {
  return hit->upperLeft != NO_RECORD && hit->upperRight != NO_RECORD && hit->lowerRight != NO_RECORD && hit->lowerLeft != NO_RECORD;
}
