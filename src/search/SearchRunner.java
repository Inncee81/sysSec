package search;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;


import org.apache.commons.codec.binary.Base64;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.json.simple.parser.JSONParser;

public class SearchRunner {

	static String BING_API_KEY = "xaGM3hcKEWMx00/z9tB71zIDIuvtr/hkYEMP5oNr6G0="; 
	public static String search(String query) throws Exception {
	    String bingUrl = "https://api.datamarket.azure.com/Bing/Search/Web?Query=%27" + java.net.URLEncoder.encode(query) + "%27&$format=JSON";

	    String accountKey = BING_API_KEY;
	    byte[] accountKeyBytes = Base64.encodeBase64((accountKey + ":" + accountKey).getBytes()); // code for encoding found on stackoverflow
	    String accountKeyEnc = new String(accountKeyBytes);

	    URL url = new URL(bingUrl);
	    URLConnection urlConnection = url.openConnection();
	    String s1 = "Basic " + accountKeyEnc;
	    urlConnection.setRequestProperty("Authorization", s1);
	    BufferedReader in = new BufferedReader(new InputStreamReader(
	        urlConnection.getInputStream()));
	    String inputLine;
	    StringBuffer sb = new StringBuffer();
	    while ((inputLine = in.readLine()) != null){
	      //System.out.println(inputLine);
	      sb.append(inputLine);
	    }
	    in.close();
	    return sb.toString();
	  }
	/**
	 * @param args
	 * @throws Exception 
	 */
	public static void main(String[] args) throws Exception {
		// TODO Auto-generated method stub
		String searchResult =SearchRunner.search("Mike Ehrenberg");
		JSONParser parser = new JSONParser();
		JSONObject json = (JSONObject)parser.parse(searchResult);
		String top = json.get("d").toString();
		json = (JSONObject)parser.parse(top);
		//String result = json.get("results").toString();
		//Object obj= parser.parse(top);
		JSONArray array=(JSONArray)json.get("results");
		for(int i = 0 ; i < array.size() ; i ++){
			JSONObject obj2=(JSONObject)array.get(i);
			json = (JSONObject)parser.parse(obj2.toString());
			String Url = top = json.get("Url").toString();
			System.out.println(Url);
		}
		
	}

}
