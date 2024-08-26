import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Member(BaseModel):
    fullname = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class Relationship(BaseModel):
    PARENT = "PARENT"
    CHILD = "CHILD"
    SPOUSE = "SPOUSE"
    RELATIONSHIP_CHOICES = [
        (PARENT, "Parent"),
        (CHILD, "Child"),
        (SPOUSE, "Spouse"),
    ]

    member_from = models.ForeignKey(
        Member, related_name="relationships_from", on_delete=models.CASCADE
    )
    member_to = models.ForeignKey(
        Member, related_name="relationships_to", on_delete=models.CASCADE
    )
    relation = models.CharField(max_length=6, choices=RELATIONSHIP_CHOICES)

    def __str__(self):
        return f"{self.member_from} - {self.relation} - {self.member_to}"
