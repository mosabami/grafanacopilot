import React from 'react';
import { Monitor, Database, AlertTriangle, Workflow, Cloud, Lock, Users, Settings } from 'lucide-react';

const capabilities = [
  {
    icon: Database,
    title: 'Observe all your telemetry data in one place',
    description: 'Access a wide variety of data sources supported by Grafana Enterprise and connect to your data stores in Azure and elsewhere.',
    features: ['Multiple dataset correlation', 'Holistic application view', 'Azure and external data stores']
  },
  {
    icon: Users,
    title: 'Collaborate easily with your team',
    description: 'Share Grafana dashboards with people inside and outside of your organization. Allow others to contribute to solution monitoring.',
    features: ['Internal and external sharing', 'Collaborative monitoring', 'Team contribution workflows']
  },
  {
    icon: Lock,
    title: 'Secure access with Microsoft Entra ID',
    description: 'Centralize identity management in Microsoft Entra ID. Control which users can use a Grafana instance and leverage managed identities.',
    features: ['Centralized identity management', 'User access controls', 'Managed identity support']
  },
  {
    icon: Monitor,
    title: 'Create dashboards with ease',
    description: 'Get started quickly with prebuilt dashboards for Azure services and import existing charts directly from the Azure Portal.',
    features: ['Prebuilt Azure dashboards', 'Azure Portal integration', 'Quick deployment']
  },
  {
    icon: Cloud,
    title: 'Comprehensive security and compliance',
    description: 'Microsoft invests more than $1 billion annually on cybersecurity research and development with 3,500+ security experts.',
    features: ['$1B+ annual security investment', '3,500+ security experts', 'Enterprise compliance']
  },
  {
    icon: Settings,
    title: 'Fully managed service experience',
    description: 'Focus on insights, not infrastructure. Azure handles deployment, scaling, updates, and maintenance automatically.',
    features: ['Zero infrastructure management', 'Automatic updates', 'Built-in high availability']
  }
];

const Capabilities = () => {
  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Complete observability and collaboration platform
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Combine charts, logs, and alerts to create one holistic view of your application and infrastructure.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {capabilities.map((capability, index) => {
            const IconComponent = capability.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-lg p-8 shadow-sm hover:shadow-lg transition-all duration-300 border border-gray-100"
              >
                <div className="flex items-start space-x-6">
                  <div className="w-14 h-14 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <IconComponent className="w-7 h-7 text-blue-600" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-semibold text-gray-900 mb-3">
                      {capability.title}
                    </h3>
                    <p className="text-gray-600 mb-4 leading-relaxed">
                      {capability.description}
                    </p>
                    <ul className="space-y-2">
                      {capability.features.map((feature, idx) => (
                        <li key={idx} className="flex items-center text-sm text-gray-600">
                          <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mr-3"></div>
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Capabilities;