# Applying WIM

- Install and load Windows ISO file.
- Run this following command to see the available editions:

```cmd
dism /get-wiminfo /wimfile:"<|drive_letter:|>\sources\install.wim"
```

- Remember the index of the version that you want to install.
- Apply the wim image:

```cmd
dism /apply-image /imagefile:"<|drive_letter:|>\sources\install.wim" /index:"<|index-here|>" /applydir:"<|destination_drive_letter:|>\"
```
