const { app, BrowserWindow } = require('electron')

const createWindow = () => {
	const win = new BrowserWindow({
		width: 1000,
		height: 800
	})
	win.menuBarVisible = false
	win.loadFile('index.html')
}


async function makeRequest() {
	try {
		const fetch = (await import('node-fetch')).default;
		const response = await fetch('http://localhost:5000/process', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ data: 'test' })
		});
		const data = await response.json();
		console.log('Success:', data);
	} catch (error) {
		console.error('Error:', error);
	}
}

makeRequest();
//app.whenReady().then(createWindow)
