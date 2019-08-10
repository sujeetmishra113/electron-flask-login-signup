const {app, BrowserWindow} = require('electron')
const path = require("path");
const log = require('electron-log');

const createNewPyProc = () => {
    let script = path.join(__dirname, 'loginsignup.exe');
    newPyProc = require('child_process').spawn(script);

    if (newPyProc != null) {
        log.info('child process for flask API success');
    }
    else {
        log.error("unable to start child");
    }
}


let parentwin;
function createWindow () {
	createNewPyProc();
    log.info('success');

    parentwin = new BrowserWindow({width: 800, height: 600})
    parentwin.loadFile('index.html');

    parentwin.openDevTools();
}


app.on('ready', createWindow)
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
})