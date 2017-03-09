
public class Main
{
  public static void main(String[] args){
	  if(args.length!=1){
		  System.out.println("Usage:java Main [Host:Port]");
		  return;
	  }
	  R r = new R(args[0]);
  }
}