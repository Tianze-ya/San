import { BaseMessage } from './types';
import fs from 'fs';

// 读取token
function get_token(): string {
	try {
		const data = fs.readFileSync('python/token', 'utf8');
		return data;
	} catch (err) {
		console.error('读取token出错:', err);
		return '';
	}
}

export function makeMsg(name: string,
	desc: string = '',
	data: Blob = new Blob()): BaseMessage {
	const token = get_token();
	return {
		name,
		desc,
		token,
		data
	}
}