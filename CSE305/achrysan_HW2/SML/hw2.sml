
val myList = []

fun push(x, xs) = x::xs

fun pop ([]) = push(":error:", [])
   | pop(x::xs) = xs
 
fun top([]) = []
   | top(x::xs) = x
   
fun readlist (infile : string) = let 

  val ins = TextIO.openIn infile 

  fun loop ins = 

   case TextIO.inputLine ins of 

      SOME line => line :: loop ins 

    | NONE      => [] 

in 

  loop ins before TextIO.closeIn ins 

end ;

fun computeList(myStack, myList) =
if String.isSubstring "push" (hd(myList)) 
then computeList(myStack@[String.substring((hd(myList)),5,(size(hd(myList))-6))],tl(myStack)) 
else myStack

fun printList(list, index, outText) =
 if (List.length(list) > index) then (
  TextIO.output(outText, (List.nth(list, index) ^ "\n"));
  printList(list, index + 1, outText)
 ) else (
  TextIO.closeOut outText
 )

fun hw2(input : string, output : string)= 
let 
val read = readlist(input)
val computed = computeList([], read)
val write = TextIO.openOut output
in
printList(computed, 0, write)
end


  
 
 
   
val _ = hw2("input.txt", "output.txt")
   


(*let val newList = [] in if substring(c,0,4) = "push" then newList = push(substring(c,5,6), myList) else newList = myList end;*)

(*fun add() = 
    if size(myStack) > 1 then
        val myVal1 = top(myStack)
        pop(myStack)
        val myVal2 = top(myStack)
        pop(myStack)
        datatype wrapper = Int of int | Real of real | String of string
            case myVal1 of Int myVal1    -> case myVal2 of Int myVal2 -> pop(myStack); pop(myStack); val result = myVal1 + myVal2; push(myVal1, myStack) | Real myVal2 -> push(":error:", myStack) | String myVal2 -> push(":error:", myStack) 
            | Real myVal1   -> push(":error:",myStack)
            | String myVal1 -> push(":error:", myStack)
    else myStack.push(":error:", myStack)*)

(*val _ = copyTextFile("input.txt", "output.txt")*)