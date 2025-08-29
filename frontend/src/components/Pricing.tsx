import React from 'react';
import { Check } from 'lucide-react';

const pricingTiers = [
  {
    name: 'Free Trial',
    price: 'Free',
    period: '30 days',
    description: 'Get started with Azure Managed Grafana',
    features: [
      '$200 credit to use within 30 days',
      'Free amounts of popular services',
      '55+ always-free services',
      'No upfront commitment',
      'Azure support included',
      'Full feature access'
    ],
    popular: false
  },
  {
    name: 'Pay-as-you-go',
    price: 'Usage-based',
    period: 'pricing',
    description: 'Pay only for what you use',
    features: [
      'Based on active users',
      'Hosting infrastructure costs',
      'No minimum commitment',
      'Scale up or down anytime',
      'Enterprise features included',
      'Azure Monitor integration',
      'Microsoft Entra ID support',
      '99.9% uptime SLA'
    ],
    popular: true
  },
  {
    name: 'Enterprise',
    price: 'Contact',
    period: '',
    description: 'For large-scale deployments',
    features: [
      'Volume discounts available',
      'Dedicated support team',
      'Custom SLA options',
      '99.99% SLA',
      'Advanced security features',
      'Professional services',
      'Custom deployment options',
      'Priority feature requests'
    ],
    popular: false
  }
];

const Pricing = () => {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Try Azure Managed Grafana free
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Azure Managed Grafana pricing is based on the number of active users and hosting infrastructure costs. 
            Try the service with a 30-day free trial.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {pricingTiers.map((tier, index) => (
            <div
              key={index}
              className={`relative rounded-lg p-8 ${
                tier.popular
                  ? 'bg-blue-50 border-2 border-blue-200 shadow-lg scale-105'
                  : 'bg-white border border-gray-200 shadow-sm'
              }`}
            >
              {tier.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-600 text-white px-4 py-2 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{tier.name}</h3>
                <p className="text-gray-600 mb-4">{tier.description}</p>
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold text-gray-900">{tier.price}</span>
                  <span className="text-gray-600 ml-1">{tier.period}</span>
                </div>
              </div>

              <ul className="space-y-4 mb-8">
                {tier.features.map((feature, idx) => (
                  <li key={idx} className="flex items-center">
                    <Check className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                    <span className="text-gray-700">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                className={`w-full py-3 px-6 rounded-sm font-medium transition-colors ${
                  tier.popular
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}
              >
                {tier.name === 'Enterprise' ? 'Contact sales' : tier.name === 'Free Trial' ? 'Start free trial' : 'Get started'}
              </button>
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <p className="text-gray-600 mb-4">
            Get started with an Azure free account. No credit card required for trial.
          </p>
          <div className="flex justify-center space-x-8 text-sm text-gray-500">
            <span>✓ $200 free credit</span>
            <span>✓ 55+ always-free services</span>
            <span>✓ Pay only for what you use</span>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;