344C3_Avramescu_Cosmin

--- Aspecte generale
    Punctul de pornire al aplicatiei este scriptul run.sh, care face 2 lucruri: da comanda docker swarm init, care initializeaza ca nod manager masina de pe care se ruleaza, apoi se face build cu ajutorul Dockerfile pentru a se crea imaginea adaptorului. Dupa rularea acestui script, se pot rula comenzile de deploy stack, apoi python3 iot_simulator.py pentru a trimite date prin mqtt, adaptor catre baza de date. Apoi se poate da comanda cu stack rm pentru a verifica ulterior persistenta datelor.

--- fisierul stack.yml
    Contine 4 servicii (mqtt, influxdb, adaptor, grafana) si 3 retele (broker_adapter_net, db_adapter_net, grafana_db_net). Dupa cum sunt si numite retelele, ele au scopul de a limita comunicarea doar intre componentele specificate (brokerul comunica doar cu adaptorul, baza de date comunica cu adaptorul si grafana). Se pornesc pe rand serviciile, fiecare are setata replicarea 1 pentru deploy. Porturile sunt cele
    standard pentru fiecare serviciu. La adaptor am setat variabila de mediu "DEBUG_DATA_FLOW" pentru a putea fi afisat logging, iar grafana are ca variabile de mediu credentialele. Folosesc fisierul de config pentru a elimina autentificarea de la mqtt. Datele isi pastreaza persistenta datorita prezentei volumelor.

--- fisierul Dockerfile
    Fisierul porneste de la imaginea de python si instaleaza in directorul curent requirements.txt (in cazul nostru, mqtt si influxdb, bibliotecile de python). Prin COPY . . se copiaza tot continutul directorului curent in imaginea de docker (cu exceptia fisierelor mentionate in .dockerignore) si se seteaza comanda de rulare pentru aceasta imagine (python3 adapter.py).

--- fisierul adapter.py
    Se seteaza ca variabila globala instanta bazei de date. Daca nu exista deja baza de date iot_db, atunci se creaza. In main se seteaza formatul logurilor si level-ul INFO. Doar la mesajele de eroare se va intra pe level-ul ERROR. Se creaza conexiunea cu mqtt, se face abonarea la toate topicurile, iar la primirea unui mesaj, se extrag locatia, statia si payload-ul. Daca primim deja timestamp, doar il formatam, daca nu, atunci extragem timestamp-ul curent si il formatam si pe acesta. Trecem prin toate valorile din payload, extragem doar valorile numerice si facem append cu json-ul (setat cu tag pe locatie, statie si tipul senzorului). Daca a fost gasita cel putin o valoarea numerica, se face scrierea in baza de date. Ulterior vom putea vedea datele introduse in influxdb cu urmatoarele comenzi: USE iot_db, SHOW MEASUREMENTS, select * from "UPB.station1.BAT"

--- fisierul iot_simulator.py
    Aici se face conectarea la mqtt, iar datorita faptului ca adaptorul s-a abonat la toate topicurile brokerului, el va receptiona tot ce este trimis de acest simulator. Se trimit mai multe combinatii de valori numerice cu random, iar din 4 in 4 mesaje trimise se adauga un timestamp si in plus un mesaj string ca sa se verifice ca in baza de date vor ajunge doar valori numerice. Se trimit 20 de pachete in total, apartinand uneia dintre statiile 1, 2 sau 3.
