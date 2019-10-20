from django.test import TestCase

# Create your tests here.
from .models import ClozeData, Language, Note, Sentence, Translation

class Helpers():
    def make_ClozeCard(t, ss, se, mc0='', 
                  mc1='', mc2='', mc3='', 
                  a='-111'):
        return ClozeData.objects.create(
                translation  = t,   splice_start = ss,
                splice_end   = se,  mult_choice0 = mc0,
                mult_choice1 = mc1, mult_choice2 = mc2,
                mult_choice3 = mc3, answer = a)

    # does not have note property yet
    def make_Translation(s, l, nt, ipa, am  = None, 
                        af      = None, rom = None, 
                        rom_alt = None, p   = None, 
                        p_alt   = None, z   = None, 
                        zh_alt  = None):
        return Translation.objects.create(
                sentence     = s,   language     = l,
                audio_male   = am,  audio_female = af,
                native_text  = nt,  ipa          = ipa,
                romanization = rom, roman_alt    = rom_alt,
                pinyin       = p,   pinyin_alt   = p_alt,
                zhuyin       = z,   chinese_alt  = zh_alt)

    def make_Language(name: str) -> Language:
        return Language.objects.create(name = name)

    def make_Sentence():
        return Sentence.objects.create()

"""
helpers are (mostly) mutually dependent. Bugs will cascade
these are somewhat redundant considering we test the constructors
of the individual models later on in this file. But redundancy 
isn't bad when testing IMO -- only in functional code
note that these are not substitutes for constructor tests,
as these don't test every property -- only those used in the
helper functions
"""
class HelperTest(TestCase):

    native_text = "你什麼時候能到達？"
    ipa = "arbitrary test value (not IPA)"

    def test_make_Sentence(self):
        s = Helpers.make_Sentence()
        s.save()
        self.assertIsInstance(s, Sentence)
        self.assertEqual(s.id, 1)

    def test_make_ClozeCard(self):
        s = Helpers.make_Sentence()
        l = Helpers.make_Language("Wenzhounese")
        s.save()
        l.save()

        t = Helpers.make_Translation(s, l, self.native_text, self.ipa,
                                    None, None)

        c = Helpers.make_ClozeCard(t, 3, 5)

        self.assertIsInstance(c, ClozeData)
        self.assertEqual(c.id, 1)
        self.assertEqual(c.translation, t)
        self.assertEqual(c.splice_start, 3)
        self.assertEqual(c.splice_end, 5)

    def test_make_Language(self):
        l = Helpers.make_Language("Chinese")
        self.assertIsInstance(l, Language)
        self.assertEqual(l.id, 1)
        self.assertEqual(l.name, "Chinese")

    def test_make_Translation(self):
        # n = Helpers.make_Note(foo, bar, foobar, a, b, c, d)
        s = Helpers.make_Sentence()
        l = Helpers.make_Language("Chinese")
        s.save()
        l.save()
        # note = n

        t = Helpers.make_Translation(s, l, self.native_text, self.ipa,
                                    None, None)

        self.assertIsInstance(t, Translation)
        self.assertEqual(t.id, 1)

# class ClozeDataTest(TestCase):
#     def foo(self):
#         return "foo"

class LanguageTest(TestCase):

    def test_Language_constructor(self):
        s = "Basque"
        l = Helpers.make_Language(s)
        self.assertIsInstance(l, Language)
        self.assertEqual(l.id, 1)
        self.assertEqual(l.name, s)
        l = Helpers.make_Language("Lakota")
        self.assertEqual(l.id, 2)

    def test_Language_underscore_methods(self):
        s = "Basque"
        l = Helpers.make_Language(s)
        self.assertEqual(str(l), s)
        self.assertEqual(l.__str__(), s)
        self.assertEqual(l.__unicode__(), s)

# class NoteTest(TestCase):

class SentenceTest(TestCase):

    def test_Note_constructor(self):
        s = Sentence.objects.create()
        self.assertIsInstance(s, Sentence)
        self.assertEqual(s.id, 1)
        s = Sentence.objects.create()
        self.assertEqual(s.id, 2)

    def test_Note_underscore_methods(self):
        s = Sentence.objects.create()
        self.assertEqual(s.__str__(), "Sentence 1")
        self.assertEqual(s.__unicode__(), "Sentence 1")
        s = Sentence.objects.create()
        self.assertEqual(s.__str__(), "Sentence 2")
        self.assertEqual(s.__unicode__(), "Sentence 2")

# class TranslationTest(TestCase):
#     def foo(self):
#         return "foo"
