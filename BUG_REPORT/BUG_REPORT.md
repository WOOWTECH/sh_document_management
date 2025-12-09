# Bug Report

## Bug 1

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

1. In `All Documents` page click any document.
2. Assign user to document.
3. Click save.
4. Click share icon.
5. User receive an email including `Download Attachmet URL`.
6. User click `Download Attachmet URL`

- Reference `Bug_2_screenshot_1.png` and `Bug_2_screenshot_2.png`.

### Expected behavior

Create remote URL download link for user.

### Actual behavior

Somehow the URL is showing the local address instead of a remote URL. If I manually change the local address to remote URL, the file can be downloaded normally.

- Reference `Bug_2_screenshot_3.png`.