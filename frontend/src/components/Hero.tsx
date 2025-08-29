import React from 'react';
import { ArrowRight, Play } from 'lucide-react';

const Hero = () => {
  return (
    <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            <div className="space-y-4">
              <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                Analytics and Monitoring Solutions
              </span>
              <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                Enhance your observability solution with
                <span className="text-blue-600"> rich data visualization</span>
              </h1>
              <p className="text-xl text-gray-600 leading-relaxed">
                Azure Managed Grafana is a fully managed service for analytics and monitoring solutions. 
                It's supported by Grafana Enterprise, which provides extensible data visualizations. 
                Quickly and easily deploy Grafana dashboards with built-in high availability and control access with Azure security.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="bg-blue-600 text-white px-8 py-4 rounded-sm hover:bg-blue-700 transition-all duration-300 flex items-center justify-center group">
                Try Azure for free
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="border border-gray-300 text-gray-700 px-8 py-4 rounded-sm hover:border-blue-600 hover:text-blue-600 transition-all duration-300 flex items-center justify-center">
                <Play className="mr-2 w-5 h-5" />
                See pricing
              </button>
            </div>

            <div className="flex items-center space-x-8 text-sm text-gray-600">
              <span>✓ 30-day free trial</span>
              <span>✓ Built-in high availability</span>
              <span>✓ Azure security integrated</span>
            </div>
          </div>

          <div className="relative">
            <div className="bg-white rounded-lg shadow-2xl p-8">
              <div className="bg-gray-900 rounded-lg p-6">
                <div className="flex items-center space-x-2 mb-4">
                  <div className="w-3 h-3 bg-red-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-yellow-400 rounded-full"></div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <div className="space-y-4">
                  <div className="bg-blue-500 h-2 w-3/4 rounded"></div>
                  <div className="bg-green-500 h-2 w-1/2 rounded"></div>
                  <div className="bg-orange-500 h-2 w-5/6 rounded"></div>
                  <div className="grid grid-cols-2 gap-4 mt-6">
                    <div className="bg-gray-700 h-16 rounded"></div>
                    <div className="bg-gray-700 h-16 rounded"></div>
                  </div>
                </div>
              </div>
              <div className="mt-4 text-center text-sm text-gray-500">
                Interactive Grafana Dashboard
              </div>
            </div>
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-blue-100 rounded-full opacity-50"></div>
            <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-indigo-100 rounded-full opacity-50"></div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;