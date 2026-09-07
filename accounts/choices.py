import pycountry

from phonenumbers import COUNTRY_CODE_TO_REGION_CODE


def get_country_code_choices():

    choices = []

    for country_code, regions in COUNTRY_CODE_TO_REGION_CODE.items():

        for region in regions:

            country = pycountry.countries.get(
                alpha_2=region
            )

            if country:

                choices.append(
                    (
                        f"+{country_code}",
                        region
                    )
                )

    return sorted(set(choices), key=lambda item: item[0])


COUNTRY_CODE_CHOICES = get_country_code_choices()