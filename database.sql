BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "activiteiten" (
	"Activiteit_ID"	INTEGER NOT NULL UNIQUE,
	"Titel"	TEXT NOT NULL,
	"Thema"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Activiteit_ID")
);
CREATE TABLE IF NOT EXISTS "contact" (
	"Contact_ID"	INTEGER NOT NULL UNIQUE,
	"Naam"	TEXT NOT NULL,
	"Email"	TEXT NOT NULL,
	"Bericht"	TEXT NOT NULL,
	"Activiteit_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Contact_ID" AUTOINCREMENT),
	FOREIGN KEY("Activiteit_ID") REFERENCES "activiteiten"("Activiteit_ID")
);
CREATE TABLE IF NOT EXISTS "favorieten" (
	"Gebruiker_ID"	INTEGER NOT NULL,
	"Activiteit_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Gebruiker_ID","Activiteit_ID"),
	FOREIGN KEY("Activiteit_ID") REFERENCES "activiteiten"("Activiteit_ID"),
	FOREIGN KEY("Gebruiker_ID") REFERENCES "gebruikers"("Gebruiker_ID")
);
CREATE TABLE IF NOT EXISTS "gebruikers" (
	"Gebruiker_ID"	INTEGER NOT NULL UNIQUE,
	"Gebruikersnaam"	TEXT NOT NULL UNIQUE,
	"Email"	TEXT NOT NULL UNIQUE,
	"Wachtwoord"	TEXT NOT NULL,
	PRIMARY KEY("Gebruiker_ID" AUTOINCREMENT)
);
INSERT INTO activiteiten (Titel, Thema)
VALUES
	("Oefening rust: Dankbaarheid", "rust_dankbaarheid"),
	("Oefening rust: Meditatie", "rust_mediteren"),
	("Oefening rust: Ademhaling", "rust_ademhaling"),
	("Oefening rust: Hier en nu", "rust_hier_en_nu"),
	("Oefening rust: Journal", "rust_journal"),
	("Oefening balans: Hobby", "balans_hobby"),
	("Oefening balans: Grenzen", "balans_grenzen"),
	("Oefening balans: Planning", "balans_planning"),
	("Oefening balans: Spieren ontspannen", "balans_spieren_ontspannen"),
	("Oefening balans: Levensdomein", "balans_levensdomein"),
	("Oefening groei: Uitdagingen lijst", "groei_uitdagingen_lijst"),
	("Oefening groei: Moeilijke momenten evalueren", "groei_moeilijke_momenten_evalueren"),
	("Oefening groei: Bereidheid", "groei_bereidheid"),
	("Oefening groei: Leer jezelf beter kennen", "groei_leer_jezelf_beter_kennen"),
	("Oefening groei: Ontwikkel je zelfbewust zijn", "groei_ontwikkel_je_zelfbewust_zijn");
COMMIT;