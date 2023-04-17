from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Asmenys(models.Model):
    user_name = models.CharField('Vardas', max_length=80, blank=False, help_text='Įveskite savo Vardą')
    user_surname = models.CharField('Pavardė', max_length=80, blank=False, help_text='Įveskite savo Pavardę')
    user_birth_date = models.DateField('Gimimo data', blank=False, help_text='Įveskite savo gimimo datą')
    user_age = models.PositiveIntegerField('Amžius', null=True, blank=True, editable=False)

    def calculate_age(self):
        today = date.today()
        age = today.year - self.user_birth_date.year - \
              ((today.month, today.day) < (self.user_birth_date.month, self.user_birth_date.day))
        return max(age, 10)

    def save(self, *args, **kwargs):
        age = self.calculate_age()
        if age <= 10:
            raise ValidationError("Age must be greater than 10.")
        self.user_age = age
        super(Asmenys, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_name}, {self.user_surname}, {self.user_birth_date}, {self.user_age}'

