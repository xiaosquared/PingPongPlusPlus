int TABLE_WIDTH = 60;
int TABLE_HEIGHT = 54;

float screenMultiplier = 11;
int points[][] = {{6, 6}, {6, 18}, {6, 30}, {6, 42},
              {18, 6}, {18, 18}, {18, 30}, {18, 42},
              {30, 6}, {30, 18}, {30, 30}, {30, 42},
              {42, 6}, {42, 18}, {42, 30}, {42, 42},
              {54, 6}, {54, 18}, {54, 30}, {54, 42}};

PFont font;

void setup() {
  size(int(2*54*screenMultiplier), int(60*screenMultiplier));
  background(100);
  noLoop();
  
  font = loadFont("font.vlw");
  textFont(font, 14);
  
}

void draw() {
  for (int i=0; i < points.length; i++) {
    Hit hr = new Hit(points[i][0], points[i][1], true, TABLE_WIDTH, TABLE_HEIGHT);
    PVector pr = hr.getPixelVector();
    
    fill(255, 0, 0);
    ellipse(pr.x, pr.y, 10, 10);
    
    Hit hl = new Hit(points[i][0], points[i][1], false, TABLE_WIDTH, TABLE_HEIGHT);
    PVector pl = hl.getPixelVector();
    
    fill(0, 255, 0);
    ellipse(pl.x, pl.y, 10, 10);
    
    fill(255, 255, 255);
    text(points[i][0] + ", " + points[i][1], pr.x+10, pr.y+5);
    text(points[i][0] + ", " + points[i][1], pl.x+10, pl.y+5);
  }
  
  fill(255, 255, 0);
  textFont(font, 40);
  text("LEFT", width/4-50, 45);
  text("RIGHT", 3*width/4, 45);
}
