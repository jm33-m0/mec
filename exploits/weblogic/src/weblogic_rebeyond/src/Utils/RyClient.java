package Utils;

import java.util.Hashtable;
import javax.naming.InitialContext;
import javax.naming.NamingException;

public class RyClient
{
  public static final String JNDI_FACTORY = "weblogic.jndi.WLInitialContextFactory";
  int port;
  String host;
  
  public static InitialContext getInitialContext(String url)
    throws NamingException
  {
    Hashtable<String, String> env = new Hashtable();
    env.put("java.naming.factory.initial", "weblogic.jndi.WLInitialContextFactory");
    env.put("java.naming.provider.url", url);
    return new InitialContext(env);
  }
}
