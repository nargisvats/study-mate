from django.db.models import Avg, Count

from .models import Review


class ReviewService:
    @staticmethod
    def create_review(booking, student, rating, comment=""):
        if booking.status != booking.Status.COMPLETED:
            raise ValueError("Can only review completed sessions.")
        if hasattr(booking, "review"):
            raise ValueError("Review already exists.")
        review = Review.objects.create(
            booking=booking,
            student=student,
            tutor=booking.tutor,
            rating=rating,
            comment=comment,
        )
        ReviewService.update_tutor_rating(booking.tutor)
        from notifications.services import NotificationService
        NotificationService.notify_review_received(review)
        return review

    @staticmethod
    def update_tutor_rating(tutor):
        agg = Review.objects.filter(tutor=tutor).aggregate(avg=Avg("rating"), count=Count("id"))
        tutor.avg_rating = agg["avg"] or 0
        tutor.review_count = agg["count"] or 0
        tutor.save(update_fields=["avg_rating", "review_count"])
