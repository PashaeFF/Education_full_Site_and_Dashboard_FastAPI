# Education site (Full Admin panel control)

- [Education site](#education-site)
- [Project Title](#project-title)
- [Description](#description)
- [Installing](#installing)
      - [First](#first)
      - [Second](#second)
      - [Third](#third)
      - [First m](#first-m)
      - [Second](#second-1)
      - [Third](#third-1)
- [Executing program](#executing-program)
- [Environment variables](#environment-variables)
- [Author](#author)
- [Version](#version)
___

# Project Title
___
* <b>Education site</b>
___

# Description
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


>### for <font color = "red">macOS / Linux</font>
#### I - <font color = "blue"><b>VENV</b></font> yaradırıq
``` 
$ python3 -m venv env

```
#### II - <font color = "blue"><b>requirements.txt</b></font> faylında nə varsa yükləyirik
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

<hr>                                                                                                                           |
____

# Author

<b>Contributors names and contact info</b>

<b>ex. Pashayev Rafig - [PashaeFF - Github](https://github.com/PashaeFF) </b>

# Version

>* <b>v1.0</b>
>* <b>Initial Release</b>

___