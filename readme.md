<p> Šis projektas skirtas kurti ir valdyti vartotojų automobilių duomenų bazę, įskaitant informaciją apie automobilius, degalines ir automobilio aptarnavimą. Vartotojas gali fiksuoti tokią informaciją kaip degalų kiekis automobilio bake, automobilio rida, degalų kaina ir aptarnavimo istorija bei kaina.</p>
<br />
simple user nėra.

Admin:
usr: admin
psw: admin
<br />
<h3>admin.py:</h3>
Importuojami reikalingi Django modeliai iš models.py failo.


Sukuriamos CarAdmin, CarModelAdmin, UserCarAdmin, GasStationNameAdmin klasės  kurios bus rodomos Django administracijos puslapyje

<br />
<h3>forms.py:</h3>


<b>GasStationNameSelectWidget:</b> Specializuota forma, kuri leidžia sukurti pasirinkimo lauką su papildomomis savybėmis.

<b>UserCarForm:</b> ModelForm tipo forma skirta UserCar modeliui.

<b>CarMileageForm:</b> ModelForm tipo forma skirta CarMileage modeliui.

<b>AddCarForm:</b> forma, kurią naudojant vartotojas gali pridėti naują automobilį į sistemą.

<b>EditGasStationForm:</b> skirta GasStation modelio informacijos redagavimui.

<b>AddMileageForm:</b> forma, kurią naudojant vartotojas gali pridėti naują automobilio kilometražą.

<b>CarServiceEventForm:</b> forma skirta CarServiceEvent modeliui.

<br />
<h3>models.py:</h3>

<b>Car:</b> automobilio gamintojas

<b>CarModel:</b> automobilio modelis, kuris yra susijęs su automobilio gamintoju.

<b>UserCar:</b> konkretaus vartotojo turimas automobilis. Jis yra susijęs tiek su User, tiek su CarModel. Jame taip pat saugoma informacija apie automobilio metus, kuro tipą, VIN ir valstybinį numerį.

<b>GasStationName:</b> degalių pavadinimai (įmonės). Jis naudojamas tam, kad būtų išvengta pavadinimų dubliavimo.

<b>GasStation:</b> konkreti degalinė, kurioje automobilis pildėsi kuro.

<b>CarMileage:</b> Šis modelis naudojamas tam, kad sekti su rida susijusią informaciją apie konkretų automobilį. Apima tokią informaciją, kaip automobilio odometro parodymai, kuro kiekis bake, automobilio nuvažiuotas atstumas, kuro kaina ir rida.

<b>CarServiceEvent:</b> Šis modelis skirta fiksuoti bet kokį aptarnavimo įvykį, susijusį su vartotojo automobiliu. Jis yra susijęs su User ir UserCar modeliais ir fiksuoja tokią informaciją, kaip pavadinimas, data, aptarnavimo aprašymas ir jo kaina.

<br />
<h3>views.py:</h3>


<b>home_page:</b> atvaizduoja pagrindinį puslapį, jei naudotojas neprisijungęs, nukreipia į prisijungimo puslapį, gauna susijusius automobilio duomenis iš duomenų bazės ir atvaizduoja.

<b>register:</b> naudotojo registracija, patikrina formos duomenis, išsaugo naują naudotoją ir nukreipia į prisijungimo puslapį.

<b>user_login:</b> naudotojo prisijungimas, patikrina prisijungimo formos duomenis, autentifikuoja naudotoją ir nukreipia į pagrindinį puslapį po sėkmingo prisijungimo.

<b>user_logout:</b> atjungia naudotoją ir nukreipia į prisijungimo puslapį.

<b>logged_home:</b> atvaizduoja pagrindinį puslapį prisijungusiems naudotojams.

<b>add_car:</b> leidžia naudotojui pridėti naują automobilį į savo profilį, tvarko formos pateikimą, patikrina duomenis, kuria susijusius modelio objektus (UserCar, GasStation, CarMileage) ir išsaugo juos duomenų bazėje.

<b>your_car_info:</b> gauna ir atvaizduoja informaciją apie naudotojo automobilius.

<b>edit_car:</b> leidžia naudotojui redaguoti automobilio informaciją, tvarko formos pateikimą, atnaujina susijusius modelio objektus ir išsaugo pakeitimus.

<b>delete_car:</b> ištrina automobilį ir susijusius degalinės įrašus iš duomenų bazės.

<b>add_mileage:</b> leidžia naudotojui pridėti ridą į konkretų automobilio įrašą, tvarko formos pateikimą, patikrina duomenis, kuria ir išsaugo susijusius modelio objektus.

<b>mano_service:</b> gauna ir atvaizduoja susijusius aptarnavimo įvykius naudotojo automobiliams.

<b>service_new:</b> leidžia naudotojui pridėti naują aptarnavimo įvykį, tvarko formos pateikimą, patikrina duomenis ir išsaugo aptarnavimo įvykį.

<b>service_edit:</b> leidžia naudotojui redaguoti aptarnavimo įvykį, tvarko formos pateikimą, atnaujina aptarnavimo įvykį ir išsaugo pakeitimus.

<b>service_delete:</b> Ištrina aptarnavimo įvykį iš duomenų bazės.
