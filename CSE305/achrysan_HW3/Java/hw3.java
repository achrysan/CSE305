
import java.io.IOException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Stack;
import java.io.*;

public class hw3 {
	
	private static Stack myStack = new Stack();
	private static HashMap myMap = new HashMap();
	public static void hw3(String input, String output){
		try {
			
		BufferedWriter write = new BufferedWriter(new FileWriter(output));
		BufferedReader read = new BufferedReader(new FileReader(input));
		String line;
		while((line = read.readLine()) != null){
			line = line.replace("\n","");
			System.out.println("The line is: "+line);
			if(line.length()>3 && !line.equals(":true:") && !line.equals(":false:") && !line.equals(":error:")  && !line.equals("swap") && !line.equals("equal") && !line.equals("bind") && !line.equals("lessThan") && !line.equals("quit")){
			if(line.substring(0, 4).equals("push")){
				try{
					String value = line.substring(5,  line.length());
					if(value.charAt(0) == '\"' && value.charAt(value.length()-1) == '\"'){
						value = value.substring(1, value.length()-1);
						value = value +'`';
						myStack.push(value);
					}
					else if(Character.isLetter(value.charAt(0))){
						myStack.push(value);
					}else{
				myStack.push(Integer.parseInt(line.substring(5, line.length())));
					}
				System.out.println(line.substring(5, line.length())+" is being pushed onto the stack.");
				System.out.println("The Stack now contains:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
				}catch(Exception e){
					myStack.push(":error:");
					System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
				}
			}else{ myStack.push(":error:");
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");}
			}else if(line.equals("pop")){
				try{
				myStack.pop();
				System.out.println("An element is being popped off!");
				}catch(Exception e){
					myStack.push(":error:");
				}
			}else if(line.equals(":true:") ||line.equals(":false:")||line.equals(":error:")){
				myStack.push(line);
				System.out.println(line +" is being pushed onto the stack.");
				System.out.println("The Stack now contains:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else if(line.equals("add")){
				add_vals();
			}else if(line.equals("sub")){
				sub_vals();
			}else if(line.equals("mul")){
				mul_vals();
			}else if(line.equals("div")){
				div_vals();
			}else if(line.equals("rem")){
				rem_vals();
			}else if(line.equals("neg")){
				neg_vals();
			}else if(line.equals("swap")){
				swap_vals();
			}else if(line.equals("and")){
				comp_and();
			}else if(line.equals("or")){
				comp_or();
			}else if(line.equals("not")){
				comp_not();
			}else if(line.equals("equal")){
				comp_equal();
			}else if(line.equals("lessThan")){
				comp_lessThan();
			}else if(line.equals("bind")){
				comp_bind();
			}else if(line.equals("if")){
				comp_if();
			}else if(line.equals("let")){
				myStack.push("xletx");
			}else if(line.equals("end")){
				Object topval = myStack.peek();
				myStack.pop();
				while(myStack.peek() != "xletx"){
					myStack.pop();
				}
				myStack.pop();
				myStack.push(topval);
			}else if(line.equals("quit")){
				System.out.println("This is what is being printed to the File: ");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
				for(int i = 0; i<myStack.size(); i++){
					if(myStack.get(i) instanceof String){
						String item = (String) myStack.get(i);
						if(item.charAt(item.length()-1) == '`'){
							item = item.substring(0, item.length()-1);
							myStack.remove(i);
							myStack.insertElementAt(item, i);
						}else{
							continue;
						}
					}
				}
				Iterator<Object> iter = myStack.iterator();
				for(int i = myStack.size()-1; i>=0; i--){
					write.write(myStack.get(i).toString());
					write.newLine();
				}
				
				//System.exit(0);
			}else{
				myStack.push(":error:");
				}
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		read.close();
		write.close();
	} catch (IOException e) {
		System.out.println("Error Occured:\n");
		e.printStackTrace();
	}
		
	}

	private static void comp_if() {
		if(myStack.size() > 2){
			Object temp0 = myStack.peek();
			Object temp1 = myStack.get(myStack.size()-2);
			Object myVal_1 = myStack.peek();
			Object myVal_2 = myStack.get(myStack.size()-2);
			Object myVal_3 = myStack.get(myStack.size()-3);
			System.out.println("myval2: "+myVal_2);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myMap.containsKey(myVal_3)){
				myVal_3 = myMap.get(myVal_3);
			}
			if(myVal_3.equals(":true:") || myVal_3.equals(":false:")){
				if(myVal_3.equals(":true:")){
					myStack.pop();
					myStack.pop();
					myStack.pop();
					myStack.push(temp0);
				}else if(myVal_3.equals(":false:")){
					myStack.pop();
					myStack.pop();
					myStack.pop();
					myStack.push(temp1);
				}
			}else{
				myStack.push(":error:");
			}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_bind() {
		if(myStack.size() > 1){
			if(myStack.get(myStack.size()-2) instanceof String){
				String x = (String) myStack.get(myStack.size()-2);
				if(x.charAt(x.length()-1) == '`' || x.equals(":error:") || x.equals("xletx") || x.equals(":true:") || x.equals(":false:") || x.equals(":unit:") || myStack.peek().equals(":error:")){
					myStack.push(":error:");
				}else{
					myMap.put(x, myStack.peek());
					Object origVal = myMap.get(x);
					System.out.println("x: "+x);
					if(myMap.containsKey(x)){
						if(myMap.containsKey(origVal)){
							myMap.put(x, myMap.get(origVal));
						}
					}
					myStack.pop();
					myStack.pop();
					myStack.push(":unit:");
				}
			}else{
				myStack.push(":error:");
			}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_lessThan() {
		if(myStack.size() >1){
		Object myVal_1 = myStack.peek();
		Object myVal_2 = myStack.get(myStack.size()-2);
		System.out.println("myVak_1: "+myVal_1);
		System.out.println("myVak_2: "+myVal_2);
		if(myMap.containsKey(myVal_1)){
			myVal_1 = myMap.get(myVal_1);
		}
		if(myMap.containsKey(myVal_2)){
			myVal_2 = myMap.get(myVal_2);
		}
		if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
			if((int)myVal_2 < (int)myVal_1){
				myStack.pop();
				myStack.pop();
				myStack.push(":true:");
			}else{
				myStack.pop();
				myStack.pop();
				myStack.push(":false:");
			}
		}else{
			myStack.push(":error:");
		}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_equal() {
		if(myStack.size() > 1){
			Object myVal_1 = myStack.peek();
			Object myVal_2 = myStack.get(myStack.size()-2);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				if((int)myVal_1 == (int)myVal_2){
					
					myStack.pop();
					myStack.pop();
					myStack.push(":true:");
				}else{
					myStack.pop();
					myStack.pop();
					myStack.push(":false:");
				}
			}else{
				myStack.push(":error:");
			}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_not() {
		if(myStack.size() > 0){
		Object myVal_1 = myStack.peek();
		if(myMap.containsKey(myVal_1)){
			myVal_1 = myMap.get(myVal_1);
		}
		if(!(myVal_1.equals(":true:")) && !(myVal_1.equals(":false:"))){
			myStack.push(":error:");
		}else{
			if(myVal_1.equals(":true:")){
				myStack.pop();
				myStack.push(":false:");
			}else if(myVal_1.equals(":false:")){
				myStack.pop();
				myStack.push(":true:");
			}
		}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_or() {
		if(myStack.size() > 1){
			Object myVal_1 = myStack.peek();
			Object myVal_2 = myStack.get(myStack.size()-2);
				if(myMap.containsKey(myVal_1)){
					myVal_1 = myMap.get(myVal_1);
				}
				if(myMap.containsKey(myVal_2)){
					myVal_2 = myMap.get(myVal_2);
				}
			
				if(!(myVal_1.equals(":true:")) && !(myVal_1.equals(":false:")) || !(myVal_2.equals(":true:")) && !(myVal_2.equals(":false:"))){
					myStack.push(":error:");
				}else{
					if(myVal_1.equals(myVal_2)){
						Object temp = myVal_1;
						myStack.pop();
						myStack.pop();
						myStack.push(temp);
					}else if(myVal_1.equals(":true:") || myVal_2.equals(":true:")){
						myStack.pop();
						myStack.pop();
						myStack.push(":true:");
					}
				}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void comp_and() {
		if(myStack.size() > 1){
			Object myVal_1 = myStack.peek();
			Object myVal_2 = myStack.get(myStack.size()-2);
				if(myMap.containsKey(myVal_1)){
					myVal_1 = myMap.get(myVal_1);
				}
				if(myMap.containsKey(myVal_2)){
					myVal_2 = myMap.get(myVal_2);
				}
			
				if(!(myVal_1.equals(":true:")) && !(myVal_1.equals(":false:")) || !(myVal_2.equals(":true:")) && !(myVal_2.equals(":false:"))){
					myStack.push(":error:");
				}else{
					if(myVal_1.equals(myVal_2)){
						Object temp = myVal_1;
						myStack.pop();
						myStack.pop();
						myStack.push(temp);
					}else if(myVal_1.equals(":false:") || myVal_2.equals(":false:")){
						myStack.pop();
						myStack.pop();
						myStack.push(":false:");
					}
				}
		}else{
			myStack.push(":error:");
		}
		
	}

	private static void swap_vals() {
		System.out.println("swapping");
		if(myStack.size()>1){
			Object temp = myStack.pop();
			Object temp2 = myStack.pop();
			myStack.push(temp);
			myStack.push(temp2);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
	}

	private static void neg_vals() {
		System.out.println("negating");
		if(myStack.size()>0){
			Object myVal_1 = myStack.peek();
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myVal_1 instanceof Integer){
				Object myVal1 = myStack.pop();
				if(myMap.containsKey(myVal1)){
					myVal1 = myMap.get(myVal1);
					//myVal_1 = Integer.parseInt(myVal_1);
				}
			int	result = 0 - ((int)myVal1);
			System.out.println("result: "+result);
			myStack.push(result);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		
	}

	private static void rem_vals() {
		System.out.println("modulating");
		if(myStack.size()>1){
			Object myVal_1 = myStack.peek();
			Object temp = myStack.pop();
			Object myVal_2 = myStack.peek();
			myStack.push(temp);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
				if(myMap.containsKey(myVal1)){
					myVal1 = myMap.get(myVal1);
					//myVal_1 = Integer.parseInt(myVal_1);
				}
				if(myMap.containsKey(myVal2)){
					myVal2 = myMap.get(myVal2);
				}
			int	result = ((int) myVal2) % ((int)myVal1);
			System.out.println("result: "+result);
			myStack.push(result);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		
	}

	private static void div_vals() {
		System.out.println("dividing");
		if(myStack.size()>1){
			Object myVal_1 = myStack.peek();
			Object temp = myStack.pop();
			Object myVal_2 = myStack.peek();
			myStack.push(temp);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
				if(myMap.containsKey(myVal1)){
					myVal1 = myMap.get(myVal1);
					//myVal_1 = Integer.parseInt(myVal_1);
				}
				if(myMap.containsKey(myVal2)){
					myVal2 = myMap.get(myVal2);
				}
			int	result = ((int) myVal2) / ((int)myVal1);
			System.out.println("result: "+result);
			myStack.push(result);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		
	}

	private static void mul_vals() {
		System.out.println("multiplying");
		if(myStack.size()>1){
			Object myVal_1 = myStack.peek();
			Object temp = myStack.pop();
			Object myVal_2 = myStack.peek();
			myStack.push(temp);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
				if(myMap.containsKey(myVal1)){
					myVal1 = myMap.get(myVal1);
					//myVal_1 = Integer.parseInt(myVal_1);
				}
				if(myMap.containsKey(myVal2)){
					myVal2 = myMap.get(myVal2);
				}
			int	result = ((int) myVal2) * ((int)myVal1);
			System.out.println("result: "+result);
			myStack.push(result);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		
	}

	private static void sub_vals() {
		System.out.println("subtracting");
		if(myStack.size()>1){
			Object myVal_1 = myStack.peek();
			Object temp = myStack.pop();
			Object myVal_2 = myStack.peek();
			myStack.push(temp);
			System.out.println("myVal_1: "+myVal_1);
			System.out.println("myVal_2: "+myVal_2);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
				if(myMap.containsKey(myVal1)){
					myVal1 = myMap.get(myVal1);
					//myVal_1 = Integer.parseInt(myVal_1);
				}
				if(myMap.containsKey(myVal2)){
					myVal2 = myMap.get(myVal2);
				}
			int	result = ((int) myVal2) - ((int)myVal1);
			System.out.println("result: "+result);
			myStack.push(result);
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
			}else{
				myStack.push(":error:");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
			}
		
		
	}

	private static void add_vals() {
		System.out.println("adding");
		if(myStack.size()>1){
			Object myVal_1 = myStack.peek();
			Object temp = myStack.pop();
			Object myVal_2 = myStack.peek();
			myStack.push(temp);
			if(myMap.containsKey(myVal_1)){
				myVal_1 = myMap.get(myVal_1);
			}
			if(myMap.containsKey(myVal_2)){
				myVal_2 = myMap.get(myVal_2);
			}
		if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
			Object myVal1 = myStack.pop();
			Object myVal2 = myStack.pop();
			if(myMap.containsKey(myVal1)){
				myVal1 = myMap.get(myVal1);
				//myVal_1 = Integer.parseInt(myVal_1);
			}
			if(myMap.containsKey(myVal2)){
				myVal2 = myMap.get(myVal2);
			}
		int	result = ((int) myVal2) + ((int)myVal1);
		System.out.println("result: "+result);
		myStack.push(result);
		System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
		}else{
			myStack.push(":error:");
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
		}
		}else{
			myStack.push(":error:");
			System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
		}
		
	}

}
