# Education site (Full Admin panel control)
- [Education site](#education-site)
- [Project Title](#project-title)
- [Description](#description)
    - [Azərbaycanca](#az)
    - [English](#en)

<hr>

- İnstallation/Quraşdırılma
- [Azərbaycanca quraşdırılma](#azərbaycanca-quraşdırılma)
- [İnstallation English](#installation-in-english)
- [Author](#author)
- [Version](#version)
___



<hr>

# Project Title
___
* <b>Education site</b>
___

# Description

## AZ
___
* <b>Skript FastAPİ ilə qurulub.</b>
* <b>Admin Paneldən saytın hər bir detalı rəhbərlik tərəfindən idarə olunur</b>
* <b>Admin Paneldə 3 dil seçimi mövcuddur.(AZ,RU,EN)</b>

![alt text](/docs/languages.png)

* <b> Admin Panelin 2 modu var(Dark/Light)</b>
![alt text](/docs/dark.png) ![alt text](/docs/light.png)
<hr>
* <b> Istifadəçilər</b><br/>
Admin Paneldə, yuxarı hissədə istifadəçilərin statistikası mövcuddur. Günlük, aylıq, həftəlik və ümumi.
![alt text](/docs/registers.png)

Bundan əlavə, istifadəçi profillərini tam idarə etmək(bütün məlumatlarını dəyişdirmək, istifadəçinin sayta daxil olmağını Aktiv/Deaktiv etmək, istifadəçini ADMİN etmək də olur.)
Saytda 3 istifadəçi tipi var, Super İstifadəçi(scripti install edəndə yaranan ilk istifadəçi, super istifadəçi olur). Super istifadəçi və Admin bərabər hüquqludur, lakin Super istifadəçinin adminliyi alındıqda belə yenə də Adminin edə biləcəyi hərşeyi edə bilir. Hər hansı bir adminin vəzifəsi alındıqda isə adi istifadəçi kimi fəaliyyət göstərir.
Adi istifadəçilər isə yalnız saytın daxilində yalnız öz profilləri ilə bağlı əməliyyat edə bilirlər.
'Adminlər' bölümündən Admin istifadəçilərə nəzarət edə bilər və dəyişikliklərinizi edə bilərsiniz.
<hr>
* <b> Slaydlar</b><br/>
Admin paneldən saytın slaydlarını və slaydın xəbərini Əlavə etmək/Yeniləmək/Silmək olur. Maksimum 4 slayd əlavə etməyə icazə verilir. İcazəni html template-də limitləmişəm, istəyən artırıb azalda bilər. Sadəcə slayd şəkillərinin ölçüsü böyük olduğundan saytı çox yükləməmək baxımından belə bir tədbir görülüb.
Admin panel:

![alt text](/docs/add_slide.png)
![alt text](/docs/slides.png)
Sayt:

![alt text](/docs/slide_in_site.png)
![alt text](/docs/slide_news.png)

<hr>

* <b> Sayt Parametrləri</b><br/>
Buradan sayt daxili çox parametri idarə edə bilərsiniz. Məsələn
Saytın əsas dilini dəyişmək
Saytın başlığı, Logosu(yazı ilə), Sloqanı, Əlaqə nömrəsi, Email, Whatsapp nömrəsi, Whatsapp(saytdan sizə Whatsapp ilə göndəriləcək qısa mətn), Google map link, Adres, Saytın təsviri, Sayt haqqında səhifəsinin məlumatları, Personal haqqında, Youtube Video Tutorial, İş saatları, Saytı aktiv/deaktiv etmək

![alt text](/docs/site.jpg)
![alt text](/docs/about.png)
![alt text](/docs/schedules.png)
![alt text](/docs/contact.png)

Saytı deaktiv etdikdə

![alt text](/docs/deactive_site.png)

<hr>

* <b> Təhsil Parametrləri</b><br/>
Admin paneldən sayta təhsil parametrləri əlavə etmək olur.
Təhsil kateqoriyası, (Universitet, İmtahan və s.).
İstifadəçilər Təhsil parametrinə Foreignkey ilə bağlıdır. Qeydiyyatdan keçən zaman təhsil parametri seçməlidirlər.

Admin panel:
![alt text](/docs/education.png)

<hr>

* <b> Xəbər Parametrləri</b><br/>
Xəbər kateqoriyası və xəbər əlavə edə bilərsiniz. Saytla bağlı və digər xəbərlər

<hr>

* <b> Dil Parametrləri</b><br/>
Admin panelin 3 dili var, lakin sayt üçün daha çox dil əlavə edə bilərsiniz. Sayt üçün 3 dil(AZ,RU,EN) paketləri install etmək olur. Lakin 'Başqa dil əlavə et' seçimi ilə siz istədiyiniz dili də bazaya əlavə edə bilərsiniz. İstəmədiyiniz dili silə bilərsiniz(əgər həmin dil sayt parametrlərindən saytın əsas dili kimi qeyd olunmayıbsa).

Admin panel
![alt text](/docs/site_languages.png)

Sayt
![alt text](/docs/site_languages_top.png)

İstifadəçilər özləri üçün istədiyi dil seçimi edə bilər. Databazada bir Column onlar üçün bunu tənzimləyir, əgər saytda qonaq kimisinizsə, bu zaman dil seçimi kukilərə əlavə olunur və yenə də istədiyin dil seçimini edə bilirsən.

<hr>

* <b> Personal Parametrləri</b><br/>
Personalınızı əlavə edə bilərsiniz(Ad/Soyad, Vəzifə və hər hansı sosial şəbəkəsi varsa)

Sayt
![alt text](/docs/staff.png)

<hr>

* <b> Rəhbərliyə məktub</b><br/>
Qeydiyyatlı istifadəçi yazdıqda onun adından bir başa məktub gedir.
![alt text](/docs/message_1.png)
Qonaqlar yazdıqda isə mütləq bütün xanaları doldurmalıdır.
![alt text](/docs/message_2.png)
Spamın qarşısı alınıb. Məktublar arasında bir neçə saniyə interval olmalıdır.
![alt text](/docs/spam.png)
Admin panel:

Bildirişlər
![alt text](/docs/notifications.png)
![alt text](/docs/messages.png)
İstifadəçi tərəfindən

![alt text](/docs/from_user.png)
Qonaq tərəfindən

![alt text](/docs/from_guest.png)


<hr>

* <b> İstifadəçi</b><br/>
Sayt

![alt text](/docs/profile.png)

İstifadəçilər 4 ədəd təhsillə bağlı fayl yükləyə bilər(JPG,JPEG,PNG).
![alt text](/docs/edu_files.png)
Bu fayllar Admin Paneldə istifadəçinin profilində də görünür. Sayt Rəhbərliyinə lazım olacaq skan olunmuş sənədlər üçün nəzərdə tutulub.

Admin panel

![alt text](/docs/user_docs.png)


<hr>

* <b> Sayt barədə ümumi məlumatlar</b><br/>
Sayta Admin Paneldən nələrsə əlavə etmədikdə sayt ağ səhifədən ibarət olur. Siz əlavə etdikcə saytın seksiyaları görünən olur.
Saytda mövcud olan funksiyalar:
Qeydiyyat
Login
Parol bərpası
Rəhbərliyə məktub
İstifadəçinin profilinə baxış(yalnız adminlər bütün profillərə baxa və düzəliş edə bilir, hər istifadəçi yalnız öz profilinə baxa və düzəliş edə bilər)
İstifadəçinin sənədlərini yükləməyi, profil şəkli əlavə etmək.


____

## EN
___
* <b>The script is built with FastAPI.</b>
* <b>Every detail of the site is controlled by the administration from the Dashboard</b>
* <b>There are 3 language options available in the Dashboard.(AZ,RU,EN)</b>

![alt text](/docs/languages.png)

* <b>Dashboard has 2 modes(Dark/Light)</b>
![alt text](/docs/dark.png) ![alt text](/docs/light.png)
<hr>
* <b> Users</b><br/>
In the upper part, the statistics of users are available. Daily, monthly, weekly and total.
![alt text](/docs/registers.png)

In addition, it is possible to fully manage user profiles (change all information, enable/disable the user's access to the site, make the user ADMIN.)
There are 3 types of users on the site, Super User (the first person created when installing the script is the super user). Superuser and Admin have rights, but even if the Super person's admin is removed, they can do everything that Admin can do. Even if the administrator is canceled, all functions work.
Users can only perform transactions related to their profiles within the site.
Admin management can be controlled and modified from the 'Admins' section.
<hr>
* <b> Slides</b><br/>
You can add/update/delete site slides and slide news from the admin panel. You are allowed to add a maximum of 4 slides. I have restricted the permissions in the html template, anyone can increase or decrease it. Just because the size of the slide images is large, such a measure has been taken so that the site does not load too much.
Dashboard:

![alt text](/docs/add_slide.png)
![alt text](/docs/slides.png)
Sayt:

![alt text](/docs/slide_in_site.png)
![alt text](/docs/slide_news.png)

<hr>

* <b> Site Settings</b><br/>
From here you can manage many settings within the site. for example
Change the main language of the site
Site title, Logo (in writing), Slogan, Contact number, Email, Whatsapp number, Whatsapp (a short text that will be sent to you via Whatsapp from the site), Google map link, Address, Site description, About site information, About staff, Youtube Video Tutorial , Opening hours, Activate/deactivate the site

![alt text](/docs/site.jpg)
![alt text](/docs/about.png)
![alt text](/docs/schedules.png)
![alt text](/docs/contact.png)

When you deactivate the site

![alt text](/docs/deactive_site.png)

<hr>

* <b> Educational Settings</b><br/>
You can add educational settings to the site from the admin panel.
Education category, (University, Exam, etc.).
Users are bound by Foreignkey to the Education setting. They must select a study setting when registering.

Dashboard:
![alt text](/docs/education.png)

<hr>

* <b> News Settings</b><br/>
You can add news information and news. Site related and other news

<hr>

* <b> Language Settings</b><br/>
Dasboard has 3 languages, but you can add more languages for the site. 3 language packages (AZ, RU, EN) are installed on the site. However, you can add any language you want to the database with the "Add another language" option. You can remove the language you don't want (if that language is not specified as the main language of the site in the site settings).

Dashboard
![alt text](/docs/site_languages.png)

Site
![alt text](/docs/site_languages_top.png)

Users can choose their preferred language. A column in the database adjusts this for them, if you are a guest on the site then the language selection is added to the cookies and you can still choose the language you want.

<hr>

* <b> Staff settings</b><br/>
You can add personal (First/Surname, Job Position and any social network).

Site
![alt text](/docs/staff.png)

<hr>

* <b> Message to management</b><br/>
When a registrant writes, a letter is sent on his behalf.
![alt text](/docs/message_1.png)
Guests must fill in all other fields when writing.
![alt text](/docs/message_2.png)
Spam prevented. There should be a pause of a few seconds between messages.
![alt text](/docs/spam.png)
Dashboard:

Notifications
![alt text](/docs/notifications.png)
![alt text](/docs/messages.png)
By the user

![alt text](/docs/from_user.png)
By the guest

![alt text](/docs/from_guest.png)


<hr>

* <b> User</b><br/>
Site

![alt text](/docs/profile.png)

Users can download 4 document files(JPG,JPEG,PNG).
![alt text](/docs/edu_files.png)
These files are also visible in the user's profile in the Admin Panel. It is intended for scanned documents that will be needed by the Site Administration.

Dashboard

![alt text](/docs/user_docs.png)


<hr>

* <b> General information about the site</b><br/>
If you don't add anything to the site from the Admin Panel, the site will be a white page. Sections of the site become visible as you add.
Features available on the site:
Registration
Login
Reset Passüord
Message to management
View user's profile (only admins can view and edit all profiles, everyone can only view and edit their own profile)
User can upload their documents and add profile picture.


_______________________________________

# Azərbaycanca Quraşdırılma
>### for <font color = "red">macOS / Linux</font>
#### I - <font color = "blue"><b>VENV</b></font> yaradırıq
``` 
$ python3 -m venv env

```
#### II - <font color = "blue"><b>requirements.txt</b></font> faylında nə varsa quraşdırırıq
```
$ source env/bin/activate
$ pip install -r requirements.txt

```
#### III - <font color = "blue"><b>.env</b></font> faylı yaradırıq. İçərisinə aşağıdaki lazımi məlumatları qeyd edirik.


```
SQLALCHEMY_DATABASE_URL=postgresql://postgres_userin:parolun@serverin/databaza_adı

SECRET_KEY='Secret Key'in'

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

MAIL_SERVER=smtp.gmail.com
MAIL_SENDER=email_adresin
MAIL_PASSWORD=email_parolun

```
<font color = "blue">SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES</font> (gün ilə qeyd olunub, hansı rəqəmi yazsanız o qədər gün aktiv olacaq) - Bunlar JWT üçün lazımdır.

<font color = "blue">MAIL_SERVER, MAIL_SENDER, MAIL_PASSWORD</font> - Bu məlumatlar olmadıqda saytın <font color = "red">parol bərpası</font> sistemi işləmiyəcək.

#### IV - Proqramı işə salırıq
```
uvicorn main:app --reload
```

# Scripti işə salmaq

#### I addım - aşağıdakı linkə daxil oluruq(link şərtidir, sizdə port vəya url başqa cür ola bilər). İlk öncə saytın parametrlərini yerləşdirmək üçün dil seçimi edirik. Qeyd: siz hansı dili seçsəniz Admin panelin əsas dili o olacaq(id=1), lakin digər dillər də sazlamalar tamamlandıqdan sonra yüklənəcək.

<b>http://127.0.0.1:8000/install/</b>

![alt text](/docs/installation_1.png)

#### II addım - Lazımlı məlumatları doldururuq
<font color = "blue">Super user</font> və <font color = "blue">adını</font> daxil edirik.

<font color = "blue">Sayt Parametri</font> əlavə edirik ki, saytımız işə düşsün. Əks təqdirdə saytımız işə düşməyəcək.

Sayt parametrində <font color = "blue">sayt URL</font> düzgün qeyd olunmalıdır ki, <font color = "red">Parol bərpası</font> üçün göndərilən link düzgün işləsin.

<font color = "blue">Saytın dilini</font> seçirik. Saytı işə saldıqdan sonra başqa dil də əlavə etmək olar. Bu əsas başlanğıc üçündür.


![alt text](/docs/installation_2.png)

#### Sayt artıq istifadəyə tam hazırdır ;)

![alt text](/docs/installation_completed.png)

<hr>                                                                                                                           

# Installation in English
>### for <font color = "red">macOS / Linux</font>
#### I - We create <font color = "blue"><b>VENV</b></font>
``` 
$ python3 -m venv env

```
#### II - We install whatever is in the <font color = "blue"><b>requirements.txt</b></font> file
```
$ source env/bin/activate
$ pip install -r requirements.txt

```
#### III -  We create an <font color = "blue"><b>.env</b></font> file. We enter the following necessary information into it.


```
SQLALCHEMY_DATABASE_URL=postgresql://postgres_user:postgress_password@server/databasa_name

SECRET_KEY='Secret Key'in'

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

MAIL_SERVER=smtp.gmail.com
MAIL_SENDER=your_email
MAIL_PASSWORD=your_email_password

```
<font color = "blue">SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES</font> (marked in days, the number of days you write will be active) - These are needed for JWT.

<font color = "blue">MAIL_SERVER, MAIL_SENDER, MAIL_PASSWORD</font> - 
If this information is not available, the site's <font color = "red">reset password</font> system will not work.


#### IV - We run the program
```
uvicorn main:app --reload
```

# Run the script

#### Step I - we enter the following link (the link is conditional, your port or url can be different). First of all, we select the language to place the site settings. Note: whichever language you choose will be the main language of the Dashboard(id=1), but other languages will also be loaded after the configuration is complete.

<b>http://127.0.0.1:8000/install/</b>

![alt text](/docs/installation_1.png)

#### Step II - We fill in the necessary information
We enter the <font color = "blue">Superuser</font> and <font color = "blue">his name.</font>

We add a <font color = "blue">Site Parameter</font> to launch our site. Otherwise, our site will not work.

The <font color = "blue">site URL</font> must be specified correctly in the site setting for the posted <font color = "red">password reset</font> link to work properly.


We select the <font color = "blue">language of the site</font> . Other languages may be added after the site is launched. This is a basic start.


![alt text](/docs/installation_2.png)

#### The site is now fully ready for use ;)

![alt text](/docs/installation_completed.png)

<hr>                                                                                                                           |
____

# Author

<b>Contributors names and contact info</b>

<b>ex. Pashayev Rafig - [PashaeFF - Github](https://github.com/PashaeFF) </b>

# Version

>* <b>v1.0</b>
>* <b>Initial Release</b>

___