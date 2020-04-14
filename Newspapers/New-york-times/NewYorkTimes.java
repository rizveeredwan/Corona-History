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
      StringBuilder sb = new StringBuilder();
      Document doc = Jsoup.connect(link).get();

      //headline
      Elements headline = doc.select("h1");
      String val="";
      sb = new StringBuilder();
      sb.append(" ");
      for (Element text : headline) {
          val = text.text();
          val = val.replace(","," ");
          sb.append(val);
          break;
      }
      extracted_data.add(sb.toString());

      //summary
      Elements summary = doc.select("p#article-summary");
      val = "";
      sb = new StringBuilder();
      sb.append(" ");
      for (Element text : summary) {
        val = text.text();
        val = val.replace(","," ");
        sb.append(val);
      }
      extracted_data.add(sb.toString());

      //normal text
      Elements texts = doc.select("p");
      int cnt=0;
      sb = new StringBuilder();
      sb.append(" ");
      for (Element text : texts) {
          cnt=cnt+1;
          if(cnt==1) continue;
          val = text.text();
          val = val.replace(","," ");
          sb.append(val+" ");
      }
      extracted_data.add(sb.toString());
      //System.out.println(extracted_data.get(extracted_data.size()-1).length());

      Elements image = doc.select("img[src]");
      sb = new StringBuilder();
      sb.append(" ");
      for (Element text : image) {
          sb.append(text.attr("abs:src")+" ");
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
            //System.out.println(savenew.get(2).length());
            /*System.out.println(savenew.size());
            System.out.println(savenew.get(0));
            System.out.println(savenew.get(1));
            System.out.println(savenew.get(2));
            System.out.println(savenew.get(3));*/
            date=metaData.get(i).get(3)+'/'+metaData.get(i).get(2)+'/'+metaData.get(i).get(1); //date-month-year
            tags="";
            for(int j=4;j<metaData.get(i).size()-1;j++){
              tags=tags+" "+metaData.get(i).get(j);
            }

            WriteIntoFile(date,s,tags,savenew.get(0),savenew.get(1),savenew.get(2),savenew.get(3));
            //String t = this.getTextData(s);
            //bw.write(t + "\n");
        }
    }

    public void WriteIntoFile(String date, String url, String tags, String headline, String summary, String text_data, String image_source) throws IOException{
        String t = date+','+url+','+tags+','+headline+','+summary+','+text_data+','+image_source;
        bw.write(t+'\n');
        //System.out.println("written "+t);
    }

    public void FileClose() throws IOException{
      bw.close();
      fw.close();
    }

}

class CustomComparator implements Comparator<String> {
    //@Override
    public int compare(String o1, String o2) {
        String arr[] = o1.split("/"); //date/month/year
        Calendar c1 = new GregorianCalendar(Integer.parseInt(arr[2]),Integer.parseInt(arr[1]),Integer.parseInt(arr[0]));
        Date d1 = c1.getTime();

        String arr2[] = o2.split("/");
        Calendar c2 = new GregorianCalendar(Integer.parseInt(arr2[2]),Integer.parseInt(arr2[1]),Integer.parseInt(arr2[0]));
        Date d2 = c2.getTime();
        return d1.compareTo(d2);
    }
}


public class NewYorkTimes {

    String topicName = "news_data"; // this says the topic name of the content of which I am collecting data
    Fetcher fetcher = new Fetcher(topicName);

    public static Date MakeDateFromString(String date){
        String arr[] = date.split("/"); //   day/month/year
        int year = Integer.parseInt(arr[2]);
        int month = Integer.parseInt(arr[1]);
        int day = Integer.parseInt(arr[0]);
        Date d =  new GregorianCalendar(year, month, day).getTime();
        return d;
    }

    public static ArrayList<String> SplitDate(String date){
      String arr[] = date.split("/"); //   day/month/year
      ArrayList<String>temp = new ArrayList<String>();
      temp.add(arr[0]);
      temp.add(arr[1]);
      temp.add(arr[2]);
      return temp;
    }

    public static ArrayList<String> ReturnNextDay(String day, String month, String year){
      System.out.println(day+" , "+month+" , "+year);
      System.out.println(Integer.parseInt(year));
      Date dt = new GregorianCalendar(Integer.parseInt(year), Integer.parseInt(month), Integer.parseInt(day)).getTime();
      System.out.println(dt);
      Calendar cal = Calendar.getInstance();
      cal.setTime(dt);
      cal.add(Calendar.DATE, 1);
      dt = cal.getTime();
      cal.setTime(dt);
      System.out.println(dt);
      ArrayList<String>temp = new ArrayList<String>();
      temp.add(Integer.toString(cal.get(Calendar.DAY_OF_MONTH)));
      temp.add(Integer.toString(cal.get(Calendar.MONTH)));
      temp.add(Integer.toString(cal.get(Calendar.YEAR)));
      return temp;
    }

    public static ArrayList<String> ReturnPreviousDays(String day, String month, String year,int offset){
      //System.out.println(day+" , "+month+" , "+year);
      //System.out.println(Integer.parseInt(year));
      Date dt = new GregorianCalendar(Integer.parseInt(year), Integer.parseInt(month), Integer.parseInt(day)).getTime();
      //System.out.println(dt);
      Calendar cal = Calendar.getInstance();
      cal.setTime(dt);
      cal.add(Calendar.DATE, -offset);
      dt = cal.getTime();
      cal.setTime(dt);
      //System.out.println(dt);
      ArrayList<String>temp = new ArrayList<String>();
      temp.add(Integer.toString(cal.get(Calendar.DAY_OF_MONTH)));
      temp.add(Integer.toString(cal.get(Calendar.MONTH)));
      temp.add(Integer.toString(cal.get(Calendar.YEAR)));
      return temp;
    }

    public static boolean DataFetchInitiate(String day, String month, String year, NewYorkTimes newspaer){
        day = Padding(day,2);
        month = Padding(Integer.toString((Integer.parseInt(month)+1)),2);
        String page_link = "https://www.nytimes.com/issue/todayspaper/"+year+"/"+ month +"/"+day+"/todays-new-york-times";
        try{
          newspaer.fetcher.getFetchedLinks(page_link);
          return true;
        }
        catch(Exception error){
          System.out.println(error);
          return false;
        }
    }

    public static void WriteIntoFile(ArrayList<String>dates) throws IOException{
      FileWriter fw = new FileWriter("processed_dates.txt");
      BufferedWriter bw = new BufferedWriter(fw);
      for(int i=0;i<dates.size();i++){
        bw.write(dates.get(i)+"\n");
      }
      bw.close();
      fw.close();
    }

    public static String Padding(String str,int size){
        while(str.length()<size){
          str="0"+str;
        }
        return str;
    }

    public static void main(String[] args) throws IOException {

        NewYorkTimes newspaper = new NewYorkTimes();

        ArrayList<String> dates = new ArrayList<String>();

        Date current_date = new Date();
        System.out.println(current_date);
        Calendar cal = Calendar.getInstance();
        cal.setTime(current_date); // don't forget this if date is arbitrary e.g. 01-01-2014, Read more: https://www.java67.com/2016/12/how-to-get-current-day-month-year-from-date-in-java8.html#ixzz6JYhH6VmN
        String day = Integer.toString(cal.get(Calendar.DAY_OF_MONTH)); // 17
        String month = Integer.toString(cal.get(Calendar.MONTH)); // 5
        String year =  Integer.toString(cal.get(Calendar.YEAR)); // 2016
        String current_date_string = day + '/' + month + '/' + year;
        //Read more: https://www.java67.com/2016/12/how-to-get-current-day-month-year-from-date-in-java8.html#ixzz6JYhOo52p

        String line = "";


        try{
          FileReader fr = new FileReader("processed_dates.txt");
          BufferedReader br = new BufferedReader(fr);
          while((line = br.readLine()) != null){
              dates.add(line);
          }
          br.close();
          fr.close();
          Collections.sort(dates, new CustomComparator());
          for(int i=0;i<dates.size();i++){
            System.out.println(dates.get(i));
          }
        }
        catch(Exception e){
            System.out.println(e);
        }

        ArrayList<String>temp;
        if(dates.size()>0){
            while(true){
                Date d1 = MakeDateFromString(dates.get(dates.size()-1));
                Date d2 = MakeDateFromString(current_date_string);
                System.out.println(d1.compareTo(d2));
                if(d1.compareTo(d2)<0) {
                    //we need to update some more dates: date gap exists
                    temp = SplitDate(dates.get(dates.size()-1));
                    temp = ReturnNextDay(temp.get(0), temp.get(1), temp.get(2));
                    System.out.println(temp);
                    boolean var =  DataFetchInitiate(temp.get(0),temp.get(1),temp.get(2),newspaper); // day/month/year
                    dates.add(temp.get(0)+"/"+temp.get(1)+"/"+temp.get(2));
                }
                else if(d1.compareTo(d2)>=0) break;
            }
            //dates.add(day+'/'+month+'/'+year);
        }
        else{
            System.out.println(day+" "+month+" "+year);
            boolean var =  DataFetchInitiate(day,month,year,newspaper); // day/month/year
            dates.add(day+"/"+month+"/"+year);
        }
        //backwards
        int number_of_backward_days=10;
        for(int i=1;i<=number_of_backward_days;i++){
            temp = SplitDate(dates.get(0));
            temp = ReturnPreviousDays(temp.get(0), temp.get(1), temp.get(2),i);
            System.out.println(temp);
            boolean var =  DataFetchInitiate(temp.get(0),temp.get(1),temp.get(2),newspaper); // day/month/year
            dates.add(temp.get(0)+"/"+temp.get(1)+"/"+temp.get(2));
        }
        Collections.sort(dates, new CustomComparator());
        WriteIntoFile(dates);
    }
}
