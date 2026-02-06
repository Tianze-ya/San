export declare global {
  interface Window {
    ipc: {
      log: (msg: string) => void;
      send: (data: BaseMessage) => Promise<void>;
    };
  }
}

import { BaseMessage } from './index';