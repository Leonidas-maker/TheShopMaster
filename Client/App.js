import App from './src/App';
export default App;
export * from './src/App';

import { NativeWindStyleSheet } from "nativewind";

NativeWindStyleSheet.setOutput({
  default: "native",
});