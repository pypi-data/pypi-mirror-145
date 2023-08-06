===
CONVERT IMAGE TO BASE64
===

IMGTOBASE64 convert your image url from web or your image field from database to base64

Detailed documentation is in the "docs" directory.

## Quick start

1. Install the module:

   pip install imgtobase64

2. CASE OF IMAGE FROM WEB URL

   from imgtobase64.job import png_to_base64

   web_url = "https://sb.kaleidousercontent.com/67418/800x533/a5ddfb21a6/persons3-nobg.png"

   image_base4 = png_to_base64(web_url)

3. CASE OF IMAGE FROM FIELD OF A TABLE ON YOUR DB

   `We have a table named **Banner** with attribute **name image and description** so :
   So if we want tranform image to base64 to print blog on pdf,we will do this:

   import **imgtobase64**

   image_base4 = imgtobase64(banner.image)`
