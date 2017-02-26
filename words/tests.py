import json

import jwt
from django.contrib.auth.models import User
from django.test import TestCase, Client

from services import WordService, AuthServices
from words.models import Word


# BEARER_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c" \
#                "2VyIjo0fQ.LvcApqSzzNsBJsUGretNjAHj_a6tpfpOEAE0PJHaH1g"


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

        result = WordService.compute_distance("felipe", "neide")
        self.assertEqual(result, 3)

        result = WordService.compute_distance(self.longest_word_of_english, self.other_long_word)
        self.assertEqual(result, 2682)

    def test_recursive(self):
        # This test show how recursive version can be unusual, see that for long strings this solution
        # is not usable in practical approach
        with self.assertRaises(RuntimeError):
            WordService.recursive_version(self.longest_word_of_english, self.other_long_word)

    def test_if_words_are_similars(self):

        is_similar = WordService.is_similar("abacate", "banana")
        self.assertFalse(is_similar, False)

        is_similar = WordService.is_similar("ovo", "uva")
        self.assertTrue(is_similar, True)

        is_similar = WordService.is_similar("ovo", "uva", threshold=1)
        self.assertFalse(is_similar, False)

        is_similar = WordService.is_similar("ovo", "ovo", threshold=0)
        self.assertTrue(is_similar, True)

        is_similar = WordService.is_similar(self.longest_word_of_english, "ovo")
        self.assertFalse(is_similar, False)

        is_similar = WordService.is_similar("abacate", "banana", threshold=4)
        self.assertTrue(is_similar, True)

    def test_filter_words(self):

        Word(word="abacate").save()
        Word(word="banana").save()
        Word(word="bola").save()
        Word(word="carro").save()
        Word(word="melancia").save()
        Word(word="abobora").save()
        Word(word="peixe").save()

        words = WordService.filter_words(keyword='abacate', threshold=4)
        self.assertTrue(len(words))
        self.assertEqual(len(words), 2)

        words = WordService.filter_words(keyword='', threshold=0)
        self.assertEqual(len(words), 7)

        words = WordService.filter_words(keyword='')
        self.assertEqual(len(words), 7)

        words = WordService.filter_words(keyword='peixe', threshold=3)
        self.assertEqual(len(words), 1)

        words = WordService.filter_words(keyword='peixe', threshold=5)
        self.assertEqual(len(words), 3)


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
        user = User.objects.create_user('user_test', 'test@gmail.com', "useruser")
        user.save()

        user = User.objects.get(username='user_test')
        token = AuthServices.verify_user(username=user.username,
                                         email=user.email,
                                         password=user.password)

        self.auth_header = dict(HTTP_AUTHORIZATION="Bearer " + token)
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


class AuthTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user('user_test', 'test@gmail.com', "useruser")
        user.save()

    def test_create_token(self):
        user = User.objects.get(username='user_test')
        token = AuthServices.create_token(user)
        claims = jwt.decode(token, 'secret', algorithms=['HS256'])

        self.assertEqual(claims.get('user_id'), 1)
        with self.assertRaises(jwt.DecodeError):
            jwt.decode(None, 'secret', algorithms=['HS256'])

    def test_decode_token(self):
        result = AuthServices.decode_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1"
                                            "c2VyX2lkIjoxLCJleHAiOjE0ODgxMjQxMzd9.jxpHa1t"
                                            "Dm39naVuvymtk_NtOZhiB9vwhUIS0r-pl_uk")
        # Toke gave was expired
        self.assertEqual(result, False)

    def test_token_manager(self):
        user = User.objects.get(username='user_test')
        token = AuthServices.token_manager(user)

        claims = jwt.decode(token, 'secret', algorithms=['HS256'])

        self.assertEqual(claims.get('user_id'), 1)
        with self.assertRaises(jwt.DecodeError):
            jwt.decode(None, 'secret', algorithms=['HS256'])

    def test_user_verification(self):

        token = AuthServices.verify_user(username='user_test',
                                         email='test@gmail.com',
                                         password='useruser')
        user_id = AuthServices.decode_token(token)
        self.assertEqual(user_id, 1)

        token = AuthServices.verify_user(username='user_test_2',
                                         email='test2@gmail.com',
                                         password='useruser')

        user_id = AuthServices.decode_token(token)
        self.assertEqual(user_id, 2)





