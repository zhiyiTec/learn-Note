package aaaa;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;

/**
 * 遍历数据，去掉所有的双引号
 */
public class Test {

	public static void main(String[] args) throws Exception{
		String inputPath="C:\\Users\\admin\\Desktop\\20190601\\20190601.csv";
		File file1=new File(inputPath);
		String outputPath="C:\\Users\\admin\\Desktop\\20190601\\20190601-2.csv";
	
		BufferedReader br=new BufferedReader(new FileReader(inputPath));
		BufferedWriter bw=new BufferedWriter(new FileWriter(outputPath));
		String line=br.readLine();
		while(line!=null){
			char[] arr1=line.toCharArray();
			char[] arr2=new char[arr1.length];
			int count=0;
			for(char c:arr1){
				if(c!='\"'){
					arr2[count++]=c;
				}
			}
			String str=new String(arr2,0,count);
			bw.write(str);
			line=br.readLine();
			if(line!=null){
				bw.newLine();
			}
		}
		br.close();
		bw.flush();
		bw.close();
	}

}
