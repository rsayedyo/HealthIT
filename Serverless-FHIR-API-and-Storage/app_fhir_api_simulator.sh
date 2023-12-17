#!/bin/sh
#  The file simulates an application creating a new patient record.
api_url="<API_URL>"
api_key="<API_KEY>"

echo '\nCREATE 1---------------------------------------------------------------------------'
curl -X POST \
    -H 'Content-Type: application/json' \
    $api_url'/r4/Patient' -d'
{
    "resourceType": "Patient",
    "api_url": "'$api_url'",
    "id": "1",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2020-01-21T05:30:30.527+00:00",
        "source": "#onxG4W83SbUORCVY"
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Terry <b>Whitlock </b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>a5fc83ec-1821-43b1-b294-9d2347ef5df7</td></tr></tbody></table></div>"
    },
    "identifier": [
        {
            "type": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/v2/0203",
                        "code": "MR"
                    }
                ]
            },
            "value": "a5fc83ec-1821-43b1-b294-9d2347ef5df7"
        }
    ],
    "name": [
        {
            "family": "Whitlock",
            "given": [
                "Terry"
            ]
        }
    ]
}'

echo $0
read -p "Record 1 created. Press enter to run the next POST request."
clear
#!/bin/sh
echo '\nCREATE 2---------------------------------------------------------------------------'
curl -X POST \
    -H 'Content-Type: application/json' \
    $api_url'/default/r4/Patient' -d '
{
    "resourceType": "Patient",
    "api_url": "'$api_url'",
    "id": "2",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2020-01-21T05:30:30.527+00:00",
        "source": "#onxG4W83SbUORCVY"
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Terry <b>Whitlock </b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>a5fc83ec-1821-43b1-b294-9d2347ef5df7</td></tr></tbody></table></div>"
    },
    "identifier": [
        {
            "type": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/v2/0203",
                        "code": "MR"
                    }
                ]
            },
            "value": "a5fc83ec-1821-43b1-b294-9d2347ef5df7"
        }
    ],
    "name": [
        {
            "family": "Whitlock",
            "given": [
                "Terry"
            ]
        }
    ]
}'

echo $0
read -p "Record 2 created. Press enter to run the PUT request."
clear
echo '\nUPDATE---------------------------------------------------------------------------'

curl -X PUT \
    -H 'Content-Type: application/json' \
    $api_url'/default/r4/Patient' -d '
{
    "resourceType": "Patient",
    "api_url": "'$api_url'",
    "id": "1",
    "meta": {
        "versionId": "1",
        "lastUpdated": "2020-01-21T05:30:30.527+00:00",
        "source": "#onxG4W83SbUORCVY"
    },
    "text": {
        "status": "generated",
        "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><div class=\"hapiHeaderText\">Terry <b>Whitlock </b></div><table class=\"hapiPropertyTable\"><tbody><tr><td>Identifier</td><td>a5fc83ec-1821-43b1-b294-9d2347ef5df7</td></tr></tbody></table></div>"
    },
    "identifier": [
        {
            "type": {
                "coding": [
                    {
                        "system": "http://hl7.org/fhir/v2/0203",
                        "code": "MR"
                    }
                ]
            },
            "value": "a5fc83ec-1821-43b1-b294-9d2347ef5df7"
        }
    ],
    "name": [
        {
            "family": "Whitlock Updated",
            "given": [
                "Terry"
            ]
        }
    ]
}'

echo $0
read -p "Record 1 updated. Press enter to run the GET request."
clear
echo '\nREAD---------------------------------------------------------------------------'

curl -X GET -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient/1'

echo $0
read -p "Retrieve record from /default/r4/Patient/1. Press enter to run the next GET request."
clear
echo '\nSEARCH 1 ITEM---------------------------------------------------------------------------'

curl -X GET -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient?id=1'

echo $0
read -p "Retrieve record from /default/r4/Patient?id=1. Press enter to run the next GET request."
clear
echo '\nSEARCH 2 ITEMS---------------------------------------------------------------------------'

curl -X GET -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient?name.given=Terry'

echo $0
read -p "Retrieve records from /default/r4/Patient?name.given=Terry. Press enter to run the next GET request."
clear
echo '\nSEARCH 1 ITEM---------------------------------------------------------------------------'

curl -X GET -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient?name.given=Terry&id=1'

echo $0
read -p "Retrieve record from /default/r4/Patient?name.given=Terry&id=1. Press enter to run the next GET request."
clear
echo '\nSEARCH 0 ITEMS---------------------------------------------------------------------------'

curl -X GET -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient?name.given=Souza'

echo $0
read -p "Retrieve record from /default/r4/Patient?name.given=Souza. Press enter to run the DELETE request."
clear
echo '\nDELETE---------------------------------------------------------------------------'

curl -X DELETE -H "Accept: application/json" -H "x-api-key:$api_key" $api_url'/default/r4/Patient/1'

echo '\n'
