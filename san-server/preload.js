const { contextBridge, ipcRenderer } = require('electron');

const log = (msg) => {
	ipcRenderer.invoke('log', msg);
};

const post = async (data) => {
	let response = await ipcRenderer.invoke('post', data);
	return response;
};

contextBridge.exposeInMainWorld('ipc', {
	log,
	post,
});
