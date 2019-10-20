from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Category
from .models import Comment
from .models import Post

class CategoryTest(TestCase):

    def test_constructor(self):
        c = Category.objects.create(name="Vocabulary")
        self.assertIsInstance(c, Category)
        self.assertEqual(c.name, "Vocabulary")
        self.assertEqual(c.id, 1)
        c = Category.objects.create(name="Hacks")
        self.assertIsInstance(c, Category)
        self.assertEqual(c.name, "Hacks")
        self.assertEqual(c.id, 2)
    
    def test_underscore_methods(self):
        c = Category.objects.create(name="Vocabulary")
        self.assertEqual(str(c), "Vocabulary")
        self.assertEqual(c.__str__(), "Vocabulary")
        self.assertEqual(c.__unicode__(), "Vocabulary")

        c = Category.objects.create(name="愛❤️牛🐂")
        self.assertEqual(c.__str__(), "愛❤️牛🐂")
        self.assertEqual(str(c), "愛❤️牛🐂")

class CommentTest(TestCase):

    def test_comment(self):
        u = User.objects.create(username="testUser")
        t = "“中文評論呀！”"
        p = Post.objects.create(
                title = "test", article_text = "test body", 
                author = u)
        c = Comment(user = u,text = t,post = p)
        c.save()

        self.assertIsInstance(c, Comment)

        """
        This implicitly tests post assignment,
        PK generation, comment text assignment,
        and user assignment. Explicitly tests
        __str__() and __unicode__()
        """
        answer = "test: 1\t“中文評論呀！”\ttestUser"
        self.assertEqual(c.__str__(), answer)
        self.assertEqual(c.__unicode__(), answer)

        # DEBUG
        print('\n%s\n' % c.__str__())

# still need test ordering by date descending from class Meta
# still need test asserting that text_preview is not altered if not empty string
#   i.e.) author manually input a text preview for SEO, copywriting, etc.
class PostTest(TestCase):

    # setup
    def create_post(self, title="only a test", article_text="This is a test body"):
        author = User.objects.create(username='testauthor')
        p = Post.objects.create(
                title = title, article_text = article_text, 
                author = author)
        p.save()
        c1 = p.categories.create(name="Chinese")
        c2 = p.categories.create(name="Vocabulary")
        p.categories.add(c1)
        p.categories.add(c2)
        p.save()
        return p

    def test_post_constructor(self):
        p = self.create_post()
        self.assertIsInstance(p, Post)
        self.assertIsInstance(p.categories.get(id=1), Category)
        self.assertIsInstance(p.categories.get(id=2), Category)

        self.assertEqual(p.__str__(), p.title)
        self.assertEqual(p.__unicode__(), p.title)
        self.assertEqual(p.article_text, "This is a test body")
        self.assertEqual(p.author.username, "testauthor")

    def test_auto_slug(self):
        p = self.create_post()
        self.assertEqual(p.slug, "only-a-test")

    # test that no chars are cut off and adds \" at start and end
    def test_preview_lt_150(self):
        len_149_str = '6MgzokCcVEqz0A7vb992dTES4sqwcjsRHzYf9qhqi4IrgAvExmmCshRlZ2YG4E4RNelhDMM9R00BNcUM6jHWlSmWuOGlLauUgzypze4lgo3xI3OIStL77zuJbHaMiRkzpi0PQYupqOJNzXZ1OWJWX'
        p = self.create_post(article_text=len_149_str)
        self.assertEqual(p.text_preview, '\"6MgzokCcVEqz0A7vb992dTES4sqwcjsRHzYf9qhqi4IrgAvExmmCshRlZ2YG4E4RNelhDMM9R00BNcUM6jHWlSmWuOGlLauUgzypze4lgo3xI3OIStL77zuJbHaMiRkzpi0PQYupqOJNzXZ1OWJWX\"')

    # test that char 150 remains and adds \" at start and end
    def test_preview_eq_150(self):
        len_150_str = 'EwdFIvavEpvwsui7AXuiC0iTRgN9KDcot1RmqbtKVVLiJgdISv4hCdyTuaArYjMXgJNfXVzCEXiXv4oRafUUSNu3vDi5L33laIDKKj6tIEj4Y6tf2Zy9FYKlZFn7P4YbIVNTNQUomIduOIX00RYslo'
        p = self.create_post(article_text=len_150_str)
        self.assertEqual(p.text_preview, '\"EwdFIvavEpvwsui7AXuiC0iTRgN9KDcot1RmqbtKVVLiJgdISv4hCdyTuaArYjMXgJNfXVzCEXiXv4oRafUUSNu3vDi5L33laIDKKj6tIEj4Y6tf2Zy9FYKlZFn7P4YbIVNTNQUomIduOIX00RYslo\"')

    # test that it cuts off at char 150 and adds "..." as well as \" at start and end
    def test_preview_gt_150(self):
        len_151_str = 'f7iPRsKS7BHpTch6xjJ7EVTKl1of17EvED3jdLejQSNQbx4qD5x5BvkZgdOmreXjWtHHHpeMc5XmN2J60INsXx4pDIXlPyG3JsN6xbOv5YlykwHB57SX0NpCBJmpTVqANlVsRPfRMVtWVKA7QePHpsu'
        p = self.create_post(article_text=len_151_str)
        self.assertEqual(p.text_preview, '\"f7iPRsKS7BHpTch6xjJ7EVTKl1of17EvED3jdLejQSNQbx4qD5x5BvkZgdOmreXjWtHHHpeMc5XmN2J60INsXx4pDIXlPyG3JsN6xbOv5YlykwHB57SX0NpCBJmpTVqANlVsRPfRMVtWVKA7QePHps...\"')
