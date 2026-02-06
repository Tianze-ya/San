import { MenuItemConstructorOptions } from 'electron';

const menuTemplate: MenuItemConstructorOptions[] = [
	{
		label: 'DevTools',
		role: 'toggleDevTools',
	},
];

export default menuTemplate;