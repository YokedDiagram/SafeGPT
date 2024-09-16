# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 10:54:58 2024

@author: HamzaHussain
"""
import pprint
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import TransformersNlpEngine
from presidio_analyzer import RecognizerRegistry
from presidio_anonymizer import AnonymizerEngine

text = "My name is Mr. Don and my phone number is 212-555-5555 and my zip is M3J 1L1"

# Define which transformers model to use
model_config = [{"lang_code": "en", "model_name": {
    "spacy": "en_core_web_sm",  # use a small spaCy model for lemmas, tokens etc.
    "transformers": "dslim/bert-base-NER"
    }
}]

# Define Custom Pattern Recognizers
yaml_file = "./CustomEntities/recognizers.yaml"

# Set up the engine, loads the NLP module (spaCy model by default) 
# and other PII recognizers
nlp_engine = TransformersNlpEngine(models=model_config)
analyzer = AnalyzerEngine(nlp_engine=nlp_engine)
analyzer.registry.add_recognizers_from_yaml(yaml_file)


# Call analyzer to get results
results = analyzer.analyze(text=text, language='en', return_decision_process=True)
print(results)
for result in results:
    decision_process = result.analysis_explanation
    
    pp = pprint.PrettyPrinter()
    print("Decision process output:\n")
    pp.pprint(decision_process.__dict__)

# Analyzer results are passed to the AnonymizerEngine for anonymization

anonymizer = AnonymizerEngine()

anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)

print(anonymized_text)