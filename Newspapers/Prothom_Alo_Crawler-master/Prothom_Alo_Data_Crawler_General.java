import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.attribute.FileStoreAttributeView;
import java.util.List;
import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

class Fetcher {

    List<String> articleLinks = new ArrayList<String>();
    String fileName;
    String topic;
    BufferedWriter bw;
    FileWriter fw;

    public Fetcher(String topicName) {
        this.topic = topicName;
        this.fileName = "prothom_alo_" + this.topic + ".txt";
        try {
            this.fw = new FileWriter(fileName, true); // to append
            this.bw = new BufferedWriter(fw);
        } catch (Exception e) {
            System.out.println("Writer Error");
        }

    }

    public boolean linkValidityCheck(String link) {
        String[] parts = link.split("/");
        int cnt = 0;
        for (String p : parts) {
            if (p.compareTo("article") == 0) {
                cnt++;
            }
            if (p.compareTo(this.topic) == 0) {
                cnt++;
            }
        }
        if (cnt == 0)
            return false;
        if (cnt == 2)
            return true;
        return false;
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

    public void getFetchedLinks(String mainPage) throws IOException {
        Document doc = Jsoup.connect(mainPage).get();
        Elements links = doc.select("a[href]");
        articleLinks.clear();

        for (Element link : links) {
            String val = link.attr("abs:href");
            boolean ok = this.linkValidityCheck(val);
            if (ok == true) {
                articleLinks.add(val);
            }
        }
        for (String s : articleLinks) {
            String t = this.getTextData(s);
            bw.write(t + "\n");
        }
    }

}

public class Prothom_Alo_Data_Crawler_General {
    public static void main(String[] args) {
        String topicName = "bangladesh"; // this says the topic name of the content of which I am collecting data
        Fetcher fetcher = new Fetcher(topicName);

        int page = 0;

        try {
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
        }
    }
}
