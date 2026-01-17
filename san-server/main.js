const { app, BrowserWindow, Menu, ipcMain } = require('electron');
const {
	ensureServerRunning,
	cleanupPythonProcess,
	post,
	api,
} = require('./py_server');
const path = require('node:path');
const mainMenu = Menu.buildFromTemplate(require('./menu'));

const createWindow = () => {
	const win = new BrowserWindow({
		width: 1000,
		height: 800,
		webPreferences: {
			preload: path.join(__dirname, 'preload.js'),
		},
	});
	//win.menuBarVisible = false;

	win.loadFile('index.html');
	Menu.setApplicationMenu(mainMenu);
};

// 应用关闭时清理Python进程
app.on('before-quit', async () => {
	await cleanupPythonProcess();
});

app.on('activate', () => {
	if (BrowserWindow.getAllWindows().length === 0) {
		createWindow();
	}
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.whenReady().then(async () => {
	ipcMain.handle('log', async (_event, msg) => {
		console.log(msg);
	});

	ipcMain.handle('post', async (_event, body_data) => {
		return await api(body_data);
	});
	// 启动时确保服务器运行
	await ensureServerRunning();
	createWindow();
	post('active', '');
});
