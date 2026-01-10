const { spawn } = require('child_process');
const path = require('path');
const net = require('net');

// Python进程管理
let pythonProcess = null;
const PYTHON_SERVER_PORT = 5000;
const PYTHON_SERVER_HOST = '127.0.0.1';

// 检测服务器是否已运行
async function isServerRunning() {
	return new Promise((resolve) => {
		const socket = new net.Socket();

		socket.setTimeout(1000);
		socket.connect(PYTHON_SERVER_PORT, PYTHON_SERVER_HOST, () => {
			socket.destroy();
			resolve(true);
		});

		socket.on('error', () => {
			resolve(false);
		});

		socket.on('timeout', () => {
			socket.destroy();
			resolve(false);
		});
	});
}

// 启动Python服务器
async function startPythonServer() {
	return new Promise((resolve, reject) => {
		console.log('正在启动Python服务器...');

		pythonProcess = spawn('uv run flask_server.py', {
			cwd: path.join(__dirname, 'python'),
			stdio: ['pipe', 'pipe', 'pipe'],
			shell: true,
		});

		pythonProcess.stdout.on('data', (data) => {
			console.log(`Python服务器输出: ${data}`);
		});

		pythonProcess.stderr.on('data', (data) => {
			console.error(`Python服务器错误: ${data}`);
		});

		pythonProcess.on('exit', (code, signal) => {
			pythonProcess = null;
		});

		pythonProcess.on('error', (error) => {
			console.error('启动Python服务器失败:', error.message);
			reject(error);
		});

		// 等待服务器启动
		setTimeout(async () => {
			const running = await isServerRunning();
			if (running) {
				console.log('Python服务器启动成功');
				resolve();
			} else {
				console.error('Python服务器启动失败');
				reject(new Error('Python服务器启动失败'));
			}
		}, 3000);
	});
}

// 确保服务器运行
async function ensureServerRunning() {
	const isRunning = await isServerRunning();
	if (!isRunning) {
		console.log('Python服务器未运行，正在启动...');
		await startPythonServer();
	} else {
		console.log('Python服务器已运行');
	}
}

// 清理Python进程
function cleanupPythonProcess() {
	api('exit', '');
	console.log('关闭Python服务器');
	pythonProcess = null;
}

async function api(api, body_data) {
	try {
		const fetch = (await import('node-fetch')).default;
		const response = await fetch(
			`http://${PYTHON_SERVER_HOST}:${PYTHON_SERVER_PORT}/${api}`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ data: body_data }),
			}
		);
		const data = await response.json();
		console.log('Success:', data);
	} catch (_error) {
		console.error('API调用失败');
	}
}

// 导出函数供其他模块使用
module.exports = {
	isServerRunning,
	startPythonServer,
	ensureServerRunning,
	api,
	cleanupPythonProcess,
};
