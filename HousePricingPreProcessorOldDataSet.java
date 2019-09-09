import java.io.BufferedReader;
import java.io.*;
import java.util.List;
import java.util.ArrayList;

public class HousePricingPreProcessorOldDataSet {

    public static void main(String[] args) throws Exception {
        String csvFile = "C:\\Users\\user\\Downloads\\listings\\listings_2018-02-01.csv";
        String processedCsvFile = "C:\\Users\\user\\Downloads\\listings\\output_2018-02-01.csv";
        BufferedReader br = null;
        FileWriter writer = null;
        String line = "", tokenStr = "", prevTokenStr = "", completeLine = "", finalRecord = "";
        String cvsSplitBy = ",";
        boolean lineBreak = false, isJson = false;
        List<String> rowList = new ArrayList<String>();

        try {
            writer = new FileWriter(processedCsvFile);
            br = new BufferedReader(new FileReader(csvFile));
            RegExText re = new RegExText();
            int count = 0;
            boolean isRecStartWithId = false;
            while ((line = br.readLine()) != null) {
                completeLine = line;
                //System.out.println("count : " + count + " , line.length():" + line.length());
                count = count + line.length();
                br.mark(count);

                while(!re.isRecordStartsWithId(line = br.readLine())) {
                    completeLine = completeLine + line;
                    //System.out.println("completeLine: " + completeLine);
                    br.mark(count);
                }

                line = completeLine;
                br.reset();

                line = re.replaceCommasFromNumbers(line);

                // use comma as separator
                String[] tokens = line.split(cvsSplitBy);

                if(tokens.length > 0) {
                    tokenStr = "";
                    prevTokenStr = "";
                    lineBreak = false;
                    isJson = false;
                    rowList = new ArrayList<>();
                    for(String token: tokens) {
                        if(token.length() > 0 || token.trim().equals("")) {

                            if(token.contains("{")) {
                                isJson = true;
                                tokenStr = "";
                            }

                            if(token.startsWith(" ") || token.startsWith("\t") || token.startsWith("\\s+")) {
                                lineBreak = true;
                                //System.out.println("token: " + token);
                            }
                            else
                                lineBreak = false;

                            if (lineBreak || isJson) {
                                tokenStr = tokenStr + (isJson ? " " : " ") + token;
                                prevTokenStr = tokenStr;
                            }  else {
                                //tokenStr = "";
                                tokenStr = token;
                            }

                            if(token.contains("}")) {
                                isJson = false;
                                prevTokenStr = "";
                            }
                        }

                        if(!lineBreak && !isJson ) {
                            if(!prevTokenStr.equals("") && !lineBreak ) {
                                rowList.remove(rowList.size() - 1);
                                rowList.add(prevTokenStr);
                                prevTokenStr = "";
                            }
                            rowList.add(tokenStr);
                            //System.out.println("tokenStr : " + tokenStr);
                        }

                    }
                    if(rowList.size() == 96) {
                        //System.out.println("rowList:" + rowList.size() + " =>" + rowList);
                        finalRecord = "\"" + String.join("\",\"", rowList) + "\"";
                        System.out.println(finalRecord);
                        writer.append(finalRecord+"\n");
                    }
                }
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            if(writer != null) {
                try {
                    writer.flush();
                    writer.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}