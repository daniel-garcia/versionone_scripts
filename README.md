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
./epics_export.py "Required"
./epics_export.py "Re-review"
./epics_export.py "DA Review Required"
./epics_export.py "Done"
./epics_export.py ""
./epics_export.py "Not Required"

```
