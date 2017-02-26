import json

from django.test import TestCase, Client

from services import WordService
from words.models import Word


class WordServiceTestCase(TestCase):
    def setUp(self):
        self.longest_word_of_english = '''
                                Methionylglutaminylarginyltyrosylglutamylserylleucylphenyl-
                                alanylalanylglutaminylleucyllysylglutamylarginyllysylglutamyl-
                                glycylalanylphenylalanylvalylprolylphenylalanylvalylthreonyl-
                                leucylglycylaspartylprolylglycylisoleucylglutamylglutaminyl-
                                serylleucyllysylisoleucylaspartylthreonylleucylisoleucylglutamy-
                                lalanylglycylalanylaspartylalanylleucylglutamylleucylglycylisoleucyl-
                                prolylphenylalanylserylaspartylprolylleucylalanylaspartylglycylproly-
                                lthreonylisoleucylglutaminylaspfraginylalanylthreonylleucylarginy-
                                lalanylphenylalanylalanylalanylglycylvalylthreonylprolylalanyl-
                                glutaminylcysteinylphenylalanylglutamylmethionylleucylalany-
                                lleucylisoleucylarginylglutaminyllysylhistidylprolylthreonylisoleucyl-
                                prolylisoleucylglycylleucylleucylmethionyltyrosylalanylasparaginy-
                                lleucylvalylphenylalanylasparaginyllysylglycylisoleucylaspartyl-
                                glutamylphenylalanyltyrosylalanylglutaminylcysteinylglutamylly-
                                sylvalylglycylvalylaspartylserylvalylleucylvalylalanylaspartylvalyl-
                                prolylvalylglutaminylglutamylserylalanylprolylphenylalanylarginyl-
                                glutaminylalanylalanylleucylarginylhistidylasparaginylvalylalanyl-
                                prolylisoleucylphenylalanylisoleucylcysteinylprolylprolylaspartylalanyl-
                                aspartylaspartylaspartylleucylleucylarginylglutaminylisoleucylalanyl-
                                seryltyrosylglycylarginylglycyltyrosylthreonyltyrosylleucylleucylseryl-
                                arginylalanylglycylvalylthreonylglycylalanylglutamylasparaginyl-
                                arginylalanylalanylleucylprolylleucylasparaginylhistidylleucylvalyl-
                                alanyllysylleucyllysylglutamyltyrosylasparaginylalanylalanylprolyl-
                                prolylleucylglutaminylglycylphenylalanylglycylisoleucylserylalanyl-
                                prolylaspartylglutaminylvalyllysylalanylalanylisoleucylaspartylalanyl-
                                glycylalanylalanylglycylalanylisoleucylserylglycylserylalanylisoleucyl-
                                valyllysylisoleucylisoleucylglutamylglutaminylhistidylasparaginy-
                                lisoleucylglutamylprolylglutamyllysylmethionylleucylalanylalanyl-
                                leucyllysylvalylphenylalanylvalylglutaminylprolylmethionyllysylalanyl-
                                alanylthreonylarginylserine
                                '''

        self.other_long_word = '''
                                Lopadotemachoselachogaleokranioleipsanodrimhypotrimmatosilphioparaomelitokat
                                akechymenokichlepikossyphophattoperisteralektryonoptekephalliokigklopeleiola
                                goio-siraiobaphetraganopterygon
                                '''

    def test_none_words(self):
        with self.assertRaises(ValueError):
            WordService.compute_distance(None, "bola")
            WordService.compute_distance("bola", None)
            WordService.compute_distance(None, None)

    def test_distance_between_equal_words(self):
        result = WordService.compute_distance("bola", "bola")
        self.assertEqual(result, 0)

    def test_distance_between_empty_words(self):
        result = WordService.compute_distance("", "bola")
        self.assertEqual(result, 0)

        result = WordService.compute_distance("", "")
        self.assertEqual(result, 0)

        result = WordService.compute_distance("bola", "")
        self.assertEqual(result, 0)

    def test_distance_between_words(self):
        result = WordService.compute_distance("abacate", "banana")
        self.assertEqual(result, 4)

        result = WordService.compute_distance("kitten", "sitting")
        self.assertEqual(result, 3)

        result = WordService.compute_distance("uva", "ovo")
        self.assertEqual(result, 2)

        result = WordService.compute_distance("paralelepipido", "ovo")
        self.assertEqual(result, 13)

        result = WordService.compute_distance("breach", "search")
        self.assertEqual(result, 3)

        result = WordService.compute_distance(self.longest_word_of_english, self.other_long_word)
        self.assertEqual(result, 2682)

    def test_recursive(self):
        # This test show how recursive version can be unusual, see that for long strings this solution
        # is not usable in practical approach
        with self.assertRaises(RuntimeError):
            WordService.recursive_version(self.longest_word_of_english, self.other_long_word)


class WordTestCase(TestCase):
    def setUp(self):
        Word.objects.create(word="banana")
        Word.objects.create(word="cat")

    def test_names(self):
        w1 = Word.objects.get(word="banana")
        w2 = Word.objects.get(word="cat")
        self.assertEqual(w1.get_word(), 'banana')
        self.assertEqual(w2.get_word(), 'cat')


class WordEndPointTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.auth_header = dict(HTTP_AUTHORIZATION="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjo0"
                                                   "fQ.LvcApqSzzNsBJsUGretNjAHj_a6tpfpOEAE0PJHaH1g")
        Word.objects.create(word="banana")
        Word.objects.create(word="cat")

    def test_list_words(self):
        response = self.client.get('/api/v1/words/', **self.auth_header)

        content = json.loads(response.content)
        words = [dict(word='banana', id=1), dict(word='cat', id=2)]

        list_words = content.get('results')
        self.assertIsNotNone(list_words)
        self.assertNotEqual(len(list_words), 0)
        self.assertEqual(list_words, words)

    def test_create_word(self):
        response = self.client.post(path='/api/v1/words/',
                                    data=json.dumps(dict(word='ball')),
                                    content_type='application/json',
                                    **self.auth_header)

        self.assertEqual(response.status_code, 201)
        obj = Word.objects.get(word='ball')

        self.assertIsNotNone(obj)
        self.assertEqual(obj.get_word(), 'ball')

        # self.assertEqual(json.dumps(content), words)

    def test_calcule_distance(self):
        response = self.client.post(path='/api/v1/words/distance/',
                                    data=json.dumps(dict(word1='abacate', word2='banana')),
                                    content_type='application/json',
                                    **self.auth_header)

        self.assertEqual(response.status_code, 201)

        obj = json.loads(response.content)
        self.assertEqual(obj.get('distance'), 4)
