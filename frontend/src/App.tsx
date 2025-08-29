import { useState } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Benefits from './components/Benefits';
import Capabilities from './components/Capabilities';
import Pricing from './components/Pricing';
import Testimonials from './components/Testimonials';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import CopilotSidebar from './components/CopilotSidebar';

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <div className="min-h-screen bg-white">
      <Header />

      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="lg:flex lg:gap-8">
          <main className="flex-1">
            <Hero />
            <Benefits />
            <Capabilities />
            <Pricing />
            <Testimonials />
            <FAQ />
            <Footer />
          </main>

          {/* On large screens: show the sidebar in the layout only when opened */}
          <div className="hidden lg:flex">
            {isChatOpen && (
              <div className="w-80">
                <CopilotSidebar />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile overlay: render the sidebar as a right-side overlay when opened */}
      {isChatOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div className="absolute inset-0 bg-black/40" onClick={() => setIsChatOpen(false)} />
          <div className="absolute right-0 top-16 bottom-0 w-full md:w-3/4 lg:w-80 bg-white shadow-xl">
            <CopilotSidebar />
          </div>
        </div>
      )}

      {/* Floating toggle button */}
      <button
        onClick={() => setIsChatOpen(s => !s)}
        aria-label="Toggle Copilot"
        className="fixed bottom-6 right-6 z-50 bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full shadow-lg flex items-center justify-center"
      >
        CP
      </button>
    </div>
  );
}

export default App;