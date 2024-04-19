from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet for handling soft deletes."""

    def delete(self):
        """Soft delete queryset items."""
        return super().update(is_deleted=True, is_active=False)

    def undelete(self):
        """Undelete previously soft-deleted items."""
        return super().update(is_deleted=False, is_active=True)

    def activate(self):
        """Activate queryset items."""
        return super().update(is_active=True)

    def deactivate(self):
        """Deactivate queryset items."""
        return super().update(is_active=False)

    def archive(self):
        """Retrieve all items."""
        return super().all()


class DeleteManager(models.Manager):
    """Manager for handling soft deletes."""

    def get_queryset(self):
        """Get the queryset object associated with this manager."""
        if not hasattr(self.__class__, '__queryset'):
            self.__class__.__queryset = SoftDeleteQuerySet(self.model)
        return self.__queryset

    def delete(self):
        """Soft delete items."""
        return self.get_queryset().delete()

    def undelete(self):
        """Undelete items."""
        return self.get_queryset().undelete()

    def activate(self):
        """Activate items."""
        return self.get_queryset().activate()

    def deactivate(self):
        """Deactivate items."""
        return self.get_queryset().deactivate()

    def archive(self):
        """Retrieve all items."""
        return self.get_queryset().archive()
