/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proyecto;

import java.net.URL;
import java.security.cert.Certificate;
import java.security.cert.CertificateExpiredException;
import java.security.cert.X509Certificate;
import javax.net.ssl.HttpsURLConnection;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.NodeList;

/**
 *
 * @author carlos
 */
public class Proyecto {

    
    public static void main(String[] args) {
        // TODO code application logic here
      
      try {
            traffic("http://google.com/");
        } catch (Exception e) {
            e.printStackTrace();
        }
      
    }
    public static int prefSuf (String ip) {
      int a = ip.indexOf('-');
      if (a == -1){
          System.out.print("legitimate");
          return 1;
      }
      else{
          System.out.print("phishing");
          return -1;
      } 
    }
    
    public static int urlOfAnchor (String ip) {
      int a = ip.indexOf('<');
      int b = ip.indexOf('>');
      double c = b-a-1;
       if (c/ip.length()<.31){
               System.out.print("legitimate");
        return 1;
       }
       else if(c/ip.length()>=.31 && c/ip.length()<=.67){
         System.out.print("suspicius");
         return 0;
       }
      else{
          System.out.print("phishing");
          return -1;
      } 
    }
    
    public static int SSLState (String ip) throws Exception {
        boolean valido = true;
        URL destinationURL = new URL(ip);
     
        HttpsURLConnection conn = (HttpsURLConnection) destinationURL
                .openConnection();
        conn.connect();
        Certificate[] certs = conn.getServerCertificates();
        for (Certificate cert : certs) {
          //  System.out.println("Certificate is: " + cert);
            if(cert instanceof X509Certificate) {
                try {
                    ( (X509Certificate) cert).checkValidity();
                    valido = true;
                } catch(CertificateExpiredException cee) {
                    valido = false;
                }
            }
        }
      
      int a = ip.indexOf("https");
      
      if ((a == 0 || a==1)&& valido == true){
          System.out.print("legitimate");
          return 1;
      }
      else if ((a == 0 || a==1)&& valido == false){
          System.out.print("Suspicius");
          return 0;
      } 
      else
          System.out.print("Phishing");
          return -1;
    }
    
     private static int subDomain(String ip){
       
        String replace = null;
        String replace2= null;
        String ult=null;
        int a = 0;
         for (int i = 0; i < 20; i++) {
            if (ip.contains(TLDS[i])){
                 replace = ip.replace("."+TLDS[i],"");
            }
            else
                replace = ip;
         }
         
         for (int i = 0; i < 249; i++) {
            if (ip.contains(Countries[i])){
                replace2 = replace.replace("."+Countries[i],"");
            }
            else
                replace2 = replace;
         }
         
         ult = replace2.replace("www.", "");
          
            for (int i = 0; i < ult.length(); i++) {
                if (ult.charAt(i) == '.') {
                    a++;
                }
            }
         
            if (a == 0 || a == 1){
                System.out.print("legitimate");
                return 1;
            }
            else if (a==2){
                System.out.print("Suspicius");
                return 0;
            } 
            else
                System.out.print("Phishing");
                return -1;

    }
     
      public static int traffic (String ip) {
               int result = 0;
		
		String url = "http://data.alexa.com/data?cli=10&url=" + ip;

		try {

			URLConnection conn = new URL(url).openConnection();
			InputStream is = conn.getInputStream();
			
			DocumentBuilder dBuilder = DocumentBuilderFactory.newInstance()
					.newDocumentBuilder();
			Document doc = dBuilder.parse(is);

			Element element = doc.getDocumentElement();

			NodeList nodeList = element.getElementsByTagName("POPULARITY");
			if (nodeList.getLength() > 0) {
				Element elementAttribute = (Element) nodeList.item(0);
				String ranking = elementAttribute.getAttribute("TEXT");
				if(!"".equals(ranking)){
					result = Integer.valueOf(ranking);
				}
			}

		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
              
                if (result <= 100000 && result != 0  ){
                    System.out.print("legitimate");
                    return 1;
                }
                else if (result >= 100000){
                    System.out.print("Suspicius");
                    return 0;
                } 
                else
                    System.out.print("Phishing");
                    return -1;

                
	}
         public static int domainLength(String ip) throws Exception {
             boolean valido = false;
        URL destinationURL = new URL(ip);
     
        HttpsURLConnection conn = (HttpsURLConnection) destinationURL
                .openConnection();
        conn.connect();
        Certificate[] certs = conn.getServerCertificates();
        for (Certificate cert : certs) {
           if(cert instanceof X509Certificate) {
                try {
                    ( (X509Certificate) cert).checkValidity();
                    valido = true;
                } catch(CertificateExpiredException cee) {
                    valido = false;
                }
            }
        }
           if (valido){
                System.out.print("legitimate");
                return 1;
            }
            
            else
                System.out.print("Phishing");
                return -1;
           
        }

    
     
     private static final String[] TLDS = {
        "ac",                 // academic
        "aero",               // air transport industry
        "asia",               // Pan-Asia/Asia Pacific
        "biz",                // businesses
        "cat",                // Catalan linguistic/cultural community
        "com",                // commercial enterprises
        "coop",               // cooperative associations
        "info",               // informational sites
        "jobs",               // Human Resource managers
        "mobi",               // mobile products and services
        "museum",             // museums, surprisingly enough
        "name",               // individuals' sites
        "net",                // internet support infrastructure/business
        "org",                // noncommercial organizations
        "pro",                // credentialed professionals and entities
        "tel",                // contact data for businesses and individuals
        "travel",             // entities in the travel industry
        "gov",                // United States Government
        "edu",                // accredited postsecondary US education entities
        "mil",                // United States Military
        "int"                 // organizations established by international treaty};
    
      };
     
     private static final String[] Countries = {
        "ac",                 // Ascension Island
        "ad",                 // Andorra
        "ae",                 // United Arab Emirates
        "af",                 // Afghanistan
        "ag",                 // Antigua and Barbuda
        "ai",                 // Anguilla
        "al",                 // Albania
        "am",                 // Armenia
        "an",                 // Netherlands Antilles
        "ao",                 // Angola
        "aq",                 // Antarctica
        "ar",                 // Argentina
        "as",                 // American Samoa
        "at",                 // Austria
        "au",                 // Australia (includes Ashmore and Cartier Islands and Coral Sea Islands)
        "aw",                 // Aruba
        "ax",                 // Ã…land
        "az",                 // Azerbaijan
        "ba",                 // Bosnia and Herzegovina
        "bb",                 // Barbados
        "bd",                 // Bangladesh
        "be",                 // Belgium
        "bf",                 // Burkina Faso
        "bg",                 // Bulgaria
        "bh",                 // Bahrain
        "bi",                 // Burundi
        "bj",                 // Benin
        "bm",                 // Bermuda
        "bn",                 // Brunei Darussalam
        "bo",                 // Bolivia
        "br",                 // Brazil
        "bs",                 // Bahamas
        "bt",                 // Bhutan
        "bv",                 // Bouvet Island
        "bw",                 // Botswana
        "by",                 // Belarus
        "bz",                 // Belize
        "ca",                 // Canada
        "cc",                 // Cocos (Keeling) Islands
        "cd",                 // Democratic Republic of the Congo (formerly Zaire)
        "cf",                 // Central African Republic
        "cg",                 // Republic of the Congo
        "ch",                 // Switzerland
        "ci",                 // CÃ´te d'Ivoire
        "ck",                 // Cook Islands
        "cl",                 // Chile
        "cm",                 // Cameroon
        "cn",                 // China, mainland
        "co",                 // Colombia
        "cr",                 // Costa Rica
        "cu",                 // Cuba
        "cv",                 // Cape Verde
        "cx",                 // Christmas Island
        "cy",                 // Cyprus
        "cz",                 // Czech Republic
        "de",                 // Germany
        "dj",                 // Djibouti
        "dk",                 // Denmark
        "dm",                 // Dominica
        "do",                 // Dominican Republic
        "dz",                 // Algeria
        "ec",                 // Ecuador
        "ee",                 // Estonia
        "eg",                 // Egypt
        "er",                 // Eritrea
        "es",                 // Spain
        "et",                 // Ethiopia
        "eu",                 // European Union
        "fi",                 // Finland
        "fj",                 // Fiji
        "fk",                 // Falkland Islands
        "fm",                 // Federated States of Micronesia
        "fo",                 // Faroe Islands
        "fr",                 // France
        "ga",                 // Gabon
        "gb",                 // Great Britain (United Kingdom)
        "gd",                 // Grenada
        "ge",                 // Georgia
        "gf",                 // French Guiana
        "gg",                 // Guernsey
        "gh",                 // Ghana
        "gi",                 // Gibraltar
        "gl",                 // Greenland
        "gm",                 // The Gambia
        "gn",                 // Guinea
        "gp",                 // Guadeloupe
        "gq",                 // Equatorial Guinea
        "gr",                 // Greece
        "gs",                 // South Georgia and the South Sandwich Islands
        "gt",                 // Guatemala
        "gu",                 // Guam
        "gw",                 // Guinea-Bissau
        "gy",                 // Guyana
        "hk",                 // Hong Kong
        "hm",                 // Heard Island and McDonald Islands
        "hn",                 // Honduras
        "hr",                 // Croatia (Hrvatska)
        "ht",                 // Haiti
        "hu",                 // Hungary
        "id",                 // Indonesia
        "ie",                 // Ireland (Ã‰ire)
        "il",                 // Israel
        "im",                 // Isle of Man
        "in",                 // India
        "io",                 // British Indian Ocean Territory
        "iq",                 // Iraq
        "ir",                 // Iran
        "is",                 // Iceland
        "it",                 // Italy
        "je",                 // Jersey
        "jm",                 // Jamaica
        "jo",                 // Jordan
        "jp",                 // Japan
        "ke",                 // Kenya
        "kg",                 // Kyrgyzstan
        "kh",                 // Cambodia (Khmer)
        "ki",                 // Kiribati
        "km",                 // Comoros
        "kn",                 // Saint Kitts and Nevis
        "kp",                 // North Korea
        "kr",                 // South Korea
        "kw",                 // Kuwait
        "ky",                 // Cayman Islands
        "kz",                 // Kazakhstan
        "la",                 // Laos (currently being marketed as the official domain for Los Angeles)
        "lb",                 // Lebanon
        "lc",                 // Saint Lucia
        "li",                 // Liechtenstein
        "lk",                 // Sri Lanka
        "lr",                 // Liberia
        "ls",                 // Lesotho
        "lt",                 // Lithuania
        "lu",                 // Luxembourg
        "lv",                 // Latvia
        "ly",                 // Libya
        "ma",                 // Morocco
        "mc",                 // Monaco
        "md",                 // Moldova
        "me",                 // Montenegro
        "mg",                 // Madagascar
        "mh",                 // Marshall Islands
        "mk",                 // Republic of Macedonia
        "ml",                 // Mali
        "mm",                 // Myanmar
        "mn",                 // Mongolia
        "mo",                 // Macau
        "mp",                 // Northern Mariana Islands
        "mq",                 // Martinique
        "mr",                 // Mauritania
        "ms",                 // Montserrat
        "mt",                 // Malta
        "mu",                 // Mauritius
        "mv",                 // Maldives
        "mw",                 // Malawi
        "mx",                 // Mexico
        "my",                 // Malaysia
        "mz",                 // Mozambique
        "na",                 // Namibia
        "nc",                 // New Caledonia
        "ne",                 // Niger
        "nf",                 // Norfolk Island
        "ng",                 // Nigeria
        "ni",                 // Nicaragua
        "nl",                 // Netherlands
        "no",                 // Norway
        "np",                 // Nepal
        "nr",                 // Nauru
        "nu",                 // Niue
        "nz",                 // New Zealand
        "om",                 // Oman
        "pa",                 // Panama
        "pe",                 // Peru
        "pf",                 // French Polynesia With Clipperton Island
        "pg",                 // Papua New Guinea
        "ph",                 // Philippines
        "pk",                 // Pakistan
        "pl",                 // Poland
        "pm",                 // Saint-Pierre and Miquelon
        "pn",                 // Pitcairn Islands
        "pr",                 // Puerto Rico
        "ps",                 // Palestinian territories (PA-controlled West Bank and Gaza Strip)
        "pt",                 // Portugal
        "pw",                 // Palau
        "py",                 // Paraguay
        "qa",                 // Qatar
        "re",                 // RÃ©union
        "ro",                 // Romania
        "rs",                 // Serbia
        "ru",                 // Russia
        "rw",                 // Rwanda
        "sa",                 // Saudi Arabia
        "sb",                 // Solomon Islands
        "sc",                 // Seychelles
        "sd",                 // Sudan
        "se",                 // Sweden
        "sg",                 // Singapore
        "sh",                 // Saint Helena
        "si",                 // Slovenia
        "sj",                 // Svalbard and Jan Mayen Islands Not in use (Norwegian dependencies; see .no)
        "sk",                 // Slovakia
        "sl",                 // Sierra Leone
        "sm",                 // San Marino
        "sn",                 // Senegal
        "so",                 // Somalia
        "sr",                 // Suriname
        "st",                 // SÃ£o TomÃ© and PrÃ­ncipe
        "su",                 // Soviet Union (deprecated)
        "sv",                 // El Salvador
        "sy",                 // Syria
        "sz",                 // Swaziland
        "tc",                 // Turks and Caicos Islands
        "td",                 // Chad
        "tf",                 // French Southern and Antarctic Lands
        "tg",                 // Togo
        "th",                 // Thailand
        "tj",                 // Tajikistan
        "tk",                 // Tokelau
        "tl",                 // East Timor (deprecated old code)
        "tm",                 // Turkmenistan
        "tn",                 // Tunisia
        "to",                 // Tonga
        "tp",                 // East Timor
        "tr",                 // Turkey
        "tt",                 // Trinidad and Tobago
        "tv",                 // Tuvalu
        "tw",                 // Taiwan, Republic of China
        "tz",                 // Tanzania
        "ua",                 // Ukraine
        "ug",                 // Uganda
        "uk",                 // United Kingdom
        "um",                 // United States Minor Outlying Islands
        "us",                 // United States of America
        "uy",                 // Uruguay
        "uz",                 // Uzbekistan
        "va",                 // Vatican City State
        "vc",                 // Saint Vincent and the Grenadines
        "ve",                 // Venezuela
        "vg",                 // British Virgin Islands
        "vi",                 // U.S. Virgin Islands
        "vn",                 // Vietnam
        "vu",                 // Vanuatu
        "wf",                 // Wallis and Futuna
        "ws",                 // Samoa (formerly Western Samoa)
        "ye",                 // Yemen
        "yt",                 // Mayotte
        "yu",                 // Serbia and Montenegro (originally Yugoslavia)
        "za",                 // South Africa
        "zm",                 // Zambia
        "zw",                 // Zimbabwe
    };
}



       
          
      
          
          
    
     
    
    

    

