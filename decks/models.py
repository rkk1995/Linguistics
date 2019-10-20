from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ClozeData(models.Model):
    
    translation  = models.ForeignKey('Translation', on_delete=models.PROTECT)
    splice_start = models.SmallIntegerField(blank=False)
    splice_end   = models.SmallIntegerField(blank=False)

    mult_choice0 = models.TextField()
    mult_choice1 = models.TextField()
    mult_choice2 = models.TextField()
    mult_choice3 = models.TextField()

    answer = models.SmallIntegerField()

    def save(self, *args, **kwargs):
        if not self.mult_choice0:
            print("\n\nERROR: Must have at least 2 answer choices\n")
        elif not self.mult_choice1:
            print("\n\nERROR: Must have at least 2 answer choices\n")
        elif not self.mult_choice2:
            self.mult_choice2 = self.mult_choice3 = "NO DATA"
        elif not self.mult_choice3:
            self.mult_choice3 = "NO DATA"
        if self.answer == '-111':
            print("ERROR: No answer key given ")
        super(ClozeData, self).save(*args, **kwargs)

    def __str__(self):
        return "splice: (%i,%i)" % (splice_start, splice_end)
    
    def __unicode__(self):
        return self.__str__()

class Language(models.Model):

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Note(models.Model):

    note        = models.TextField()
    sentence    = models.ForeignKey('Sentence', on_delete=models.PROTECT)
    # translation = models.OneToOneField('Translation', on_delete=models.PROTECT)

    def __str__(self):
        return self.note

    def __unicode__(self):
        return self.note

    class Meta:
        ordering = ['id']

class Sentence(models.Model):

    def __str__(self):
        return "Sentence %i" % self.id

    def __unicode__(self):
        return self.__str__()

    class Meta:
        ordering = ['id']

# consider having flag for chinese and abstracting the
# chinese language fields (pinyin, zhuyin) to separate table
# to save a crapload of space (particularly important as we build
# thousands of entries in the database)
class Translation(models.Model):

    sentence     = models.ForeignKey(Sentence, on_delete=models.PROTECT)
    language     = models.ForeignKey(Language, on_delete=models.PROTECT)
    audio_male   = models.BinaryField(blank=True, null=True)
    audio_female = models.BinaryField(blank=True, null=True)
    native_text  = models.TextField(blank=False)
    ipa          = models.TextField(blank=False)
    romanization = models.TextField(blank=True, null=True)
    roman_alt    = models.TextField(blank=True, null=True)
    pinyin       = models.TextField(blank=True, null=True)
    pinyin_alt   = models.TextField(blank=True, null=True)
    zhuyin       = models.TextField(blank=True, null=True)
    chinese_alt  = models.TextField(blank=True, null=True)
    # note         = models.OneToOneField(Note, on_delete=models.CASCADE)



