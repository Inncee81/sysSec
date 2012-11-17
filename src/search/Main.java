package search;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {
    public static Logger logger;
	String insecureWebsiteList = "/home/avijit/workspace/newSysSec/sysSec/py/in_url_links";
	String insecureKeywords = "/home/avijit/lists/insecureKeyWords";
	String commonInsecureKeywords = "/home/avijit/lists/common";
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		//String query = "free";
		//ArrayList <String> results = new ArrayList<String>();
		//results = SearchRunner.getUrlsFromKeyword(query);
		Main o = new Main();
		o.checkInsecureWebsiteList();
	}
	
	public void checkInsecureWebsiteList() {
	  logger = Logger.getLogger("");
	  HashSet<String> insecureKeySet = new HashSet<String>();
	  HashSet<String> commonInsecureKeySet = new HashSet<String>();
      FileInputStream fstream = null;
      FileWriter fout;
      String insecureUrl = ""; 
      int count = 0;
      try {
        FileHandler handler = new FileHandler("err-log.txt");
        logger.addHandler(handler);
        logger.setLevel(Level.ALL);
        fstream = new FileInputStream(insecureWebsiteList);
        fout = new FileWriter(insecureKeywords);
        BufferedWriter out = new BufferedWriter(fout);
        DataInputStream in = new DataInputStream(fstream);
		while((insecureUrl = in.readLine())!=null){
          System.out.println(insecureUrl);
      	  ArrayList<String> keywords = null;
          keywords = KeywordExtractor.getKeywords(insecureUrl, logger);
          for(int i = 0 ; i < keywords.size(); i ++){
            //System.out.println(keywords.get(i));
            if(insecureKeySet.contains(keywords.get(i))){
              commonInsecureKeySet.add(keywords.get(i));
            }
            else{
              count++;
              insecureKeySet.add(keywords.get(i));
            }
        } 
		}
		Iterator<String> keyIterator = insecureKeySet.iterator();
        while(keyIterator.hasNext()){
          String str = keyIterator.next();
          //System.out.println(str);
          out.write(str+"\n");
          out.flush();
        }
        out.close();
        
        fout = new FileWriter(commonInsecureKeywords);
        out = new BufferedWriter(fout);
        
        keyIterator = commonInsecureKeySet.iterator();
        while(keyIterator.hasNext()){
          String str = keyIterator.next();
          //System.out.println(str);
          out.write(str+"\n");
          out.flush();
        }
        out.close();
        
        System.out.println(count + " Keywords");
    } catch (Exception e) {
      // TODO Auto-generated catch block
      logger.info(insecureUrl + " " + e.getMessage());
    }
	}

}
