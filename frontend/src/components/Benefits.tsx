import React from 'react';
import { Shield, Zap, Users, Globe, Settings, BarChart3 } from 'lucide-react';

const benefits = [
  {
    icon: Globe,
    title: 'Optimized for Azure-native data sources',
    description: 'Connect seamlessly to Azure Monitor, Azure Data Explorer, and other Azure services with built-in optimization and performance.'
  },
  {
    icon: Users,
    title: 'Secure dashboard sharing for collaboration',
    description: 'Share Grafana dashboards with dispersed teams while maintaining security controls and access management.'
  },
  {
    icon: Shield,
    title: 'Integrated identity management',
    description: 'Centralize access control with Microsoft Entra ID (formerly Azure Active Directory) for seamless authentication and authorization.'
  },
  {
    icon: Zap,
    title: 'One-click dashboard authoring',
    description: 'Create dashboards instantly from existing charts in the Azure portal with seamless integration and data continuity.'
  },
  {
    icon: Settings,
    title: 'Comprehensive security and compliance',
    description: 'Built-in enterprise security with Microsoft\'s $1 billion annual cybersecurity investment and 3,500+ dedicated security experts.'
  },
  {
    icon: BarChart3,
    title: 'Observe all telemetry data in one place',
    description: 'Access wide variety of data sources supported by Grafana Enterprise and connect to Azure and external data stores.'
  }
];

const Benefits = () => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Key capabilities and benefits
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Deploy Grafana dashboards with built-in high availability and control access with Azure security.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => {
            const IconComponent = benefit.icon;
            return (
              <div
                key={index}
                className="group p-8 rounded-lg border border-gray-100 hover:border-blue-200 hover:shadow-xl transition-all duration-300"
              >
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-6 group-hover:bg-blue-200 transition-colors">
                  <IconComponent className="w-6 h-6 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {benefit.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {benefit.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Benefits;