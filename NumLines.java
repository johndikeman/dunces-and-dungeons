//Cameron Egger
//1-4-2016


import static java.lang.System.*;
import java.util.*;
import java.io.*;

public class NumLines 
{
	static Scanner file;
    public static void main(String[]args)throws Exception    	
    {
    	String name="H:\\GitHub\\dunces-and-dungeons";
    	File folder = new File(name);
    	out.println(rawr(folder,name));
    	
    }
    
    
    public static int rawr(File folder,String directory)throws Exception
    {
    	int count =0;
    	for (final File fileEntry : folder.listFiles()) 
    	{
    		if(fileEntry.getName().contains(".py")||fileEntry.getName().contains(".html")||fileEntry.getName().contains(".coffee")||fileEntry.getName().contains(".css")||fileEntry.getName().contains(".js")||fileEntry.isDirectory())
    		{
    			if (fileEntry.isDirectory()) 
    	    	{
    	    		count+=rawr(fileEntry,directory+"\\"+fileEntry.getName());
     	   		}
     	   		
     	   		else if(!fileEntry.getName().contains("__init__")&&!fileEntry.getName().contains(".pyc"))
     	   		{
      	    	  	file=new Scanner(new File(directory+"\\"+fileEntry.getName()));
      	    	  	while(file.hasNextLine())
      	    	  	{
      	    	  		count++;
      	    	  		file.nextLine();
      	    	  	}
      	    	  out.println(fileEntry.getName());
       	 		}
    		}
    	    
   		}
   		return count;
    }
}


