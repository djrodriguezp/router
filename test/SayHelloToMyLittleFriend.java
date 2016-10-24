import java.io.*;
import java.net.*;

class SayHelloToMyLittleFriend
{
 public static void main(String argv[]) throws Exception
 {
  //String message = "From:B\nTo:0xMiRoutersito\nMsg:como va todo parsers\nEOF";
  String message = "From:Z\nTo:Y\nMsg:como va todo parsers\nEOF";
  String response = "";
  BufferedReader inFromUser = new BufferedReader( new InputStreamReader(System.in));
  Socket clientSocket = new Socket("192.168.1.18", 1981);
  DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
  BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
  outToServer.write(message.getBytes());
  clientSocket.close();
 }
}