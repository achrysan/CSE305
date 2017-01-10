val alpha = "abcdefghijklmnopqrstuvwxyz"
val myList = explode(alpha)
 
(* fun toUpper(myChar: char) =
   let exception invalidCharacter;
   in if ord(myChar) >= ord(#"A") andalso ord(myChar) <= ord(#"Z") then myChar
      else
       if ord(myChar) >= ord(#"a") andalso ord(myChar) <= ord(#"z") then
           chr(ord(myChar) - (ord(#"a") - ord(#"A")))
       else raise invalidCharacter
 end*)

fun helper3(charFromString: char, []) = false
| helper3(charFromString : char, a::b ) =
if charFromString = a then true else helper3(charFromString,b)      

fun helper2(a::b,[]) = true 
| helper2(a::b, c::d) = let val myChar = c in if helper3(myChar, a::b) = true then helper2(a::b,d) else false end



fun hw1(inFile : string, outFile : string) =
let
    val inStream = TextIO.openIn inFile
    val outStream = TextIO.openOut outFile
    val readLine = TextIO.inputLine inStream
    fun helper(readLine : string option) =
        case readLine of
                NONE => ( TextIO.closeIn inStream; TextIO.closeOut outStream)
            | SOME(c) =>( if helper2(explode(c), myList) = true then TextIO.output(outStream, "true\n") else TextIO.output(outStream, "false\n");
            helper(TextIO.inputLine inStream))
        
in 
    helper(readLine)
end

val _ = hw1("input.txt", "output.txt")
