# qt-desktop-translate

qt-desktop-translate allows translating .desktop files using .ts files from Qt.

## Installation

Install qt-desktop-translate with pip

```
pip install qt-desktop-translate
```

## Create translations

To create translations, use desktop-lupdate

```
desktop-lupdate your_desktop_file.desktop your_ts_file.ts
```

This will add the fields from the .desktop file to the .ts file. Now you can use Qt Linguist or any other tool, that allows translating .ts files. Call desktop-lupdate everytime after you've ran the normal lupdate. You can specify a folder instead of a single .ts file.

## Apply translations

To apply translations run, use desktop-lrelease

```
desktop-lrelease your_desktop_file.desktop output.desktop your_ts_file.ts
```

This will translate desktop-lupdate your_desktop_file.desktop using the translations from your_ts_file.ts. The output will be written into output.desktop. You can specify a folder instead of a single .ts file.
