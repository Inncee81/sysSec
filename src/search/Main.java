package search;

import java.util.ArrayList;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) throws Exception{
		// TODO Auto-generated method stub
		String query = "Mike Ehrenberg";
		ArrayList <String> results = new ArrayList<String>();
		results = SearchRunner.getUrlsFromKeyword(query);
		for(int i = 0 ; i < results.size(); i++){
			System.out.println(results.get(i));
		}
	}

}
