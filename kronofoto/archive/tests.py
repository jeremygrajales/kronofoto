from django.test import TestCase, SimpleTestCase
from . import models
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlencode

class WhenHave50Photos(TestCase):
    @classmethod
    def setUpTestData(cls):
        coll = models.Collection.objects.create(name='test collection')
        cls.photos = []
        for y in range(1900, 1950):
            p = models.Photo.objects.create(
                original=SimpleUploadedFile(
                    name='test_img.jpg',
                    content=open('testdata/test.jpg', 'rb').read(),
                    content_type='image/jpeg'),
                collection=coll,
                year=y,
                is_published=True,
            )
            cls.photos.append(p)


    def testShouldNotAllowGuestsToTagPhotos(self):
        resp = self.client.get(reverse('addtag', kwargs={'photo': self.photos[0].accession_number}))
        self.assertEqual(resp.status_code, 302)

        resp = self.client.post(reverse('addtag', kwargs={'photo': self.photos[0].accession_number}), { 'tag': 'test tag'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(self.photos[0].get_proposed_tags()), 0)
        self.assertEqual(len(self.photos[0].get_accepted_tags()), 0)


    def testShouldBeAbleToTagPhotos(self):
        User.objects.create_user('testuser', 'user@email.com', 'testpassword')
        self.client.login(username='testuser', password='testpassword')
        resp = self.client.get(reverse('addtag', kwargs={'photo': self.photos[0].accession_number}))
        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(reverse('addtag', kwargs={'photo': self.photos[0].accession_number}), { 'tag': 'test tag'})
        self.assertEqual(len(self.photos[0].get_proposed_tags()), 1)
        self.assertEqual(self.photos[0].get_proposed_tags()[0].tag, 'test tag')
        self.assertEqual(len(self.photos[0].get_accepted_tags()), 0)


    def testShould404WhenPhotoNotFound(self):
        resp = self.client.get(reverse('photoview', kwargs={'page': 1, 'photo': 'FI99999'}))
        self.assertEqual(resp.status_code, 404)

    def testShouldRedirectToCorrectPageForPhoto(self):
        photos = self.photos
        for page in range(1, 6):
            thispage = photos[:10]
            photos = photos[10:]
            for photo in thispage:
                resp = self.client.get(reverse('photoview', kwargs={'page': page % 5 + 1, 'photo':photo.accession_number}))
                self.assertRedirects(resp, reverse('photoview', kwargs={'page': page, 'photo':photo.accession_number}))

    def testGridViewShouldDisplayAllPhotosInOrder(self):
        photo_ids = {photo.id for photo in self.photos}
        currentpage = 1
        last = None
        while True:
            resp = self.client.get(reverse('gridview', kwargs={'page': currentpage}), {'display': 16})
            for photo in resp.context['page_obj']:
                self.assertIn(photo.id, photo_ids)
                if last:
                    self.assertTrue(last.year < photo.year)
                last = photo

                photo_ids.remove(photo.id)
            currentpage += 1
            if not resp.context['page_obj'].has_next():
                break
        self.assertEqual(len(photo_ids), 0)


    def testGridViewShouldHaveNavigationButtons(self):
        pages = ["{}?{}".format(reverse('gridview', kwargs={'page': page}), urlencode({'display': 16})) for page in [1,2,3,4]]
        resp = self.client.get(pages[0])
        self.assertInHTML('<div id="navigation">First Previous <a href="{}">Next</a> <a href="{}">Last</a></div>'.format(pages[1], pages[-1]), resp.content.decode('utf-8'))
        resp = self.client.get(pages[1])
        self.assertInHTML('<div id="navigation"><a href="{}">First</a> <a href="{}">Previous</a> <a href="{}">Next</a> <a href="{}">Last</a></div>'.format(pages[0], pages[0], pages[2], pages[-1]), resp.content.decode('utf-8'))
        resp = self.client.get(pages[2])
        self.assertInHTML('<div id="navigation"><a href="{}">First</a> <a href="{}">Previous</a> <a href="{}">Next</a> <a href="{}">Last</a></div>'.format(pages[0], pages[1], pages[3], pages[-1]), resp.content.decode('utf-8'))
        resp = self.client.get(pages[3])
        self.assertInHTML('<div id="navigation"><a href="{}">First</a> <a href="{}">Previous</a> Next Last'.format(pages[0], pages[2]), resp.content.decode('utf-8'))


    def testGridShouldRespectTermFilters(self):
        term = models.Term.objects.create(term="test term")
        photos = [self.photos[2], self.photos[5], self.photos[15]]
        for photo in photos:
            photo.terms.add(term)
        resp = self.client.get(reverse('gridview', kwargs={'page': 1}), {'term': term.slug})
        self.assertEqual(len(resp.context['page_obj']), len(photos))
        our_ids = {photo.id for photo in photos}
        got_ids = {photo.id for photo in resp.context['page_obj']}
        self.assertEqual(our_ids, got_ids)


    def testGridShouldRespectTagFilters(self):
        tag = models.Tag.objects.create(tag="test tag")
        photos = [self.photos[2], self.photos[5], self.photos[15]]
        for photo in photos:
            models.PhotoTag.objects.create(tag=tag, photo=photo, accepted=True)
        resp = self.client.get(reverse('gridview', kwargs={'page': 1}), {'tag': tag.slug})
        self.assertEqual(len(resp.context['page_obj']), len(photos))
        our_ids = {photo.id for photo in photos}
        got_ids = {photo.id for photo in resp.context['page_obj']}
        self.assertEqual(our_ids, got_ids)

    def testFilteringShouldNotShowUnapprovedTags(self):
        tag = models.Tag.objects.create(tag="test tag")
        photos = [self.photos[2], self.photos[5], self.photos[15]]
        for photo in photos:
            models.PhotoTag.objects.create(tag=tag, photo=photo, accepted=False)
        resp = self.client.get(reverse('gridview', kwargs={'page': 1}), {'tag': tag.slug})
        self.assertEqual(len(resp.context['page_obj']), 0)


    def testGridViewShouldHonorDisplayParameter(self):
        for disp in range(15, 24):
            resp = self.client.get(reverse('gridview', kwargs={'page': 1}), {'display': disp})
            self.assertEqual(len(resp.context['page_obj']), disp)

    def testGridViewShouldDisplayPhotoCount(self):
        currentpage = 1
        while True:
            resp = self.client.get(reverse('gridview', kwargs={'page': currentpage}), {'display': 16})
            self.assertInHTML('<div id="position">Items {} - {} of {}</div>'.format((currentpage-1)*16+1, min(50, currentpage*16), 50), resp.content.decode('utf-8'))
            currentpage += 1
            if not resp.context['page_obj'].has_next():
                break


from archive.templatetags import timeline
class TimelineDisplay(SimpleTestCase):
    def testShouldDefineMinorMarkerPositions(self):
        years = [(year, '/{}'.format(year)) for year in [1900, 1901, 1902, 1903, 1904, 1905]]
        result = timeline.make_timeline(years, width=60)
        self.assertEqual(result['majornotches'], [{
            'target': '/1900',
            'box': {
                'x': 0,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 0,
                'y': 5,
                'width': 2,
                'height': 5,
            },
            'label': {
                'text': '1900',
                'x': 5,
                'y': 3
            }
        },
        {
            'target': '/1905',
            'box': {
                'x': 50,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 50,
                'y': 5,
                'width': 2,
                'height': 5,
            },
            'label': {
                'text': '1905',
                'x': 55,
                'y': 3
            }
        },
        ])
        self.assertEqual(result['minornotches'], [{
            'target': '/1901',
            'box': {
                'x': 10,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 10,
                'y': 7,
                'width': 2,
                'height': 3,
            }
        },
        {
            'target': '/1902',
            'box': {
                'x': 20,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 20,
                'y': 7,
                'width': 2,
                'height': 3,
            }
        },
        {
            'target': '/1903',
            'box': {
                'x': 30,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 30,
                'y': 7,
                'width': 2,
                'height': 3,
            }
        },
        {
            'target': '/1904',
            'box': {
                'x': 40,
                'y': 5,
                'width': 10,
                'height': 5,
            },
            'notch': {
                'x': 40,
                'y': 7,
                'width': 2,
                'height': 3,
            }
        },
        ])
