from db.models.master_models import Countries
from db.database import engine, Base, SessionLocal

def save_language():
    # if __name__ == '__main__':
        #Crea la BD

        print('ejecutando save')
        Base.metadata.create_all(engine)

        #Abre la sesión
        session = SessionLocal()

        #* Load Lenguajes
        # lang1 = Languages(code = 'ES', language_name = 'Español')
        # lang2 = Languages(code = 'EN', language_name = 'English')
        # lang3 = Languages(code = 'FR', language_name = 'French')
        # session.add(lang1)
        # session.add(lang2)
        # session.add(lang3)

        # session.commit()

        #* Load Countries
        country1 = Countries(country_code='CO', country_phone_code = '+57')
        session.add(country1)

        #* Load Text Content
        tx1 = Tx_Content(tx_original="Colombia", lang_original='ES')
        session.add(tx1)


        #* Load Transalations
        translation1 = MData_Translations(language_code= 'ES', table_name='countries', translation='Colombia')
        translation2 = MData_Translations(language_code= 'EN', table_name='countries', translation='Colombia')
        session.add(translation1)
        session.add(translation2)

        #* Text content - Translations Relationships
        tx1.translations = [translation1, translation2]

        #* Text content - Countries Relationships
        tx1.countries = [country1]


        
        session.commit()
        session.close()