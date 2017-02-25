from django.test import TestCase
from services import WordService


class WordServiceTest(TestCase):

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



