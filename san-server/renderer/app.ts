import { makeMsg } from '../tool'

async function api(name: string, desc: string = '', data: Blob = new Blob()): Promise<void> {
	await window.ipc.send(makeMsg(name, desc, data));
}

document.querySelector('#active')?.addEventListener('click', () => {
	window.ipc.log('active');
});

document.querySelector('#get')?.addEventListener('click', async () => {
	await api('getAllAddress');
	//window.ipc.log();
});

document.querySelector('#photo')?.addEventListener('click', async () => {
	await api('photo');
});