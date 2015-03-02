class Hit {
  float x;
  float y;
  boolean isRightSide;
  int tableWidth;
  int tableHeight;
  
  Hit(float x, float y, boolean isRightSide, int tableWidth, int tableHeight) {
    this.x = x;
    this.y = y;
    this.isRightSide = isRightSide;
    this.tableWidth = tableWidth;
    this.tableHeight = tableHeight;
  }
  
  PVector getPixelVector() {
    float x_percent = x / tableWidth;
    float y_percent = y / tableHeight;
    
    float side_x = (float)width / 2;
    float pixel_x = Math.max(0, Math.min(side_x, y_percent * side_x));
    if (isRightSide) {
      pixel_x = side_x - pixel_x;
      pixel_x += side_x;
    }
    float pixel_y = Math.max(0, Math.min(height, x_percent * height));
    if (isRightSide) {
      pixel_y = height - pixel_y;
    }
    
    return new PVector(pixel_x, pixel_y);
  }  
}
