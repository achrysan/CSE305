//package hw2;

import java.io.IOException;
import java.util.Iterator;
import java.util.Stack;
import java.io.*;

public class hw2 {
	
	private static Stack myStack = new Stack();
	public static void hw2(String input, String output){
		try {
			
		BufferedWriter write = new BufferedWriter(new FileWriter(output));
		BufferedReader read = new BufferedReader(new FileReader(input));
		String line;
		while((line = read.readLine()) != null){
			line = line.replace("\n","");
			System.out.println("The line is: "+line);
			if(line.length()>3 && !line.equals(":true:") && !line.equals(":false:") && !line.equals(":error:")  && !line.equals("swap") && !line.equals("quit")){
			if(line.substring(0, 4).equals("push")){
				try{
				myStack.push(Integer.parseInt(line.substring(5, line.length())));
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
			}else if(line.equals("quit")){
				System.out.println("This is what is being printed to the File: ");
				System.out.print(myStack.toString().replaceAll("\\[", "").replaceAll("]", "")+"\n"+"\n");
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
			if(myVal_1 instanceof Integer){
				Object myVal1 = myStack.pop();
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
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
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
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
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
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
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
			if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
				Object myVal1 = myStack.pop();
				Object myVal2 = myStack.pop();
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
		if(myVal_1 instanceof Integer && myVal_2 instanceof Integer){
			Object myVal1 = myStack.pop();
			Object myVal2 = myStack.pop();
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
