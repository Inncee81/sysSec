package search;
import java.util.ArrayList;
import java.util.HashSet;

public class FindSimilarity {
	public static int GetNumberofSimilarKeywords(ArrayList<String> toCompare, ArrayList<String> compareAgainst) throws Exception{
		int NumberSimilarKeywords = 0;
		HashSet<String> keywordHash = new HashSet<String>();
		for(int i = 0 ; i < compareAgainst.size(); i ++){
			keywordHash.add(compareAgainst.get(i).trim());
		}
		
		for(int i = 0 ; i < toCompare.size(); i ++){
			if(keywordHash.contains(toCompare.get(0).trim())){
				NumberSimilarKeywords ++;
			}
		}
		return NumberSimilarKeywords;
	}
	
	public static double GetSimilarityPercentage(String toCompareUrl, String compareAgainstUrl) throws Exception{
		ArrayList<String> toCompare = KeywordExtractor.getKeywords(toCompareUrl);
		ArrayList<String> compareAgainst = KeywordExtractor.getKeywords(compareAgainstUrl);
		/*
		System.out.println("To compare keywords");
		for(int i = 0 ; i < toCompare.size(); i ++){
			System.out.println(toCompare.get(i));
		}
		System.out.println("compare against keywords");

		for(int i = 0 ; i < compareAgainst.size(); i ++){
			System.out.println(compareAgainst.get(i));
		}*/
		
		int numSimilarKeywords = GetNumberofSimilarKeywords(toCompare,compareAgainst);
		double similarityPercent = (numSimilarKeywords*100.0)/toCompare.size();
		return similarityPercent;
	}
}
