# photorder (Perl version)

# Common info
This is a tool for renaming and rearranging photos.
Main version of it is implemented in Python. Perl version is here just because I don't want to forget perl entirely.

## How to use it

### Exif library installation

**Windows**
- Install Chocolatey using PowerShell as Administrator (it's a convenient package manager for Windows). How to install: https://chocolatey.org/install
- Install exiftool library using cpamn: 
  ```
  cpanm Image::EXIF
  ```

**Linux**
It's not tested yet on Linux, but it seems that following will easily install needed library:
```
cpanm Image::EXIF
```


### Supported features
TBD


### Supported filenames and cameras
RAW:
- SAM_7074.SRW - Samsumg NX210
- IMG_2722.CR2 - Canon G9x
- DSC01524.ARW - Sony RX100 IV

JPEGs:
- P1170111 - Olympus FE190/X750
- SDC15203 - Samsung WB510
- DSC00705 - Sony Erricsson S500i

#### Names in downloaded archive from Flickr:
- 20160208-sam_7074_32246700620_o.jpg (from cameras)
- 2016-01-30-224544_28731621530_o.jpg (from ipad/iphone)


## Known exceptions
TBD