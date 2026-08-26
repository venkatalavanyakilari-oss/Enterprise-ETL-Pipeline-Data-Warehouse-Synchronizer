from src.api_extractor import APIExtractor


def main():

    print("Starting ETL API Extraction...")

    extractor = APIExtractor()

    try:

        users = extractor.fetch_users()

        print(f"Records extracted: {len(users)}")

        for user in users[:5]:
            print(user.model_dump())

    except Exception as error:

        print(f"ETL extraction failed: {error}")


if __name__ == "__main__":
    main()
