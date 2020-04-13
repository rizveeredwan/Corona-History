import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.attribute.FileStoreAttributeView;
import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.util.*;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;


//tutorials:https://jsoup.org/cookbook/extracting-data/selector-syntax

class Fetcher {

    List<String> articleLinks = new ArrayList<String>();
    ArrayList<ArrayList<String>>metaData=new ArrayList<ArrayList<String>>();
    String fileName;
    String topic;
    BufferedWriter bw;
    FileWriter fw;

    public Fetcher(String topicName) {
        this.topic = topicName;
        this.fileName = "new_york_times_" + this.topic + "_.csv";
        try {
            this.fw = new FileWriter(fileName, true); // to append
            this.bw = new BufferedWriter(fw);
        } catch (Exception e) {
            System.out.println("Writer Error");
        }

    }

    public ArrayList<String>linkValidityCheck(String link) {
        String parts[] = link.split("//");
        String parts2[] = parts[1].split("/");
        ArrayList<String>savenew = new ArrayList<String>();
        boolean flag=false;
        for(String p: parts2){
            savenew.add(p);
        }
        try{
            //System.out.println(savenew.get(0));
            //System.out.println(savenew.get(savenew.size()-1));
            if(savenew.get(0).contains("www.nytimes.com") && (savenew.get(savenew.size()-1).contains(".html"))) {
                flag=true;
                //System.out.println("dhuke");
            }
            else {
              return new ArrayList<String>();
            }
        }
        catch(Exception e){
            return new ArrayList<String>();
        }
        return savenew;
    }

    public String getTextData(String link) throws IOException {
        Document doc = Jsoup.connect(link).get();
        Elements texts = doc.select("p");

        StringBuilder sb = new StringBuilder();
        for (Element text : texts) {
            sb.append(text.text());
        }
        return sb.toString();
    }

    public ArrayList<String> getFormattedData(String link) throws IOException{
      ArrayList<String>extracted_data = new ArrayList<String>();
      Document doc = Jsoup.connect(link).get();

      Elements headline = doc.select("h1");
      for (Element text : headline) {
          extracted_data.add(text.text());
          break;
      }
      extracted_data.add(" ");
      Elements summary = doc.select("p#article-summary");
      for (Element text : summary) {
          extracted_data.add(text.text());
          break;
      }
      extracted_data.add(" ");
      Elements texts = doc.select("p");
      int cnt=0;
      StringBuilder sb = new StringBuilder();
      String txt="";
      for (Element text : texts) {
          cnt=cnt+1;
          if(cnt==1) continue;
          txt=
          sb.append(text.text());
      }
      extracted_data.add(sb.toString());
      Elements image = doc.select("img[src]");
      sb = new StringBuilder();
      sb.append(',');
      for (Element text : image) {
          sb.append(text.attr("abs:src")+",");
          //System.out.println(text.attr("abs:src"));
          //extracted_data.add(text.text());
          //break;
      }
      extracted_data.add(sb.toString());

      return extracted_data;
      //return sb.toString();
    }


    public void getFetchedLinks(String mainPage) throws IOException {
        Document doc = Jsoup.connect(mainPage).get();
        Elements links = doc.select("a[href]");
        articleLinks.clear();
        metaData.clear();

        ArrayList<String>savenew = new ArrayList<String>();
        for (Element link : links) {
            String val = link.attr("abs:href");
            savenew = linkValidityCheck(val);
            if(savenew.size()>0 && articleLinks.contains(val) == false){
                articleLinks.add(val);
                metaData.add(savenew);
            }
        }
        String y="";
        String month="";
        String date="",tags="",s;
        for (int i=0;i<articleLinks.size();i++) {
            s=articleLinks.get(i);
            System.out.println(s);
            savenew  = getFormattedData(s);
            /*System.out.println(savenew.size());
            System.out.println(savenew.get(0));
            System.out.println(savenew.get(1));
            System.out.println(savenew.get(2));
            System.out.println(savenew.get(3));*/
            date=metaData.get(i).get(3)+'/'+metaData.get(i).get(2)+'/'+metaData.get(i).get(1); //date-month-year
            tags="";
            for(int j=4;j<metaData.get(i).size()-1;j++){
              tags=tags+metaData.get(i).get(j);
            }

            WriteIntoFile(date,s,tags,savenew.get(0),savenew.get(1),savenew.get(2),savenew.get(3));
            //String t = this.getTextData(s);
            //bw.write(t + "\n");
        }
    }

    public void WriteIntoFile(String date, String url, String tags, String headline, String summary, String text_data, String image_source) throws IOException{
        String t = date+','+url+','+tags+','+headline+','+summary+','+text_data+','+image_source;
        bw.write(t+'\n');
        System.out.println("written "+t);
    }

    public void FileClose() throws IOException{
      bw.close();
      fw.close();
    }

}

public class NewYorkTimes {
    public static void main(String[] args) {
        String topicName = "bangladesh"; // this says the topic name of the content of which I am collecting data
        Fetcher fetcher = new Fetcher(topicName);

        int page = 0;
        String pageLink = "https://www.nytimes.com/issue/todayspaper/2020/04/02/todays-new-york-times";
        try{
          fetcher.getFetchedLinks(pageLink);
        }
        catch(Exception error){
          System.out.println(error);
        }


        /*try {
            FileReader fr = new FileReader("PageNumberSaver.txt");
            BufferedReader br = new BufferedReader(fr);
            page = Integer.parseInt(br.readLine());

            int max_page_at_one_pass = 100;
            int timeGap = 5000 * 60;
            for (int i = 1; i <= max_page_at_one_pass; i++) {
                page++;// starting from new page
                try {
                    String pageLink = "https://www.prothomalo.com/" + topicName + "/article?page="
                            + Integer.toString(page);
                    System.out.println("Current page: " + pageLink);
                    fetcher.getFetchedLinks(pageLink);
                    System.out.println("Status: " + Integer.toString(page) + " complete");
                    // debug: System.out.println("waiting started");
                    Long currentTime = System.currentTimeMillis();
                    while (true) {
                        Long newTime = System.currentTimeMillis();
                        if ((newTime - currentTime) <= timeGap) {
                            continue;
                        } else {
                            // debug: System.out.println("waiting End.");
                            break;
                        }
                    }
                } catch (Exception e) {
                    System.out.println("Error while sending");
                }
            }

            FileWriter fw = new FileWriter("PageNumberSaver.txt");
            fw.write(Integer.toString(page));
            fw.close();

        } catch (Exception e) {
            System.out.println(e);
            System.out.println("Error occurred");
        }*/
    }
}
