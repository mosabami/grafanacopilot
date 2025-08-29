import { useState } from 'react';
import { Menu, X, ChevronDown } from 'lucide-react';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-8">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-blue-700 rounded-sm flex items-center justify-center">
                <span className="text-white font-bold text-sm">M</span>
              </div>
              <span className="ml-2 text-xl font-semibold text-gray-900">Microsoft Azure</span>
            </div>
            
            {/* Desktop Navigation */}
            <nav className="hidden lg:flex space-x-8">
              <div className="relative group">
                <button className="flex items-center text-gray-700 hover:text-blue-600 transition-colors">
                  Products <ChevronDown className="ml-1 w-4 h-4" />
                </button>
              </div>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Solutions</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Pricing</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Documentation</a>
            </nav>
          </div>

          {/* Desktop Actions */}
          <div className="hidden lg:flex items-center space-x-4">
            <button className="bg-blue-600 text-white px-4 py-2 rounded-sm hover:bg-blue-700 transition-colors">
              Free account
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="lg:hidden p-2 rounded-md text-gray-700 hover:text-blue-600"
          >
            {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="lg:hidden border-t border-gray-200 py-4">
            <nav className="flex flex-col space-y-4">
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Products</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Solutions</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Pricing</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Documentation</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 transition-colors">Sign in</a>
              <button className="bg-blue-600 text-white px-4 py-2 rounded-sm hover:bg-blue-700 transition-colors text-left">
                Free account
              </button>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;