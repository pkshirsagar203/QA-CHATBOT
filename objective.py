import re
import nltk
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:

    def __init__(self, data, noOfQues):
        self.summary = data
        self.noOfQues = noOfQues

    def get_trivial_sentences(self):
        sentences = nltk.sent_tokenize(self.summary)
        trivial_sentences = []
        for sent in sentences:
            trivial = self.identify_trivial_sentence(sent)
            if trivial:
                trivial_sentences.append(trivial)
        return trivial_sentences

    def identify_trivial_sentence(self, sentence):
        tags = nltk.pos_tag(nltk.word_tokenize(sentence))
        if tags[0][1] == "RB" or len(nltk.word_tokenize(sentence)) < 4:
            return None

        noun_phrases = self.extract_noun_phrases(sentence)
        replace_nouns = []

        for word, _ in tags:
            for phrase in noun_phrases:
                if phrase[0] == '\'':
                    break
                if word in phrase:
                    replace_nouns.extend(phrase.split()[-2:])
                    break
            if not replace_nouns:
                replace_nouns.append(word)
            break

        if not replace_nouns:
            return None

        val = min(len(word) for word in replace_nouns)
        trivial = {
            "Answer": " ".join(replace_nouns),
            "Key": val
        }

        if len(replace_nouns) == 1:
            trivial["Similar"] = self.answer_options(replace_nouns[0])
        else:
            trivial["Similar"] = []

        replace_phrase = " ".join(replace_nouns)
        blanks_phrase = ("__________ " * len(replace_nouns)).strip()
        expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
        sentence = expression.sub(blanks_phrase, sentence, count=1)
        trivial["Question"] = sentence
        return trivial

    def extract_noun_phrases(self, sentence):
        grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                   {<NN>+<IN|DT>*<NNP>+}
                   {<NNP>+<NNS>*}
        """
        chunker = nltk.RegexpParser(grammar)
        tokens = nltk.word_tokenize(sentence)
        pos_tokens = nltk.pos_tag(tokens)
        tree = chunker.parse(pos_tokens)

        noun_phrases = [" ".join([sub[0] for sub in subtree.leaves()]) 
                        for subtree in tree.subtrees() if subtree.label() == "CHUNK"]
        return noun_phrases

    @staticmethod
    def answer_options(word):
        synsets = wn.synsets(word, pos="n")

        if not synsets:
            return []

        hypernym = synsets[0].hypernyms()[0]
        hyponyms = hypernym.hyponyms()
        similar_words = [hyponym.lemmas()[0].name().replace("_", " ") for hyponym in hyponyms 
                         if hyponym.lemmas()[0].name().replace("_", " ") != word][:8]
        return similar_words

    def generate_test(self):
        trivial_pairs = self.get_trivial_sentences()
        question_answer = [que_ans_dict for que_ans_dict in trivial_pairs 
                           if que_ans_dict["Key"] > int(self.noOfQues)]
        
        if not question_answer:
            raise ValueError("No valid questions generated. Check the input text and ensure it contains enough meaningful content.")

        questions = []
        answers = []
        while len(questions) < int(self.noOfQues):
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in questions:
                questions.append(question_answer[rand_num]["Question"])
                answers.append(question_answer[rand_num]["Answer"])

        return questions, answers
