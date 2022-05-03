# DELA-Project
DELA stands for Document-level machinE transLation evAlaution. 


# DELA CORPUS

The corpus is segmented by sentence (checked mannually). The issues tagged here are issues that would occur in a translation from English into Brazilian Portuguese when no context information is given. Issues that are solved within the single sentence are not tagged. 

The issues tagged are:

  - Ellipsis
  - Gender
  - Lexical ambiguity
  - Number
  - Reference
  - Terminology


The annotation was performed for each sentence, which are tagged one per line, in the order they appear in the sentence, followed by their explanation/solution, along with modifications performed in the source (if any) and translations of some cases and notes. 
Sentences with no context-related issues are followed by two Xs for the issue and the solution. 
For Reference and Ellipsis, the term that contains the issue is stated along with an equals sign (=) and the explanation of what it refers to. For Gender and Number, the issue is tagged along with an equals sign (=) and the solution (feminine/masculine or singular/plural) is given. For Lexical Ambiguity and Terminology, the term (or terms) is stated along with an equals sign (=) and a contrasting solution is given, the wrong meaning(s) compared to (vs) the correct one. 

The corpus is available in two formats: 

  - One is a spreadsheet (.xls) format, containing the tagged corpus in all domains and full information. This .xls format will allow for filtering specific issues or sentences and enable users/researchers to see the rationale of the annotation. 

  - Second is plain text (.txt) format, containing the segment id, sentence, issue and explanation all in one line. Modifications and translation are not provided in this format. This format will allow for an automatic use of the corpus, for training or as a test suite.

Folders:
  
  - EN_ID: contains the files with the corpus in English, with sentence ID, in txt format. Each file contains one domain.
  - PT_BR translations_ID: contains the files with the corpus with the translation into PT-BR, with sentence ID, in txt format. Each file contains one domain.
  - Contex-related issues annotated: contains the files with the corpus in English annotated with the context-related issues, with sentence ID, in txt format. Each file contains one domain. It also contains the .xls file, a spreadsheet with the corpus and translation, with sentence ID, annotated and modifications performed int he source. Each tab is one domain. 
  - Guides: contains the guidelines (In English) and the Decision Tree. 

Please, see publication for more details.
