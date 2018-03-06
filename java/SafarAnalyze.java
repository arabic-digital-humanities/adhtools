import java.util.Set;

import org.apache.commons.io.FilenameUtils;

import safar.basic.morphology.analyzer.factory.MorphologyAnalyzerFactory;
import safar.basic.morphology.analyzer.interfaces.IMorphologyAnalyzer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

import java.util.HashSet;
import java.io.File;
import java.nio.file.Paths;
import java.util.Arrays;

public class SafarAnalyze {
	
	private static final Set<String> analyzers = new HashSet<String>(Arrays.asList(
			new String[] {"Alkhalil", "BAMA", "MADAMIRA"}
	));

	public static void main(String[] args) {
		String fileIn = args[0];
		String filepathOut = args[1];
		String analyzerStr = args[2];
		
		String basename = FilenameUtils.getBaseName(fileIn);
		
		if ( !analyzers.contains(analyzerStr)) {
			System.out.println("Invalid analyzer \""+ analyzerStr +"\".");
			System.exit(1);
		}
		
		// Normalize
		System.out.println("Normalizing...");
		INormalizer normalizer = NormalizerFactory.getSAFARNormalizerImplementation();
		String normalizedText = normalizer.normalize(new File(fileIn), "utf-8");
		
		IMorphologyAnalyzer analyzer = MorphologyAnalyzerFactory.getImplementation(analyzerStr);
		String filenameOut = Paths.get(filepathOut, basename+".xml").toString();
		analyzer.analyze(normalizedText, new File(filenameOut));
		
		// TODO: add name of analyzer to XML (actually, SAFAR should do this)

	}

}
