## Blender Cloud Render

This is a simple web app to rendering blender project on cloud. It's develop use django web framework.

### Prerequisite
* Install Redis
* Install Python 3.6 or latest
* virtualenv


### To do list
- [x] Client Browser
    - [x] Project Form
      - Input project name, blender file and etc
    - [x] Prerender Form 
      - Show detail project
      - Input start frame, end frame, option render, total thread etc
    - [x] Show render process
      - Show log, time, remaining and progress bar
    - [x] Show result render
      - Show all image
    - [x] Download result render
      - Download all image on .zip
- [x] API
    - [x] Endpoint Add project
      - POST: project name, blender file and etc
    - [x] Endpoint Render
      - GET: detail project
      - POST: start frame, end frame, option render, total thread etc, then exec render job
    - [x] Endpoint Log Process
      - GET: detail log and state process
    - [ ] Endpoint Result Render
    - [ ] Endpoint Download Render
- [x] Client Blender Addon
    - [x] Configuration Form
      - Input hostname or ip server
    - [ ] Prerender Form
      - Input start frame, end frame, option render, total thread etc
    - [ ] Render process
      - Show state process and open browser when finish render to get result
- [x] Other features
    - [x] automatic check max thread
    - [ ] automatic check option cycles `CPU+GPU` already
    - [x] automatic get total frame from project blender
    - [ ] Send notification email when process is finish
- [x] Testing
    - [x] Test render option cycles `CPU`
    - [ ] Test render option cycles `CPU+GPU`
    - [ ] Test on server using GPU or not
- [x] Project Management
    - [x] Create project
    - [ ] Manage all flow project process use user auth
      - website and API
