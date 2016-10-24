import java.io.*;
import java.net.*;

class SayHelloToMyLittleFriend
{
 public static void main(String args[]) throws Exception
 {
  String message = "From:"+args[0]+"\n"+args[1]+":Y\nMsg:"+args[2]+"\nEOF";
  System.out.println(message);
  String response = "";
  BufferedReader inFromUser = new BufferedReader( new InputStreamReader(System.in));
  Socket clientSocket = new Socket("192.168.1.18", 1981);
  DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
  BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
  outToServer.write(message.getBytes());
  clientSocket.close();
 }
}