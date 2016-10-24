import java.io.*;
import java.net.*;

class SayHelloToMyLittleFriend
{
 public static void main(String args[]) throws Exception
 {
    if(args.length == 4)
    {
        String message = "From:"+args[1]+"\nTo:"+args[2]+"\nMsg:"+args[2]+"\nEOF";
        String response = "";
        BufferedReader inFromUser = new BufferedReader( new InputStreamReader(System.in));
        Socket clientSocket = new Socket(args[0], 1981);
        DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
        BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        outToServer.write(message.getBytes());
        clientSocket.close();
    }
    else
    {
        System.out.println("Uso: java SayHelloToMyLittleFriend <ip> <from> <to> <mensaje>");
    }
 }
}