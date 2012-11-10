package search;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.ArrayList;

public class Main {

	String insecureWebsiteList = "/home/avijit/lists/insecure1";
	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		String query = "free";
		ArrayList <String> results = new ArrayList<String>();
		results = SearchRunner.getUrlsFromKeyword(query);
		Main o = new Main();
		//System.out.print(results.get(0));
		//KeywordExtractor.getKeywords(results.get(0));
		o.checkInsecureWebsiteList(results.get(0));
	}
	
	public void checkInsecureWebsiteList(String url) throws Exception{
		FileInputStream fstream = new FileInputStream(insecureWebsiteList);
		DataInputStream in = new DataInputStream(fstream);
		String insecureUrl; 
		while((insecureUrl = in.readLine())!=null){
			double similarityPercent = FindSimilarity.GetSimilarityPercentage(url, insecureUrl);
			System.out.println("% Similarity with " + insecureUrl +": " +  similarityPercent + "%");
		}
	}

}
