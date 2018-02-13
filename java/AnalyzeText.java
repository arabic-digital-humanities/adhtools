

import com.google.gson.Gson;

import AlKhalil2.morphology.result.model.Result;

public class AnalyzeText {

	public static void main(String[] args) {
		String textToBeAnalysed = "سيدنا محمد صلى الله عليه وعلى آله الطيبين الطاهرين وعلى جميع الأنبياء";

		AlKhalil2.util.constants.Static.analyzer = new AlKhalil2.morphology.analyzer.AnalyzerTokens();
		
		AlKhalil2.text.tokenization.Tokenization tokens = new AlKhalil2.text.tokenization.Tokenization();
        tokens.setTokenizationString(textToBeAnalysed);

        System.out.println(tokens);
        int nbNoAnalyzedWord = 0;
        int nbAnalyzedWord = 0;
        int i=0;
        
        
        java.util.List l = new java.util.ArrayList();
        l.addAll(tokens.getTokens());
        java.util.Collections.sort(l);
        java.util.Iterator<String> it_normalized = l.iterator();
        //+-------------------------------------------+
        while( it_normalized.hasNext() ){
            String normalizedWord = it_normalized.next();
            //+-------------------------------------------+
            //AlKhalil2.ui.Gui.progressBar.setValue((int) 100 * (i + 1) / tokens.getNbTokens());
            //+-------------------------------------------+
            java.util.List result =  AlKhalil2.util.constants.Static.analyzer.analyzerToken(normalizedWord);
            //+-------------------------------------------+
            if(result.isEmpty()){
                nbNoAnalyzedWord += tokens.getTokensRepeat().get(normalizedWord);
            }
            else{
                nbAnalyzedWord += tokens.getTokensRepeat().get(normalizedWord);
            }
            //+-------------------------------------------+
            AlKhalil2.util.constants.Static.allResults.put(normalizedWord, result);
            System.out.println("Word: "+normalizedWord+"\t result:");
            for(Object resO : result){
            	Result res = (Result) resO;
            	Gson gson = new Gson();
            	System.out.println(gson.toJson(res));
            }
            //+-------------------------------------------+
            i++;
            //+-------------------------------------------+
        }
        //System.out.print(AlKhalil2.util.constants.Static.allResults);

	}

}
