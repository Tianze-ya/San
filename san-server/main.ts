import { app, BrowserWindow, Menu, ipcMain } from 'electron';
import {
	ensureSanRunning,
	cleanSanProcess,
	send,
} from './py_server';
import { makeMsg } from './tool';
import path from 'node:path';
import { BaseMessage } from './types';
import menuTemplate from './menu';

const createWindow = (): void => {
	const win = new BrowserWindow({
		width: 1000,
		height: 800,
		webPreferences: {
			preload: path.join(__dirname, 'preload.js'),
		},
	});

	win.loadFile('index.html');
	const mainMenu = Menu.buildFromTemplate(menuTemplate);
	Menu.setApplicationMenu(mainMenu);
};

// 应用关闭时清理Python进程
app.on('before-quit', async () => {
	await cleanSanProcess();
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
	ipcMain.handle('log', async (_event, msg: string) => {
		console.log(msg);
	});

	ipcMain.handle('send', async (_event, body_data: BaseMessage) => {
		await send(body_data);
	});

	// 启动时确保服务器运行
	await ensureSanRunning();
	createWindow();
	send(makeMsg('ping'));
});

