# Bug Report

## Bug 1 (SOLVED)

### Test step 

1. In `All Documents` page hover on the top right corner of any document then click `Dropdown menu`.
2. `Dropdown menu` will show 2 options, `Download` and `Delete`.
3. Click `Download`. 

- Reference `Bug_1_screenshot_1.png`.

### Expected behavior

Let user download the file.

### Actual behavior

`Missing Action` message popup shows that the action "content" does not exit.

- Reference `Bug_1_screenshot_2.png`.

## Bug 2

### Test step 

1. Login with local URL.
2. Assign user to document, and then click share icon.
3. User receive an email including `Download Attachmet URL - before`.
4. Re-login with remote URL.
5. Assign user to document, and then click share icon.
6. User receive an email including `Download Attachmet URL - after`.

### Expected behavior

Create remote URL download link for user correctly.

### Actual behavior - `Download Attachmet URL - before`

- As expected, the link is using local URL.

```html
    <a style="font-weight:bold;text-decoration:None" href="http://192.168.2.6/attachment/download_directories?list_ids=1396&amp;access_token=a84e9293-9bc3-476e-93fa-886dc64d142a&amp;name=document" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://192.168.2.6/attachment/download_directories?list_ids%3D1396%26access_token%3Da84e9293-9bc3-476e-93fa-886dc64d142a%26name%3Ddocument&amp;source=gmail&amp;ust=1765365728074000&amp;usg=AOvVaw3mKaflCPcSaR8LcqgjcD9A">Click To
                                Download</a>
```

### Actual behavior - `Download Attachmet URL - after`

- The linked content appears to be correct. But when I click the link, it open a new empty page and close it. 

```html
    <a style="font-weight:bold;text-decoration:None" href="http://woowtech-testodoo.woowtech.io/attachment/download_directories?list_ids=1396&amp;access_token=a84e9293-9bc3-476e-93fa-886dc64d142a&amp;name=document" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://woowtech-testodoo.woowtech.io/attachment/download_directories?list_ids%3D1396%26access_token%3Da84e9293-9bc3-476e-93fa-886dc64d142a%26name%3Ddocument&amp;source=gmail&amp;ust=1765365835531000&amp;usg=AOvVaw1eyVNVWuANLx-bJC3m24FJ">Click To
                                Download</a>
```                      