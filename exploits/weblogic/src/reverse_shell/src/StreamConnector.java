// Decompiled by Jad v1.5.8g. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.kpdus.com/jad.html
// Decompiler options: packimports(3) 
// Source File Name:   R.java

import java.io.*;

class StreamConnector extends Thread
{

    StreamConnector(InputStream hx, OutputStream il)
    {
        this.hx = hx;
        this.il = il;
    }

    public void run()
    {
        BufferedReader ar = null;
        BufferedWriter slm = null;
        try
        {
            ar = new BufferedReader(new InputStreamReader(hx));
            slm = new BufferedWriter(new OutputStreamWriter(il));
            char buffer[] = new char[8192];
            int length;
            while((length = ar.read(buffer, 0, buffer.length)) > 0) 
            {
                slm.write(buffer, 0, length);
                slm.flush();
            }
        }
        catch(Exception exception) { }
        try
        {
            if(ar != null)
                ar.close();
            if(slm != null)
                slm.close();
        }
        catch(Exception exception1) { }
    }

    InputStream hx;
    OutputStream il;
}
