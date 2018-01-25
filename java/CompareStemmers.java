import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

import common.constants.Stemmer;
import safar.basic.morphology.stemmer.factory.StemmerFactory;
import safar.basic.morphology.stemmer.interfaces.IStemmer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

/**
 * @author Dafne van Kuppevelt
 * This java program takes a file with Arabic text as input, applies several stemmers 
 * and outputs an XML file for each stemmer.
 * Make sure to add the Safar binaries to your classpath.
 */
public class CompareStemmers {

	public static void main(String[] args) {
		String fileIn = args[0];
		String filepathOut = args[1];
		
		// Normalize
		System.out.println("Normalizing...");
		INormalizer normalizer = NormalizerFactory.getSAFARNormalizerImplementation();
		String normalizedText = normalizer.normalize(new File(fileIn), "utf-8");
		
		String[] stemmers = {
				"ISRI",
				"KHOJA STEMMER",
				"LIGHT10",
				"MOTAZ STEMMER",
				"SAFAR Stemmer",
				"TASHAPHYNE ROOT",
				"TASHAPHYNE"
		};
		System.out.println("Stemming...");
		for(String stemmerStr : stemmers){
			System.out.println("Stem with " + stemmerStr);
			IStemmer stemmer = StemmerFactory.getImplementation(stemmerStr);
			String filenameOut = Paths.get(filepathOut, "results_"+stemmerStr.replace(' ', '_')+".xml").toString();
			stemmer.stem(normalizedText, new File(filenameOut));
		}	
	}

}
