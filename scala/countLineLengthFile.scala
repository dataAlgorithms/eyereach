//Code
import scala.io.Source

def widthOfLength(s: String) = s.length.toString.length

if (args.length > 0) {
    val lines = Source.fromFile(args(0)).getLines().toList
    val longestLine = lines.reduceLeft(
        (a, b) => if (a.length > b.length) a else b
    )

    val maxWidth = widthOfLength(longestLine)
    for (line <- lines) {
        val numSpaces = maxWidth - widthOfLength(line)
        val padding = " " * numSpaces
        println(padding + line.length + " | " + line)
    }
}
else
    Console.err.println("Please enter filename:")
    
//Output
/*
22 | import scala.io.Source
 0 |
55 | def widthOfLength(s: String) = s.length.toString.length
 0 |
22 | if (args.length > 0) {
58 |     val lines = Source.fromFile(args(0)).getLines().toList
39 |     val longestLine = lines.reduceLeft(
51 |         (a, b) => if (a.length > b.length) a else b
 5 |     )
 0 |
45 |     val maxWidth = widthOfLength(longestLine)
25 |     for (line <- lines) {
54 |         val numSpaces = maxWidth - widthOfLength(line)
37 |         val padding = " " * numSpaces
53 |         println(padding + line.length + " | " + line)
 5 |     }
 1 | }
 4 | else
49 |     Console.err.println("Please enter filename:")
*/
