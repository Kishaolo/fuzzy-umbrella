from django.db import models
from datetime import datetime

class Operation(models.Model):

    name = models.TextField(
        verbose_name="Naimenovanie operatsii"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Opisanie operatsii"
    )
    cost = models.FloatField(
        verbose_name="stoimost"
    )
    operation_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="data operatsii",
    )
    class Meta:
        verbose_name = "Operatsii"
        verbose_name_plural = "Operatsii"

    def __str__(self):
        return f"At-{self.operation_at}-{self.name}"