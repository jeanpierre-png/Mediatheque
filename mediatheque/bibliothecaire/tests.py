from django.test import TestCase
from bibliothecaire.models import Media, Member, Loan


class MediaTest(TestCase):
    def test_create_media(self):
        media = Media.objects.create(
            title="Test title",
            media_type="books"
        )

        self.assertEqual(Media.objects.count(), 1)
        self.assertEqual(media.title, "Test title")
        self.assertEqual(media.media_type, "books")


class MediaListTest(TestCase):
    def test_change_media_type(self):
        media = Media.objects.create(
            title="Test title 2",
            media_type="game"
        )

        media.media_type = "dvds"
        media.save()

        self.assertFalse(media.consultation_only)


class MemberTest(TestCase):
    def test_create_member(self):
        member = Member.objects.create(
            firstname="J-P",
            lastname="NOZA",
            email="jpnoza@hotmail.com"
        )

        self.assertEqual(str(member), "J-P NOZA")


class LoanTest(TestCase):
    def test_create_loan(self):
        member = Member.objects.create(
            firstname="Jean",
            lastname="NOZA",
            email="jeannoza@hotmail.fr"
        )

        media = Media.objects.create(
            title="Test title 3",
            media_type="cds"
        )

        loan = Loan.objects.create(
            member=member,
            media=media
        )

        self.assertIsNone(loan.return_date)


class MediaBusinessRulesTest(TestCase):
    def test_game_is_not_consultation_only(self):
        game = Media.objects.create(
            title="test title 4",
            media_type="game"
        )

        self.assertTrue(game.consultation_only)
        self.assertTrue(game.available)