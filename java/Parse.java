import java.io.File;
import java.nio.file.Paths;

import safar.basic.syntax.parser.factory.ParserFactory;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;
import safar.util.splitting.impl.SAFARSentenceSplitter;
import safar.basic.syntax.parser.interfaces.IParser;
import safar.basic.syntax.parser.model.SentenceParsingAnalysis;
import common.constants.Parser;
import common.constants.ParserOutput;

public class Parse {

	public static void main(String[] args) {
		String fileIn = args[0];
		String filepathOut = args[1];
		
		// Normalize
		System.out.println("Normalizing...");
		INormalizer normalizer = NormalizerFactory.getSAFARNormalizerImplementation();
		String normalizedText = normalizer.normalize(new File(fileIn), "utf-8");
		String[] sentences = normalizedText.split("\n"); 
		System.out.println("Nr of sentences:" + sentences.length);
		IParser parser = ParserFactory.getImplementation(Parser.STANFORD_PARSER);
		// Set the output File
		String filenameOut = Paths.get(filepathOut, "results_StanfordParser2.xml").toString();
        File outputFile = new File(filenameOut);
        
        parser.parse(sentences, outputFile, ParserOutput.XML_TREE_WITH_DEPENDENCIES);
        
        // Parse the sentence and save results as xml File
        for(String sentence : sentences){
        	SentenceParsingAnalysis parsingAnalysis = parser.parse(sentence);
        	parsingAnalysis.printXMLTrees();
        }
        
	}

}
