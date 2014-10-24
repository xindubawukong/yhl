# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class UserInfo(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100, default='')
    MALE = '男'
    FEMALE = '女'
    GENDER_CHOICES = (
        (MALE, '男'),
        (FEMALE, '女')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='')
    EE = '电子工程系'
    CS = '计算机科学与技术系'
    MISSING = ''
    DEP_CHOICES = (
        (MISSING, ''),
        (EE, '电子工程系'),
        (CS, '计算机科学与技术系'),
    )
    department = models.CharField(max_length=10, choices=DEP_CHOICES, default=MISSING)
    studentClass = models.CharField(max_length=6, default='')
    birth = models.DateField(null=True)
    QUNZHONG = '群众'
    TUANYUAN = '共青团员'
    JIJIFENZI = '积极分子'
    YUBEIDANGYUAN = '预备党员'
    DANGYUAN = '党员'
    PB_CHOICES = (
        (MISSING, ''),
        (QUNZHONG, '群众'),
        (TUANYUAN, '共青 团员'),
        (JIJIFENZI, '积极分子'),
        (YUBEIDANGYUAN, '预备党员'),
        (DANGYUAN, '党员'),
    )
    politicalBackground = models.CharField(max_length=4, choices=PB_CHOICES, default=MISSING)
    GPA_Rank = models.CharField(max_length=100, default='')  #json
    phoneNum = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=50, default='')
    work = models.CharField(max_length=200, default='')  #json

    @staticmethod
    def fields():
        return set(BasicInfo._meta.get_all_field_names()).difference({'user', 'user_id', 'id'})


 
