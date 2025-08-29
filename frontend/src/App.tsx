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

          <div className="hidden lg:block w-80">
            <CopilotSidebar />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;