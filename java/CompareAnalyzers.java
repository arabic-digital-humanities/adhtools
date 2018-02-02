import java.io.File;
import java.nio.file.Paths;

import safar.basic.morphology.analyzer.factory.MorphologyAnalyzerFactory;
import safar.basic.morphology.analyzer.interfaces.IMorphologyAnalyzer;
import safar.basic.morphology.stemmer.factory.StemmerFactory;
import safar.basic.morphology.stemmer.interfaces.IStemmer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

public class CompareAnalyzers {
	public static void main(String[] args) {
		String fileIn = args[0];
		String filepathOut = args[1];
		
		// Normalize
		System.out.println("Normalizing...");
		INormalizer normalizer = NormalizerFactory.getSAFARNormalizerImplementation();
		String normalizedText = normalizer.normalize(new File(fileIn), "utf-8");
		
		String[] analyzers = {
				"Alkhalil",
				"BAMA",
				"MADAMIRA"
		};
		System.out.println("Analyzing...");
		for(String analyzerStr : analyzers){
			System.out.println("Analyze with " + analyzerStr);
			IMorphologyAnalyzer analyzer = MorphologyAnalyzerFactory.getImplementation(analyzerStr);
			String filenameOut = Paths.get(filepathOut, "results_"+analyzerStr.replace(' ', '_')+".xml").toString();
			analyzer.analyze(normalizedText, new File(filenameOut));
		}	
	}
}