import net from 'net';
import path from 'path';
import { spawn, ChildProcess } from 'child_process';
import { BaseMessage } from './types';

// Python进程管理
let sanProcess: ChildProcess | null = null;
let client: net.Socket | null = null;
const PYTHON_SERVER_HOST = '127.0.0.1';
const PYTHON_SERVER_PORT = 9241;


async function connect(): Promise<void> {
	client = new net.Socket();
	client.connect(PYTHON_SERVER_PORT, PYTHON_SERVER_HOST, () => {
		console.log('Socket > Python');
	});

	client.on('data', (data) => {
		console.log('收到数据:', data.toString('utf8'));
		//client!.destroy();
	});

	client.on('error', (err) => {
		console.error('Socket错误:', err);
	});

	client.on('close', () => {
		console.log('Socket连接关闭');
	});
}

// 检测服务器是否已运行
async function isSanRunning(): Promise<boolean> {
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
async function startSan(): Promise<void> {
	return new Promise((resolve, reject) => {
		console.log('正在启动San');

		// Use Python executable from the virtual environment
		// Since __dirname points to dist/ after compilation, we need to go up one level
		const projectRoot = path.join(__dirname, '..');
		const pythonDir = path.join(projectRoot, 'python');
		sanProcess = spawn('uv', ['run', 'san_server.py'], {
			cwd: pythonDir,
			stdio: ['pipe', 'pipe', 'pipe'],
			shell: false,
		});

		if (sanProcess.stdout) {
			sanProcess.stdout.on('data', (data) => {
				console.log(`San输出: ${data}`);
			});
		}

		if (sanProcess.stderr) {
			sanProcess.stderr.on('data', (data) => {
				console.error(`San错误: ${data}`);
			});
		}

		sanProcess.on('exit', (_code, _signal) => {
			sanProcess = null;
		});

		sanProcess.on('error', (error) => {
			console.error('启动San失败:', error.message);
			reject(error);
		});

		// 等待服务器启动
		setTimeout(async () => {
			const running = await isSanRunning();
			if (running) {
				console.log('San启动成功');
				resolve();
			} else {
				console.error('San启动失败');
				reject(new Error('San启动失败'));
			}
		}, 3000);
	});
}

// 确保服务器运行,如果未运行则启动,启动Socket链接
async function ensureSanRunning(): Promise<void> {
	const isRunning = await isSanRunning();
	if (!isRunning) {
		console.log('San未运行，正在启动...');
		await startSan();
	} else {
		console.log('San已运行');
	}
	await connect();
}

// 清理Python进程
async function cleanSanProcess(): Promise<void> {
	//await post('exit', '');
	console.log('关闭San');
	sanProcess = null;
}

async function send(basemsg: BaseMessage): Promise<void> {
	if (client) {
		client.write(JSON.stringify(basemsg));
	}
}


// 导出函数供其他模块使用
export {
	isSanRunning,
	startSan,
	ensureSanRunning,
	cleanSanProcess,
	send,
};