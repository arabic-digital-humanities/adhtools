import java.util.Set;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;

import org.apache.commons.io.FilenameUtils;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

import common.constants.Language;
import safar.basic.morphology.analyzer.factory.MorphologyAnalyzerFactory;
import safar.basic.morphology.analyzer.interfaces.IMorphologyAnalyzer;
import safar.basic.morphology.analyzer.model.WordMorphologyAnalysis;
import safar.basic.morphology.analyzer.util.*;
import safar.util.normalization.factory.NormalizerFactory;
import safar.util.normalization.impl.SAFARNormalizer;
import safar.util.normalization.interfaces.INormalizer;
import safar.util.splitting.impl.SAFARSentenceSplitter;

import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FilenameFilter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Collections;


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
		String filePathOut = args[1];
		String analyzerStr = args[2];
		
		if ( !analyzers.contains(analyzerStr)) {
			System.out.println("Invalid analyzer \""+ analyzerStr +"\".");
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
			System.out.println("Reading file "+basename);
			
			 try {
				BufferedReader in = new BufferedReader(new FileReader(fileIn));
				SAFARNormalizer normalizer = new SAFARNormalizer();
				List<WordMorphologyAnalysis> wordMorphologyAnalysis = new LinkedList<WordMorphologyAnalysis>();
				int i = 0;
				for(String sentence = in.readLine(); sentence != null; sentence = in.readLine()) {
					String normalizedText = normalizer.normalize(sentence);
					
					IMorphologyAnalyzer analyzer = MorphologyAnalyzerFactory.getImplementation(analyzerStr);
					List<WordMorphologyAnalysis> wordList = analyzer.analyze(normalizedText); 
					
					wordMorphologyAnalysis.addAll(wordList);
					
					i++;
				}
				System.out.println("Number of sentences: "+i);
				in.close();
				System.out.println("Number of analyzed words: " +wordMorphologyAnalysis.size());
				
				
				// Save in chunks of n words
				int n = 1000;
				List<File> chunkfiles = new LinkedList<File>(); 
				for(int j=0; j<wordMorphologyAnalysis.size(); j+=n) {
					int k = Math.min(j+n, wordMorphologyAnalysis.size());
					System.out.println("Sublist from "+j+" to "+k);
					List<WordMorphologyAnalysis> sublist = wordMorphologyAnalysis.subList(j, k);
					
					String filenameOut = Paths.get(filePathOut, basename+".sub"+j+".xml").toString();
					File fileOut = new File(filenameOut);
					chunkfiles.add(fileOut);
					Utilities.saveAnalysisResultAsXML(sublist, fileOut, Language.ENGLISH);
				}
				
				//Merge the docsDocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
				DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
				DocumentBuilder db = dbf.newDocumentBuilder();
				Document docOut = null;
				for(File file : chunkfiles) {
					Document doc = db.parse(file);
					if(docOut==null) {
						docOut = doc;
					}
					else {
						
					}
				}
	            
				
			 } catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			 } catch (ParserConfigurationException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (SAXException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		
		
		
		
		// TODO: add name of analyzer to XML (actually, SAFAR should do this)

	}

}
