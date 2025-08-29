import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
    server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'grafanacopilotfront.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000012.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000011.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000013.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000014.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000015.livelywave-e155fae2.eastus2.azurecontainerapps.io',
      'grafanacopilotfront--0000016.livelywave-e155fae2.eastus2.azurecontainerapps.io'

    ]
  }

}); 
