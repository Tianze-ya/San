const { app, BrowserWindow } = require('electron');
const {
	ensureServerRunning,
	api,
	cleanupPythonProcess,
} = require('./py_server');

const createWindow = () => {
	const win = new BrowserWindow({
		width: 1000,
		height: 800,
	});
	win.menuBarVisible = false;
	win.loadFile('index.html');
};

// 应用关闭时清理Python进程
app.on('before-quit', () => {
	cleanupPythonProcess();
});

app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit();
	}
});

app.whenReady().then(async () => {
	// 启动时确保服务器运行
	await ensureServerRunning();
	createWindow();
	api('active', '');
});
