from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid
from PIL import Image, ExifTags, ImageOps
from io import BytesIO
import os


class ContactInfo(models.Model):
    last_name = models.CharField(max_length=256)
    first_name = models.CharField(max_length=256)
    home_phone = models.CharField(max_length=256)
    street1 = models.CharField(max_length=256)
    street2 = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    zip = models.CharField(max_length=256)
    country = models.CharField(max_length=256)


class Donor(models.Model):
    contactinfo = models.ForeignKey(ContactInfo, models.CASCADE)


class Contributor(models.Model): # maybe should be a group? (for users)
    contactinfo = models.ForeignKey(ContactInfo, models.CASCADE)


class Collection(models.Model):
    name = models.CharField(max_length=512)
    donors = models.ManyToManyField(Donor) # maybe should be a field of Photo?
    displayed_donors = models.CharField(max_length=512)
    description = models.TextField()
    year_min = models.SmallIntegerField(
        "oldest photo year", editable=False, null=True
    )
    year_max = models.SmallIntegerField(
        "newest photo year", editable=False, null=True
    )
    total_photos = models.SmallIntegerField("photos", editable=False, default=0)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Term(models.Model):
    term = models.CharField(max_length=64)

    def __str__(self):
        return self.term


class Tag(models.Model):
    tag = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self):
        if not self.slug:
            self.slug = slugify(self.tag)
        super().save()

    def __str__(self):
        return self.tag



class Photo(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    original = models.ImageField(null=True)
    h700 = models.ImageField(null=True)
    thumbnail = models.ImageField(null=True)
    collection = models.ForeignKey(Collection, models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True, through="PhotoTag")
    def get_accepted_tags(self):
        return self.tags.filter(phototag__accepted=True)
    def get_proposed_tags(self):
        return self.tags.filter(phototag__accepted=False)
    terms = models.ManyToManyField(Term, blank=True)
    city = models.CharField(max_length=128)
    county = models.CharField(max_length=128)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64, null=True)
    year = models.SmallIntegerField(null=True)
    caption = models.TextField()
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Contributor, null=True, on_delete=models.SET_NULL, blank=True
    )
    def __str__(self):
        return self.accession_number

    @staticmethod
    def accession2id(accession):
        if not accession.startswith('FI'):
            raise ValueError("{} doesn't start with FI", accession)
        return int(accession[2:])


    @property
    def accession_number(self):
        return 'FI' + str(self.id).zfill(7)

    def save(self, *args, **kwargs):
        image = ImageOps.exif_transpose(Image.open(BytesIO(self.original.read())))
        #try: for orientation in ExifTags.TAGS.keys():
        #        if ExifTags.TAGS[orientation]=='Orientation':
        #            break
        #    exif=dict(image._getexif().items())

        #    if exif[orientation] == 3:
        #        image=image.rotate(180, expand=True)
        #    elif exif[orientation] == 6:
        #        image=image.rotate(270, expand=True)
        #    elif exif[orientation] == 8:
        #        image=image.rotate(90, expand=True)
        #except (ArributeError, KeyError, IndexError):
        #    pass
        dims = ((75, 75), (None, 700))
        results = []
        w,h = image.size
        xoff = yoff = 0
        size = min(w, h)
        for dim in dims:
            if any(dim):
                img = image
                if all(dim):
                    if w > h:
                        xoff = round((w-h)/2)
                    elif h > w:
                        yoff = round((h-w)/4)
                    img = img.crop((xoff, yoff, xoff+size, yoff+size))
                if dim[0] and not dim[1]:
                    dim = (dim[0], round(h/w*dim[0]))
                elif dim[1] and not dim[0]:
                    dim = (round(w/h*dim[1]), dim[1])
                img = img.resize(dim, Image.ANTIALIAS)
                results.append(img)
        thumb, h700 = results
        fname = 'thumb/{}.jpg'.format(self.uuid)
        thumb.save(os.path.join(settings.MEDIA_ROOT, fname), "JPEG")
        self.thumbnail.name = fname
        fname = 'h700/{}.jpg'.format(self.uuid)
        h700.save(os.path.join(settings.MEDIA_ROOT, fname), "JPEG")
        self.h700.name = fname
        super().save(*args, **kwargs)



   # def thumb(self):
   #     return "{}/archive/thumbs/{}_75x75.jpg".format(
   #         settings.STATIC_URL, self.accession_number
   #     )

   # def h700(self):
   #     return "{}/archive/h700/{}_x700.jpg".format(
   #         settings.STATIC_URL, self.accession_number
   #     )

   # def original(self):
   #     return "{}/archive/originals/{}.jpg".format(
   #         settings.STATIC_URL, self.accession_number
   #     )

    def location(self):
        result = "Location: n/a"
        if self.city:
            result = "{}, {}".format(self.city, self.state)
        elif self.county:
            result = "{} County, {}".format(self.county, self.state)
        elif self.country:
            result = self.country
        return result


class PhotoTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    accepted = models.BooleanField()


class PrePublishPhoto(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)


class ScannedPhoto(models.Model):
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/') # callable that incorporates donor name?
    collection = models.ForeignKey(Collection, models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        Contributor, null=True, on_delete=models.SET_NULL
    )
    accepted = models.BooleanField(null=True)


class PhotoVote(models.Model):
    photo = models.ForeignKey(ScannedPhoto, on_delete=models.CASCADE, related_name='votes', related_query_name='vote')
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    infavor = models.BooleanField()


class CSVRecord(models.Model):
    filename = models.TextField() #unique=True)
    # unique constraint seems to make sense to me, but there are quite a few
    # duplicate records. should both be added? Or should we take newer added to
    # archive date to be the true record? Or should this be resolved on a case
    # by case basis?
    donorFirstName = models.TextField()
    donorLastName = models.TextField()
    year = models.IntegerField()
    circa = models.BooleanField()
    scanner = models.TextField()
    photographer = models.TextField()
    address = models.TextField()
    city = models.TextField()
    county = models.TextField()
    state = models.TextField()
    country = models.TextField()
    comments = models.TextField()
    added_to_archive = models.DateField()
    photo = models.OneToOneField(Photo, on_delete=models.SET_NULL, null=True)
