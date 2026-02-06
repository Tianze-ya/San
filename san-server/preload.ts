import { contextBridge, ipcRenderer } from 'electron';
import { BaseMessage } from './types';

const log = (msg: string): void => {
	ipcRenderer.invoke('log', msg);
};

const send = async (data: BaseMessage): Promise<void> => {
	await ipcRenderer.invoke('post', data);
};

contextBridge.exposeInMainWorld('ipc', {
	log,
	send,
});