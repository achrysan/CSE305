(* CSE305 Spring 2016
 * A possible solution to HW2, expressed in Standard ML
 * Author: Carl Alphonce
 * Modified: Lu Meng
 *)

(****************************************************************************
 TYPE DEFINITIONS 
 ****************************************************************************)

(* The type of expressions and special forms *)
datatype exp =
    Boolean of bool
  | Number of int
  | String of string
  | Name of string
  | Error | Quit | Add | Sub | Mul | Div | Rem | Pop | Swap | Neg | And | Or | Not | Equal | LessThan | If | Bind;

(****************************************************************************
 UTILITY FUNCTIONS 
 ****************************************************************************)

(* Utility function to build a textual form of an expression
   or special form, used for printing.
 *)
fun expression2string(Boolean(true)) = ":true:"
  | expression2string(Boolean(false)) = ":false:"
  | expression2string(String(X)) = X
  | expression2string(Name(X)) = X
  | expression2string(Number(X)) = if (X<0) then "-"^Int.toString(~X) else Int.toString(X)
  | expression2string(Error) = ":error:"
  | expression2string(_) = "?? should not happen ??"
  ;


(* Computes quotient according to rules of the language *)
fun quotient(a2,a1) =
    if (a1<0)
    then if (a2 div a1) * a1 > a2 then (a2 div a1)+1 else (a2 div a1)
    else (a2 div a1);

(* Computes remainder according to rules of the language *)
fun remainder(a2,a1) = a2 - a1 * quotient(a2,a1);


(****************************************************************************
 MAIN EVALUATOR FUNCTIONS 
 ****************************************************************************)

(* Applies a primitive function to its two arguments *)

fun 
  (* 0-ARY OPERATORS *)
    apply(_,[])  = (Error,[])

  (* UNARY OPERATORS *)
  | apply(Neg,Number(a)::rest) = (Number(~a),rest)
  | apply(Not,Boolean(a)::rest) = if a = true then (Boolean(false),rest)                (*<-----Same Problem*)
                                    else if a = false then (Boolean(true),rest)
                                    else (Error,rest)                                   
  | apply(_,[x]) = (Error,[x])

  (* BINARY OPERATORS *)
  | apply(Add,Number(a1)::Number(a2)::rest) = (Number(a2+a1),rest)
  | apply(Sub,Number(a1)::Number(a2)::rest) = (Number(a2-a1),rest)
  | apply(Mul,Number(a1)::Number(a2)::rest) = (Number(a2*a1),rest)
  | apply(Div,Number(a1)::Number(a2)::rest) = if a1 = 0 then (Error,Number(a1)::Number(a2)::rest) else (Number(quotient(a2,a1)),rest)
  | apply(Rem,Number(a1)::Number(a2)::rest) = if a1 = 0 then (Error,Number(a1)::Number(a2)::rest) else (Number(remainder(a2,a1)),rest)
  | apply(Equal,Number(a1)::Number(a2)::rest) = if a1 = a2 then (Boolean(true),rest) else (Boolean(false),rest)
  | apply(LessThan,Number(a1)::Number(a2)::rest) = if a2 < a1 then (Boolean(true),rest) else (Boolean(false),rest)
  | apply(And,Boolean(a1)::Boolean(a2)::rest) = if a1 = false andalso a2 = true then (Boolean(false),rest) 
                                                 else if a2 = false andalso a1 = true then (Boolean(false),rest)
                                                 else if a1 = false andalso a2 = false then (Boolean(false),rest)
                                                 else if a1 = true andalso a2 = true then (Boolean(true),rest)
                                                 else if not(a1=true) andalso not(a1=false) andalso not(a2=true) andalso not(a2=false) then (Error,rest)
                                                 else (Error,rest)
  | apply(Or,Boolean(a1)::Boolean(a2)::rest) = if a1 = false andalso a2 = true then (Boolean(true),rest) 
                                                   else if a2 = false andalso a1 = true then (Boolean(true),rest)
                                                   else if a1 = false andalso a2 = false then (Boolean(false),rest)
                                                   else if a1 = true andalso a2 = true then (Boolean(true),rest)
                                                   else if not(a1=true) andalso not(a1=false) andalso not(a2=true) andalso not(a2=false) then (Error,rest)
                                                   else (Error,rest)
 
  (*  TERNARY OPERATORS  *)
  | apply(If,a1::a2::Boolean(a3)::rest) = if a3 = true then (a1,rest) else (a2,rest)
  | apply(Bind, a1::a2::String(a3)::rest) = (String(":unit:"),rest)
  | apply(_,stack) = (Error,stack)
  ;

(* stack operations *)

fun stackOps(Pop, x::stack) = stack
  | stackOps(Swap, x::y::stack) = y::x::stack
  | stackOps(_,stack) = Error::stack
  ;

(* Evaluates an expression *)

fun eval(Boolean(x), stack) = Boolean(x)::stack
  | eval(Number(x), stack)  = Number(x)::stack
  | eval(String(x), stack) = String(x)::stack
  | eval(Name(x), stack) = Name(x)::stack
  | eval(Quit, stack)       = Quit::stack
  | eval(Pop, x::stack)     = stack
  | eval(Swap, x::y::stack)     = y::x::stack
  | eval(Error, stack)      = Error::stack
  | eval(expr, stack) = let
        val (v,s) = apply(expr, stack)
    in
        v::s
    end;

(* Functions to parse a number *)

fun parseNumber(x,inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isDigit(ch)) then parseNumber(x*10+(ord(ch)-ord(#"0")),inStr)
       else if (Char.isSpace(ch)) then SOME(Number(x))
       else SOME(Error)
      ;

fun parseNegativeNumber(inStr) = 
    case ( parseNumber(0,inStr) ) of
        NONE => SOME(Error)
      | SOME(Number(num)) =>  SOME(Number(~1 * num))
      | SOME(_) => SOME(Error) 
      ;

(* Function to parse a boolean  *)

fun parseBoolean(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch) orelse ch = #":") then parseBoolean(x^Char.toString(ch),inStr)
       else if (Char.isSpace(ch))
	       then if (x = ":true:")  then SOME(Boolean(true))
	       else if (x = ":false:") then SOME(Boolean(false))
	       else SOME(Error)
       else SOME(Error);

(* Function to parse an error *)

fun parseError(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch) orelse ch = #":") then parseError(x^Char.toString(ch),inStr)
       else if (Char.isSpace(ch))
	       then if (x = ":error:")  then SOME(Error)
	       else SOME(Error)
       else SOME(Error);

(***** EDITED TO HERE ********************************************************************)

(* Function to parse a boolean or error  *)

fun parseBooleanOrError(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (ch = #"e")                  then parseError(x^Char.toString(ch),inStr)
       else if (ch = #"t" orelse ch = #"f") then parseBoolean(x^Char.toString(ch),inStr)
       else SOME(Error);


fun parseString(x, inStr) = 
    case (TextIO.input1(inStr)) of
    NONE => SOME(Error)
      | SOME(ch) =>
        if (Char.isAlpha(ch) orelse ch = #"\"") then parseString(x^Char.toString(ch),inStr)
        else if (Char.isSpace(ch)) then SOME(String(String.substring (x, 1, (size x) -3 )))
        else SOME(Error)
        
(* Function to parse a primitive  *)

fun parsePrimitive(x, inStr) = 
    case (TextIO.input1(inStr)) of
	NONE => SOME(Error)
      | SOME(ch) => 
	    if (Char.isAlpha(ch))  then parsePrimitive(x^Char.toString(ch),inStr)
       else if (ch = #"\n")
	       then if (x = "add") then SOME(Add)
	       else if (x = "sub") then SOME(Sub)
	       else if (x = "mul") then SOME(Mul)
	       else if (x = "div") then SOME(Div)
	       else if (x = "rem") then SOME(Rem)
	       else if (x = "pop") then SOME(Pop)
	       else if (x = "swap") then SOME(Swap)
	       else if (x = "neg") then SOME(Neg)
           else if (x = "and") then SOME(And)
           else if (x = "or") then SOME(Or)
           else if (x = "not") then SOME(Not)
           else if (x = "equal") then SOME(Equal)
           else if (x = "lessThan") then SOME(LessThan)
           else if (x = "if") then SOME(If)
           else if (x = "bind") then SOME(Bind)
           else if (x = "quit") then SOME(Quit)
	       else SOME(Name(x))
       else SOME(Error);

(* fun parsePush(inStr) = 
    case (TextIO.input1(inStr)) of
  NONE => SOME(Error)
      | SOME(ch) =>
      if (Char.isAlpha(ch)) then parsePush(inStr)
       else if (Char.isSpace(ch))
         then if (TextIO.input1(inStr) = SOME(c)) then
              (if c = #"-") then parseNegativeNumber(inStr)
              else parseNumber(ord(TextIO.input1(inStr))-ord(#"0"),inStr))
       else SOME(Error);
*)




(* A recursive helper function for the parse function, which reads
   a character from the input stream and determines what more
   specific parsing function to call.
 *)      
fun parseHelper(NONE, inStr) = NONE
  | parseHelper(SOME(ch), inStr) =

  let

    val line = Option.valOf (TextIO.inputLine inStr)
    val second = String.sub (line, 0)
    val inStr1 = TextIO.openString line

  in            
      if (ch = #"p" andalso second = #"u") then parseHelper(TextIO.input1(TextIO.openString (String.extract(line,4,NONE))), TextIO.openString (String.extract(line, 5, NONE)))
 else if (Char.isDigit(ch)) then parseNumber(ord(ch)-ord(#"0"),inStr1)
 else if (ch = #"\"")       then parseString("\"", inStr1)
 else if (ch = #"-")        then parseNegativeNumber(inStr1)
 else if (ch = #":")        then parseBooleanOrError(":", inStr1)
 else if (Char.isAlpha(ch)) then parsePrimitive(Char.toString(ch), inStr1)
 else if (ch = #"\n")       then parseHelper(TextIO.input1(inStr1), inStr1)
 else NONE
 end;


(* Function to parse the next expression on the input stream. *)      
fun parse(inStr) = parseHelper(TextIO.input1(inStr), inStr);







fun hw3(inFile : string, outFile : string) =
  let
    val fileInp = TextIO.openIn inFile
    val fileOut = TextIO.openOut outFile
    fun printStack([]) = ()
    | printStack(x::xs) = ( TextIO.output (fileOut, (expression2string(x)^"\n")) ; printStack(xs) );

    fun replHelper(inStr, stack) =
    (
      
      case (parse(inStr)) of 
         NONE => replHelper(inStr, stack)
        | SOME(Quit) => (printStack(stack); TextIO.closeIn fileInp; TextIO.closeOut fileOut) 
        | SOME(expression) => replHelper(inStr,eval(expression, stack)) 
    );

  in
    replHelper(fileInp, [])
  end

