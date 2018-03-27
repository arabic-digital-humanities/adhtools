import org.apache.commons.io.FilenameUtils;

import safar.basic.morphology.stemmer.factory.StemmerFactory;
import safar.basic.morphology.stemmer.interfaces.IStemmer;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.interfaces.INormalizer;

import java.util.Map;
import java.io.File;
import java.io.FilenameFilter;
import java.nio.file.Paths;
import java.util.HashMap;


/**
 * Reads all files in a directory and stem them with the specified stemmer
 *
 */
public class SafarStem {

	private static final Map<String, String> stemmers = createMap();
    private static Map<String, String> createMap() {
        Map<String,String> stemmers = new HashMap<String,String>();
        stemmers.put("KHOJA", "KHOJA STEMMER");
        stemmers.put("LIGHT10", "LIGHT10");
        stemmers.put("ISRI", "ISRI");
        stemmers.put("MOTAZ", "MOTAZ STEMMER");
        stemmers.put("TASHAPHYNE", "TASHAPHYNE");
        
        return stemmers;
    }
	
	public static void main(String[] args) {
		String filePathIn = args[0];
		String filePathOut = args[1];
		String stemmerStr = args[2];
		
		if ( !stemmers.containsKey(stemmerStr) ) {
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
			
			IStemmer stemmer = StemmerFactory.getImplementation(stemmers.get(stemmerStr));
			String filenameOut = Paths.get(filePathOut, basename+".xml").toString();
			stemmer.stem(normalizedText, new File(filenameOut));
		}

		// TODO: add name of stemmer to XML (actually, SAFAR should do this)

	}

}
