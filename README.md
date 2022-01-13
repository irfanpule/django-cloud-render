## Blender Cloud Render

This is a simple web app to render project blender on cloud. It's develop on django web framework.

### Prerequisite
* Install Redis
* Install Python 3.6 or latest
* virtualenv


### To do list
- [x] Client Browser
    - [x] Form upload project
    - [x] Form prerender
    - [x] Show render process
    - [x] Show result render
    - [ ] Download result render
- [x] API
    - [x] Upload file project
    - [x] Get Information prerender
    - [x] Render Process
    - [x] Get log render process
    - [ ] Get result render
    - [ ] Download result render
- [ ] Client Blender Addon
    - [ ] Form Configuration
    - [ ] Form prerender
    - [ ] Render process
- [x] Other features
    - [x] automatic check max thread
    - [ ] automatic check option cycles `CPU+GPU` already
    - [x] automatic get total frame from project blender
    - [ ] Send notification email when process is finish
- [x] Testing
    - [x] Test render option cycles `CPU`
    - [ ] Test render option cycles `CPU+GPU`
    - [ ] Test on server using GPU or not
