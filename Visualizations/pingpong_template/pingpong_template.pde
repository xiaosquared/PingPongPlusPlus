/**
 * Processing Template for PingPong++ Visualisations
 *
 *
 *                       < x      (0,0) 
 *                  -----------
 *                  |         |
 *                  |    L    |   y
 *                  |         |   v
 *                  |         |
 * Projector     -----------------
 *                  |         |
 *               ^  |         |
 *               y  |    R    |
 *                  |         |
 *            (0,0) -----------
 
 */
 
import processing.serial.*;

String winSerial = "COM7";                        // serial port on windows
String macSerial = "/dev/tty.usbserial-A9005d9p"; // serial port on os x  
 
BallPositionSensor sensor;
BallPositionUploader uploader;
String tableName = "My Table";

float screenMultiplier = 10.5;

int tableWidth = 60;
int tableHeight = 54;

PVector ballPosition = new PVector(0, 0);

void setup() {
  size(int(2*tableHeight*screenMultiplier), int(tableWidth*screenMultiplier));
  background(0);
  
  sensor = new BallPositionSensor(this, macSerial, "../../coefficients-left.txt", "../../coefficients-right.txt");
  uploader = new BallPositionUploader(tableName);
}

void draw() {
  background(0);
  
  Hit ballLocation = sensor.readHit();
  if (ballLocation != null) {
    ballPosition = ballLocation.getPixelVector();
    if (!sensor.debug) {
      //uploader.uploadHit(ballLocation.x, ballLocation.y, ballLocation.isRightSide);
    }
  }
  
  drawBallPosition();
}

void drawBallPosition() {
  noFill();
  stroke(200, 100, 100, 200);
  ellipse (ballPosition.x, ballPosition.y, 44, 44);
  ellipse (ballPosition.x, ballPosition.y, 43, 43);
  ellipse (ballPosition.x, ballPosition.y, 42, 42);
  ellipse (ballPosition.x, ballPosition.y, 41, 41);
  ellipse (ballPosition.x, ballPosition.y, 40, 40);
}

void mouseClicked() {
  ballPosition = new PVector(mouseX, mouseY);
}

