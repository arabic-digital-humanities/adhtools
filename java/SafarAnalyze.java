import java.util.Set;

import org.apache.commons.io.FilenameUtils;

import safar.basic.morphology.analyzer.factory.MorphologyAnalyzerFactory;
import safar.basic.morphology.analyzer.interfaces.IMorphologyAnalyzer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

import java.util.HashSet;
import java.io.File;
import java.io.FilenameFilter;
import java.nio.file.Paths;
import java.util.Arrays;


/**
 * Reads all files in a directory and analyzes them with the specified analyzer
 *
 */
public class SafarAnalyze {
	
	private static final Set<String> analyzers = new HashSet<String>(Arrays.asList(
			new String[] {"Alkhalil", "BAMA", "MADAMIRA"}
	));

	public static void main(String[] args) {
		String filePathIn = args[0];
		String filepathOut = args[1];
		String analyzerStr = args[2];
		
		if ( !analyzers.contains(analyzerStr)) {
			System.out.println("Invalid analyzer \""+ analyzerStr +"\".");
			System.exit(1);
		}
		
		// List all .txt files
		File directoryIn  = new File(filePathIn);
		File [] inFiles = directoryIn.listFiles(new FilenameFilter() {
		    @Override
		    public boolean accept(File dir, String name) {
		        return name.endsWith(".txt");
		    }
		});
		for(File fileIn : inFiles) {
			String basename = FilenameUtils.getBaseName(fileIn.getName());
			// Normalize
			System.out.println("Normalizing file "+basename);
			INormalizer normalizer = NormalizerFactory.getSAFARNormalizerImplementation();
			String normalizedText = normalizer.normalize(fileIn, "utf-8");
			
			IMorphologyAnalyzer analyzer = MorphologyAnalyzerFactory.getImplementation(analyzerStr);
			String filenameOut = Paths.get(filepathOut, basename+".xml").toString();
			analyzer.analyze(normalizedText, new File(filenameOut));
		}
		
		
		
		
		
		// TODO: add name of analyzer to XML (actually, SAFAR should do this)

	}

}
