# versionone_scripts

To work on VersionOne you will need to create an access token. You do this
by going to your Applications and creating a Private Application and you will
be given an access token, you need to copy the value from the clipboard as it
will not be shown again. Here is the screenshot of the page after the 
access token is created:

![Image of V1 Application with Access Token](images/v1_access_token.png)

Example of using epic export
```bash
export VERSION_ONE_ENDPOINT=https://www10.v1host.com/InfobloxNewV1
export VERSION_ONE_TOKEN=letmein
./epics_export.py ""
./epics_export.py "Done"
./epics_export.py "In Progress"
./epics_export.py "Required"
./epics_export.py "DA Review Required"
./epics_export.py "Ready for Eng Review"
./epics_export.py "Re-review"
./epics_export.py "Rejected"
./epics_export.py "Not Required"

./epics_export.py --scope "Athena 3.X" "Required"
./epics_export.py --scope "Athena 3.1" "Required"
./epics_export.py --scope "Athena 3.2" "Required"
./epics_export.py --scope "Athena 3.3" "Required"
./epics_export.py --scope "Athena 3.4" "Required"
./epics_export.py --scope "Athena 3.X" "DA Review Required"
./epics_export.py --scope "Athena 3.X" "DA Review Required"
./epics_export.py --scope "Athena 3.1" "DA Review Required"
./epics_export.py --scope "Athena 3.2" "DA Review Required"
./epics_export.py --scope "Athena 3.3" "DA Review Required"
./epics_export.py --scope "Athena 3.4" "DA Review Required"
./epics_export.py --scope "Athena 3.X" "Done"
./epics_export.py --scope "Athena 3.1" "Done"
./epics_export.py --scope "Athena 3.2" "Done"
./epics_export.py --scope "Athena 3.3" "Done"
./epics_export.py --scope "Athena 3.4" "Done"
./epics_export.py --scope "Athena 3.X" "Not Required"
./epics_export.py --scope "Athena 3.1" "Not Required"
./epics_export.py --scope "Athena 3.2" "Not Required"
./epics_export.py --scope "Athena 3.3" "Not Required"
./epics_export.py --scope "Athena 3.4" "Not Required"


```

## VersionOne APIs

There are some documentation here to read:
https://community.versionone.com/Digital.ai_Agility_Integrations/Developer_Library

The VersionOne attributes epecially the custom ones we added have some encoding
to figure out how they are mapped you can go to the browser and dump them
like this:
https://www10.v1host.com/InfobloxNewV1/meta.v1/Epic?xsl=api.xsl

Then you can find the attribute and use them in your query.
