package search;
import com.alchemyapi.api.AlchemyAPI;
import org.xml.sax.SAXException;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.util.ArrayList;


public class KeywordExtractor {
	static String ALCHEMY_KEY = "";
	public static ArrayList<String> getKeywords(String url) throws Exception{
		AlchemyAPI alchemyObj = AlchemyAPI.GetInstanceFromString(ALCHEMY_KEY);
		ArrayList<String> Keywords = new ArrayList<String>();
		// Extract topic keywords for a web URL.
        Document doc = alchemyObj.URLGetRankedKeywords(url);
        doc.getDocumentElement().normalize();
		//System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
        NodeList nList = doc.getElementsByTagName("keyword");
        //System.out.println("Length "  + nList.getLength());
        for (int temp = 0; temp < nList.getLength(); temp++) {
        	 Node nNode = nList.item(temp);
        	 if (nNode.getNodeType() == Node.ELEMENT_NODE) {
        		 Element eElement = (Element) nNode;
        		 Keywords.add(getTagValue("text", eElement));
        	 }
        		 
        }
       /* for(int i = 0 ; i < Keywords.size(); i ++){
			System.out.println(Keywords.get(i));
		}*/
        return Keywords;
	}

private static String getTagValue(String sTag, Element eElement) {
	NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();
 
        Node nValue = (Node) nlList.item(0);
 
	return nValue.getNodeValue();
  }
}

