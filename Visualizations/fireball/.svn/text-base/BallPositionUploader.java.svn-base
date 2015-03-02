import java.net.*;
import java.io.*;
import java.text.DecimalFormat;

public class BallPositionUploader {
  
  public static boolean MULTITHREAD = true;  // turning this to false will cause the game to wait while it calls the server
  
  public static String UPLOAD_HOST = "pppp.media.mit.edu";
  public static int UPLOAD_PORT = 80;
  public static String UPLOAD_URL = "/hit";
  
  private String table;
  
  public BallPositionUploader(String tableName) {
    this.table = tableName;
  }
  
  public void uploadHit(float x, float y, boolean isRightSide) {
    long time = System.currentTimeMillis();
    
    // If we're multithreading, create the Thread. Otherwise, just call the method directly.
    if (MULTITHREAD) {
      Thread thread = new Thread(new UploaderThread(x, y, isRightSide, time));
      thread.start();
    }
    else {
      callPongServer(x, y, isRightSide, time);
    }
  }
  
  /**
   * Issues the URL connection to the server to upload the hit.
   */
  private void callPongServer(float x, float y, boolean isRightSide, long time) {    
    StringBuffer url = new StringBuffer(UPLOAD_URL);
    url.append("/" + table);
    
    if (isRightSide) {
      url.append("/right");
    } else {
      url.append("/left");
    }
    
    DecimalFormat format = new DecimalFormat("#########.####");
    url.append("/x/" + format.format(x));
    url.append("/y/" + format.format(y));
    
    url.append("/time/" + time);
    
    try {
      URI encoded = new URI("http", null, UPLOAD_HOST, UPLOAD_PORT , url.toString(), null, null);
      System.out.println(encoded);
      URL pong = encoded.toURL();
      
      URLConnection pongConnection = pong.openConnection();
      BufferedReader in = new BufferedReader(new InputStreamReader(pongConnection.getInputStream()));
      String inputLine;
  
      while ((inputLine = in.readLine()) != null) {
        //System.out.println(inputLine);
      }
      in.close();
    } catch (Exception e) {
      System.err.println(e);
    }    
  }
  
  /**
   * A runnable that can call the server in an out-of-band process to notify it of a hit.
   */
  private class UploaderThread implements Runnable {
    private float x;
    private float y;
    private boolean rightSide;
    private long time;
    
    public UploaderThread(float x, float y, boolean rightSide, long time) {
      this.x = x;
      this.y = y;
      this.time = time;
      this.rightSide = rightSide;
    }
    
    // This method is called when the thread runs
    public void run() {
      BallPositionUploader.this.callPongServer(x, y, rightSide, time);
    }
  }
}
