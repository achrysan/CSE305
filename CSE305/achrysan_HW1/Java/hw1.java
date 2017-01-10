//package hw1;

import java.io.*;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

public class hw1 {
		
		public static Set<Character> cleanup(String s){
			s = s.toLowerCase();
	System.out.println("s is currently: "+s);
			char[] chars = s.toCharArray();
		    Arrays.sort(chars);
		    String sorted = new String(chars);
		    Set<Character> set = new HashSet<Character>();
		    for(int i = 0; i < sorted.length(); i++){
		    	set.add(sorted.charAt(i));
		    }
		    Iterator<Character> iterator = set.iterator();
		    while (iterator.hasNext()) {
		        Character element = iterator.next();
		        if (element == ' ' || element == '.'|| element == '?'|| element == '$'|| element == '!'|| element == '&'|| element == '%'|| element == '\"'|| element == '\''|| element == ':'|| element == ','|| element == ';'|| element == '@'|| element == '#'|| element == '-'|| element == '('|| element == ')') {
		            iterator.remove();
		        }
		    }
		    //String revised = (String)set.toString();
	System.out.println("s is now: "+set);
		    return set;
		}
		
		public static void hw1(String input, String output){
		try {
			 String alphabet = "abcdefghijklmnopqrstuvwxyz";
			 Set<Character> alpha = new HashSet<Character>();
			 Set<Character> s2 = new HashSet<Character>();
			    for(int i = 0; i < alphabet.length(); i++){
			    	alpha.add(alphabet.charAt(i));
			    }
			BufferedWriter write = new BufferedWriter(new FileWriter(output));
			BufferedReader read = new BufferedReader(new FileReader(input));
			String s1;
			while((s1 = read.readLine()) != null){
				s2 = cleanup(s1);
	System.out.println(s2);
	System.out.println(alpha);
				if(s2.equals(alpha)){
					write.write("true\n");
				}else{
					write.write("false\n");
				}
			}
			read.close();
			write.close();
		} catch (IOException e) {
			System.out.println("Error Occured:\n");
			e.printStackTrace();
		}
		}
		
	}

