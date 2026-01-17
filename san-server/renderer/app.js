async function api(name, addr = '') {
	let respons = await ipc.post({ name: name, address: addr });
	return respons;
}

document.querySelector('#active').addEventListener('click', () => {
	ipc.log('active');
});

document.querySelector('#get').addEventListener('click', async () => {
	let respons = await api('getAllAddress', '');
	ipc.log(respons);
});

document.querySelector('#photo').addEventListener('click', async () => {
	let respons = await api('photo', '');
	if (respons['data'] == 'ok') {
		//刷新
		ipc.log('ok');
	}
});
