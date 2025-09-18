import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { store, persistor } from './redux/store.ts';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import ThemeProvider from './components/ThemeProvider.tsx'; // Keep your ThemeProvider


const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('Failed to find the root element');
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
      <PersistGate persistor={persistor}>
        <Provider store={store}>
          <ThemeProvider> {/* The ThemeProvider logic needs to be inside */}
            <App />
          </ThemeProvider>
        </Provider>
      </PersistGate>
  </React.StrictMode>
);
