import java.util.Set;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;

import safar.basic.morphology.stemmer.factory.StemmerFactory;
import safar.basic.morphology.stemmer.interfaces.IStemmer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

import java.util.HashSet;
import java.io.File;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.charset.Charset;
import java.nio.file.Paths;
import java.util.Arrays;


/**
 * Reads all files in a directory and stem them with the specified stemmer
 *
 */
public class SafarStem {

	private static final Set<String> stemmers = new HashSet<String>(Arrays.asList(
			new String[] {"KHOJA STEMMER", "LIGHT10", "ISRI", "MOTAZ STEMMER", "TASHAPHYNE"}
	));

	public static void main(String[] args) {
		String filePathIn = args[0];
		String filePathOut = args[1];
		String stemmerStr = args[2];
		
		if ( !stemmers.contains(stemmerStr)) {
			System.out.println("Invalid stemmer \""+ stemmerStr +"\".");
			System.exit(1);
		}

		// Create output directory if it doesn't exists
		File directory = new File(filePathOut);
	    if (!directory.exists()){
	        directory.mkdirs();
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
			
			System.out.println("Stemming "+basename+".txt");
			
			IStemmer stemmer = StemmerFactory.getImplementation(stemmerStr);
			String filenameOut = Paths.get(filePathOut, basename+".xml").toString();
			stemmer.stem(normalizedText, new File(filenameOut));
		}

		// TODO: add name of stemmer to XML (actually, SAFAR should do this)

	}

}
