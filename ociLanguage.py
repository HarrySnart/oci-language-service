import oci

class ociLanguage():
    def __init__(self):
        try:
            self.ai_client = oci.ai_language.AIServiceLanguageClient(oci.config.from_file())
        except Exception as e:
            print('No OCI Config file detected, please setup the OCI SDK')
        
    def detectLanguage(self,text):
        ''' Detect language of input string, returning code '''
        ai_client = self.ai_client
        doc1 = oci.ai_language.models.DominantLanguageDocument(key='key1', text=text)
        documents = [doc1]
        batch_detect_dominant_language_details = oci.ai_language.models.BatchDetectDominantLanguageDetails(documents=documents)
        output = ai_client.batch_detect_dominant_language(batch_detect_dominant_language_details)
        return output.data.documents[0].languages[0].code


    def translateText(self, input_text, language_code):
        ''' Translate text to English if not already English '''
        ai_client = self.ai_client
        text_document =  oci.ai_language.models.TextDocument(
             key="1",
             text=input_text,
             language_code=language_code)

        try:
            # Run text classification on text_document
            text_translation = ai_client.batch_language_translation(
                batch_language_translation_details=oci.ai_language.models.BatchLanguageTranslationDetails(
                    documents=[text_document],
                    target_language_code="en"
                )
            )

            return text_translation.data.documents[0].translated_text

        # Print any API errors
        except Exception as e:
            print(e)
        return
        
    def ociTranslate(self,input_texts):
        ''' translate batch of strings from a list '''
        final_strings = []
        for sentence in input_texts:
            language_code = self.detectLanguage(sentence)

            if language_code != 'en':
                try:
                    sentence = self.translateText(sentence, language_code)
                except:
                    print('language not supported!')
                    sentence = 'language not supported for:'+sentence
            final_strings.append(sentence)
        return final_strings

    




